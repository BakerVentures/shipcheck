"""Structural chunker for the App Store Review Guidelines.

Apple marks every clause in the DOM:

    <li data-sidenav="1.1 Objectionable Content" id="objectionable-content">
      <span id="1.1"></span><strong>1.1 Objectionable Content</strong>
      <p>...</p>
      <ul><li id="1.1.1"><strong>1.1.1</strong> ...</li> ...</ul>
    </li>

so we chunk on that structure rather than on regex over rendered markdown.
Two things fall out of this for free:
  * exact clause numbers, including lettered sub-clauses like 3.1.2(a) -> "3.1.2a"
  * a real deep link per clause (the <li> slug id), so a citation can point at
    https://developer.apple.com/app-store/review/guidelines/#permissible-uses
"""
import re
import htmlmd
from htmlmd import Node

CLAUSE_ID_RE = re.compile(r"^\d+(?:\.\d+)*[a-z]?$")


def _clause_span(node):
    """Return the clause number if this node carries a clause anchor span."""
    for c in node.children:
        if isinstance(c, Node) and c.tag == "span":
            sid = c.attrs.get("id", "").strip()
            if CLAUSE_ID_RE.match(sid):
                return sid
    # some sub-clauses put the id on the <li> itself
    sid = node.attrs.get("id", "").strip()
    if CLAUSE_ID_RE.match(sid):
        return sid
    return None


def _has_clause(node):
    if not isinstance(node, Node):
        return False
    if _clause_span(node):
        return True
    return any(_has_clause(c) for c in node.children if isinstance(c, Node))


def _title_of(node, clause):
    ds = node.attrs.get("data-sidenav", "").strip()
    if ds:
        return re.sub(r"^\d+(?:\.\d+)*[a-z]?\.?\s*", "", ds).strip() or ds
    for c in node.children:
        if isinstance(c, Node) and c.tag in ("strong", "b"):
            t = htmlmd._clean(htmlmd._inline(c))
            t = re.sub(r"^\d+(?:\.\d+)*(?:\([a-z]\))?\.?\s*", "", t).strip(" :")
            if t:
                return t
    return ""


def _prune_clause_children(root):
    """Remove only the descendant <li>s that are themselves clauses.

    Dropping the whole nested <ul> would lose sibling content that has no
    clause id of its own -- 5.1.1's roman items (i)-(iv) live next to the
    anchored 5.1.1(v) and must stay with the parent clause.
    """
    saved = []

    def walk(n):
        kids, changed = [], False
        for c in n.children:
            if isinstance(c, Node) and c is not root and _clause_span(c):
                changed = True
                continue
            kids.append(c)
        if changed:
            saved.append((n, n.children))
            n.children = kids
        for c in n.children:
            if isinstance(c, Node):
                walk(c)

    walk(root)
    return saved


def _render_without_nested_clauses(node):
    """Markdown for this clause, excluding sub-clauses that get their own chunk."""
    saved = _prune_clause_children(node)
    try:
        blocks = htmlmd._blocks(node)
    finally:
        for n, kids in reversed(saved):
            n.children = kids
    md = "\n\n".join(b for b in blocks if b.strip())
    return re.sub(r"\n{3,}", "\n\n", md).strip()


def extract(html, base_url):
    """Returns a list of clause dicts, document order."""
    root = htmlmd.parse(html)
    content = htmlmd.pick_root(root, "apple_html")
    out, seen = [], set()

    stack = [content]
    order = []
    while stack:
        n = stack.pop()
        if isinstance(n, Node):
            order.append(n)
            stack.extend(reversed([c for c in n.children if isinstance(c, Node)]))

    for node in order:
        if node.tag not in ("li", "h2", "h3", "h4"):
            continue
        clause = _clause_span(node)
        if not clause or clause in seen:
            continue
        seen.add(clause)
        title = _title_of(node, clause)
        if node.tag in ("h2", "h3", "h4"):
            text = htmlmd._clean(htmlmd._inline(node))
        else:
            text = _render_without_nested_clauses(node)
        if len(text) < 15:
            continue
        slug_id = node.attrs.get("id", "").strip()
        if not CLAUSE_ID_RE.match(slug_id) and slug_id:
            deep = "%s#%s" % (base_url.rstrip("/") + "/", slug_id)
        else:
            deep = "%s#%s" % (base_url.rstrip("/") + "/", clause)
        out.append(dict(
            anchor=clause,
            title=title,
            text=text,
            deep_link=deep,
            depth=clause.count(".") + 1,
        ))

    def sortkey(c):
        m = re.match(r"^([\d.]+)([a-z]?)$", c["anchor"])
        nums = tuple(int(x) for x in m.group(1).split("."))
        return (nums, m.group(2))

    out.sort(key=sortkey)
    return out
