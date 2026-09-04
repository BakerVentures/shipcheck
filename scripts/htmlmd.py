"""Minimal HTML -> Markdown converter. Standard library only.

Builds a light DOM with html.parser, drops chrome, then renders the best
content container to Markdown. Tables are preserved as pipe tables because
Apple's third-party SDK list and Google's Data safety page are mostly tables.
"""
import re
from html.parser import HTMLParser
from html import unescape

VOID = {"br", "img", "hr", "input", "meta", "link", "source", "col", "area", "base", "wbr"}
DROP_TAGS = {"script", "style", "noscript", "svg", "nav", "header", "footer",
             "aside", "form", "button", "iframe", "template", "picture", "video"}
DROP_ATTR_RE = re.compile(
    r"(^|[-_ ])(nav|menu|footer|header|breadcrumb|sidebar|cookie|banner|promo|"
    r"related|feedback|social|share|search|skip|localnav|globalnav|ac-gn|"
    r"chapter-nav|pagination|newsletter|subscribe-|footnote-back|modal|dialog|"
    r"overlay|offscreen|visuallyhidden|sr-only|tooltip)($|[-_ ])",
    re.I)


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = parent

    def text(self):
        out = []
        stack = [self]
        while stack:
            n = stack.pop()
            if isinstance(n, str):
                out.append(n)
            else:
                stack.extend(reversed(n.children))
        return "".join(out)

    def find_all(self, pred):
        found = []
        stack = [self]
        while stack:
            n = stack.pop()
            if isinstance(n, Node):
                if pred(n):
                    found.append(n)
                stack.extend(reversed(n.children))
        return found


class DOM(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root
        self.skip_depth = 0
        self.skip_tag = None

    def handle_starttag(self, tag, attrs):
        if self.skip_depth:
            if tag == self.skip_tag and tag not in VOID:
                self.skip_depth += 1
            return
        if tag in DROP_TAGS:
            if tag in VOID:
                return
            self.skip_depth = 1
            self.skip_tag = tag
            return
        a = {k: (v or "") for k, v in attrs}
        node = Node(tag, a, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_endtag(self, tag):
        if self.skip_depth:
            if tag == self.skip_tag:
                self.skip_depth -= 1
                if self.skip_depth == 0:
                    self.skip_tag = None
            return
        if tag in VOID:
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent or self.root

    def handle_data(self, data):
        if self.skip_depth:
            return
        if data.strip():
            self.cur.children.append(data)
        elif data and self.cur.children:
            self.cur.children.append(" ")


def parse(html):
    d = DOM()
    d.feed(html)
    return d.root


def _is_junk(node):
    blob = (node.attrs.get("class", "") + " " + node.attrs.get("id", ""))
    return bool(blob) and bool(DROP_ATTR_RE.search(blob))


# ---------------------------------------------------------------- rendering
def _inline(node):
    """Render inline content of a node to markdown text."""
    parts = []
    for c in node.children:
        if isinstance(c, str):
            parts.append(c)
            continue
        if _is_junk(c):
            continue
        t = c.tag
        if t in ("strong", "b"):
            raw = _inline(c)
            inner = raw.strip()
            lead = " " if raw != raw.lstrip() else ""
            trail = " " if raw != raw.rstrip() else ""
            # A leading/trailing space belongs to the surrounding sentence,
            # not the emphasis -- Apple's markup puts it *inside* the tag
            # (e.g. "<strong>(v) Account Sign-In: </strong>If your app..."),
            # so a bare .strip() here used to silently glue the next word
            # onto the closing "**" with no space between them.
            parts.append(f"{lead}**{inner}**{trail}" if inner else "")
        elif t in ("em", "i"):
            raw = _inline(c)
            inner = raw.strip()
            lead = " " if raw != raw.lstrip() else ""
            trail = " " if raw != raw.rstrip() else ""
            parts.append(f"{lead}*{inner}*{trail}" if inner else "")
        elif t == "code":
            raw = _inline(c)
            inner = raw.strip()
            lead = " " if raw != raw.lstrip() else ""
            trail = " " if raw != raw.rstrip() else ""
            parts.append(f"{lead}`{inner}`{trail}" if inner else "")
        elif t == "a":
            inner = _inline(c).strip()
            href = c.attrs.get("href", "").strip()
            if inner and href and not href.startswith("#"):
                parts.append(f"[{inner}]({href})")
            else:
                parts.append(inner)
        elif t == "br":
            parts.append("\n")
        elif t == "img":
            alt = c.attrs.get("alt", "").strip()
            if alt:
                parts.append(f"![{alt}]")
        else:
            parts.append(_inline(c))
    return "".join(parts)


def _clean(s):
    s = unescape(s)
    s = s.replace(" ", " ").replace("​", "")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    return s.strip()


def _table(node):
    rows = []
    for tr in node.find_all(lambda n: n.tag == "tr"):
        cells = [c for c in tr.children
                 if isinstance(c, Node) and c.tag in ("td", "th")]
        if cells:
            rows.append([_clean(_inline(c)).replace("\n", " ").replace("|", "\\|")
                         for c in cells])
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |",
           "|" + "|".join([" --- "] * width) + "|"]
    for r in rows[1:]:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


MAX_BLOCK_DEPTH = 150


def _blocks(node, depth=0):
    if depth > MAX_BLOCK_DEPTH:
        # A real page has never come close to this; a pathologically nested
        # one (or an adversarial one, since this parser also runs on
        # whatever a GitHub Action's target repo happens to fetch) hits
        # Python's default recursion limit here otherwise. Flatten instead
        # of crashing that one source -- fetch_corpus.py's per-source
        # try/except already bounds the blast radius to just this page, but
        # there is no reason to make it rely on that as the only backstop.
        s = _clean(node.text())
        return [s] if s else []
    INLINE_TAGS = ("a", "strong", "b", "em", "i", "code", "span", "br",
                   "sub", "sup", "u", "small", "abbr", "cite", "q")

    def _is_inline(child):
        # A junk inline element (e.g. a decorative tooltip-icon <span>) must
        # still count as inline here even though it renders to nothing --
        # otherwise it acts as a wall in the middle of a run of real inline
        # siblings ("<strong>1.4.2</strong><span class=tooltip-icon>...</span>
        # Drug dosage calculators...") and splits one sentence into two
        # paragraphs, the same bug this run-grouping exists to prevent.
        # _inline() already drops junk children when it renders the run, so
        # letting it through here costs nothing.
        if isinstance(child, str):
            return True
        return isinstance(child, Node) and child.tag in INLINE_TAGS

    out = []
    children = list(node.children)
    i = 0
    n = len(children)
    while i < n:
        c = children[i]
        # A run of text/inline-tag siblings appearing as DIRECT children of a
        # block container -- common in Apple's markup, e.g. a bare <li> whose
        # content is "text <a href=...>link</a> more text" with no wrapping
        # <p>. Handling each sibling one at a time here (the old behavior)
        # sent every text node down the "text" branch and every <a>/<strong>
        # down the generic "unknown element" recursion below, and each of
        # those became its own top-level block -- splitting one sentence
        # across three separate paragraphs around any inline link, mid-word.
        # Buffer the whole run and render it as one paragraph instead.
        if _is_inline(c):
            run = []
            while i < n and _is_inline(children[i]):
                run.append(children[i])
                i += 1
            fake = Node("span")
            fake.children = run
            fake.parent = node
            s = _clean(_inline(fake))
            if s:
                out.append(s)
            continue
        if _is_junk(c):
            i += 1
            continue
        t = c.tag
        if t in ("h1", "h2", "h3", "h4", "h5", "h6"):
            s = _clean(_inline(c))
            if s:
                out.append("#" * int(t[1]) + " " + s.replace("\n", " "))
        elif t == "p":
            s = _clean(_inline(c))
            if s:
                out.append(s)
        elif t in ("ul", "ol"):
            items = []
            count = 0
            for li in c.children:
                if isinstance(li, Node) and li.tag == "li":
                    # keep nested lists readable
                    sub = [x for x in li.children
                           if isinstance(x, Node) and x.tag in ("ul", "ol")]
                    s = _clean(_inline(li))
                    if not s and not sub:
                        continue
                    count += 1
                    bullet = f"{count}." if t == "ol" else "-"
                    if s:
                        items.append(f"{bullet} {s.splitlines()[0] if s else ''}")
                    for sl in sub:
                        nested = _blocks(sl, depth + 1)
                        for line in "\n".join(nested).splitlines():
                            if line.strip():
                                items.append("  " + line)
            if items:
                out.append("\n".join(items))
        elif t == "table":
            s = _table(c)
            if s:
                out.append(s)
        elif t == "pre":
            s = _clean(c.text())
            if s:
                out.append("```\n" + s + "\n```")
        elif t == "blockquote":
            s = _clean(_inline(c))
            if s:
                out.append("> " + s.replace("\n", "\n> "))
        elif t == "hr":
            out.append("---")
        elif t in ("dl",):
            s = _clean(_inline(c))
            if s:
                out.append(s)
        else:
            out.extend(_blocks(c, depth + 1))
        i += 1
    return out


CONTAINER_HINTS = {
    "google_help": ["article-content-container", "cc", "article-content"],
    "android_dev": ["devsite-article-body", "devsite-article"],
    "apple_html": ["main", "content", "section-content"],
    "generic": ["main", "content", "prose", "markdown"],
}


def _junk_ancestor(node):
    """True if this node or any ancestor is chrome.

    Apple's help pages embed a hidden search modal whose subtree is larger than
    the article itself, so checking the node alone is not enough.
    """
    n = node
    while n is not None:
        if _is_junk(n):
            return True
        if n.attrs.get("aria-hidden") == "true":
            return True
        if "display:none" in n.attrs.get("style", "").replace(" ", ""):
            return True
        n = n.parent
    return False


def pick_root(root, strategy="generic"):
    """Choose the densest plausible content container."""
    hints = CONTAINER_HINTS.get(strategy, CONTAINER_HINTS["generic"])
    candidates = []
    for h in hints:
        candidates += root.find_all(
            lambda n, h=h: h in (n.attrs.get("class", "") + " " + n.attrs.get("id", "")).split())
    candidates += root.find_all(lambda n: n.attrs.get("itemprop") == "articleBody")
    candidates += root.find_all(lambda n: n.tag in ("main", "article"))
    candidates = [c for c in candidates if not _junk_ancestor(c)]
    candidates = [c for c in candidates if len(c.text()) > 300]
    if candidates:
        return max(candidates, key=lambda n: len(n.text()))
    body = root.find_all(lambda n: n.tag == "body")
    return body[0] if body else root


def to_markdown(html, strategy="generic"):
    root = parse(html)
    content = pick_root(root, strategy)
    blocks = _blocks(content)
    md = "\n\n".join(b for b in blocks if b.strip())
    md = re.sub(r"\n{3,}", "\n\n", md)
    # collapse the runs of repeated nav text Apple leaves in the DOM
    lines, seen_run, out = md.splitlines(), 0, []
    for ln in lines:
        if out and ln.strip() and ln == out[-1]:
            seen_run += 1
            if seen_run > 1:
                continue
        else:
            seen_run = 0
        out.append(ln)
    return "\n".join(out).strip()
