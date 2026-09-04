"""Render Apple DocC JSON (developer.apple.com/tutorials/data/*.json) to Markdown.

developer.apple.com/documentation/* and /design/* are a JavaScript SPA: a plain
GET returns roughly 50 characters of shell HTML. The same content is served as
structured JSON from the tutorials/data endpoint, which is what this reads.
"""
import re

def _refs(doc):
    return doc.get("references", {}) or {}


def _url_for(ref):
    u = ref.get("url") or ""
    if u.startswith("/"):
        u = "https://developer.apple.com" + u
    return u


def inline(items, doc):
    if items is None:
        return ""
    if isinstance(items, str):
        return items
    out = []
    for it in items:
        if isinstance(it, str):
            out.append(it)
            continue
        t = it.get("type")
        if t == "text":
            out.append(it.get("text", ""))
        elif t == "codeVoice":
            out.append("`%s`" % it.get("code", ""))
        elif t in ("emphasis", "italic"):
            out.append("*%s*" % inline(it.get("inlineContent"), doc))
        elif t in ("strong", "bold"):
            out.append("**%s**" % inline(it.get("inlineContent"), doc))
        elif t == "reference":
            ident = it.get("identifier", "")
            ref = _refs(doc).get(ident, {})
            title = ref.get("title") or inline(it.get("inlineContent"), doc) or ident
            url = _url_for(ref)
            out.append("[%s](%s)" % (title, url) if url else title)
        elif t == "link":
            out.append("[%s](%s)" % (it.get("title", ""), it.get("destination", "")))
        elif t == "image":
            ref = _refs(doc).get(it.get("identifier", ""), {})
            alt = ref.get("alt") or ""
            if alt:
                out.append("![%s]" % alt)
        elif t == "inlineHead":
            out.append("**%s**" % inline(it.get("inlineContent"), doc))
        elif "inlineContent" in it:
            out.append(inline(it["inlineContent"], doc))
        elif "content" in it:
            out.append(inline(it["content"], doc))
    return "".join(out)


MAX_BLOCK_DEPTH = 150


def blocks(items, doc, depth=0):
    if not items:
        return []
    if depth > MAX_BLOCK_DEPTH:
        # Same defensive cap as htmlmd._blocks -- this walks Apple's own
        # DocC JSON, so pathological nesting is unlikely, but there is no
        # reason to trust that indefinitely across whatever Apple's toolchain
        # emits in the future.
        return []
    out = []
    for b in items:
        if not isinstance(b, dict):
            continue
        t = b.get("type")
        if t == "paragraph":
            s = inline(b.get("inlineContent"), doc).strip()
            if s:
                out.append(s)
        elif t == "heading":
            lvl = min(max(int(b.get("level", 2)), 1), 6)
            out.append("#" * lvl + " " + (b.get("text") or inline(b.get("inlineContent"), doc)))
        elif t == "aside":
            style = (b.get("style") or b.get("name") or "Note").title()
            body = "\n".join(blocks(b.get("content"), doc, depth + 1))
            out.append("> **%s:** %s" % (style, body.replace("\n", "\n> ")))
        elif t == "codeListing":
            code = "\n".join(b.get("code") or [])
            out.append("```%s\n%s\n```" % (b.get("syntax") or "", code))
        elif t in ("unorderedList", "orderedList"):
            lines = []
            for i, li in enumerate(b.get("items") or [], 1):
                body = "\n".join(blocks(li.get("content"), doc, depth + 1)).strip()
                if not body:
                    continue
                bullet = ("%d." % i) if t == "orderedList" else "-"
                first, *rest = body.splitlines()
                lines.append("%s %s" % (bullet, first))
                lines += ["  " + r for r in rest]
            if lines:
                out.append("\n".join(lines))
        elif t == "termList":
            for it in b.get("items") or []:
                term = inline((it.get("term") or {}).get("inlineContent"), doc)
                dfn = "\n".join(blocks((it.get("definition") or {}).get("content"), doc, depth + 1))
                out.append("- **%s** — %s" % (term, dfn.replace("\n", " ").strip()))
        elif t == "table":
            rows = b.get("rows") or []
            if not rows:
                continue
            hdr = b.get("header")
            md = []
            for ri, row in enumerate(rows):
                cells = ["".join(blocks(c, doc, depth + 1)).replace("\n", " ").replace("|", "\\|")
                         if isinstance(c, list) else str(c) for c in row]
                md.append("| " + " | ".join(cells) + " |")
                if ri == 0 and hdr in ("row", "both", None):
                    md.append("|" + "|".join([" --- "] * len(cells)) + "|")
            out.append("\n".join(md))
        elif t == "dictionaryExample":
            out.append("```json\n%s\n```" % (b.get("example") or ""))
        elif "content" in b:
            out += blocks(b.get("content"), doc, depth + 1)
    return out


def render(doc):
    """doc: parsed tutorials/data JSON. Returns markdown."""
    meta = doc.get("metadata", {}) or {}
    title = meta.get("title") or ""
    parts = []
    if title:
        parts.append("# " + title)
    abstract = inline(doc.get("abstract"), doc).strip()
    if abstract:
        parts.append(abstract)

    for sec in doc.get("primaryContentSections") or []:
        kind = sec.get("kind")
        if kind == "content":
            parts += blocks(sec.get("content"), doc)
        elif kind == "properties":
            parts.append("## Properties")
            for p in sec.get("items") or []:
                name = p.get("name", "")
                types = ", ".join(
                    inline(t if isinstance(t, list) else [t], doc)
                    for t in (p.get("type") or []))
                desc = "\n".join(blocks(p.get("content"), doc)).strip()
                head = "### `%s`" % name if name else "###"
                parts.append(head + (" — *%s*" % types if types else ""))
                if desc:
                    parts.append(desc)
        elif kind == "declarations":
            for d in sec.get("declarations") or []:
                toks = "".join(t.get("text", "") for t in d.get("tokens") or [])
                if toks:
                    parts.append("```\n%s\n```" % toks)
        elif kind in ("parameters", "possibleValues", "attributes", "restrictions"):
            label = kind.replace("possibleValues", "Possible values").title()
            parts.append("## " + label)
            for p in sec.get("parameters") or sec.get("values") or sec.get("items") or []:
                nm = p.get("name") or p.get("value") or ""
                desc = "\n".join(blocks(p.get("content"), doc)).strip()
                parts.append("- **%s** — %s" % (nm, desc.replace("\n", " ")) if desc
                             else "- **%s**" % nm)
        else:
            parts += blocks(sec.get("content"), doc)

    for sec in doc.get("topicSections") or []:
        ttl = sec.get("title") or "Topics"
        links = []
        for ident in sec.get("identifiers") or []:
            ref = _refs(doc).get(ident, {})
            if ref.get("title"):
                u = _url_for(ref)
                links.append("- [%s](%s)" % (ref["title"], u) if u else "- " + ref["title"])
        if links:
            parts.append("## " + ttl)
            parts.append("\n".join(links))

    for sec in doc.get("seeAlsoSections") or []:
        links = []
        for ident in sec.get("identifiers") or []:
            ref = _refs(doc).get(ident, {})
            if ref.get("title"):
                u = _url_for(ref)
                links.append("- [%s](%s)" % (ref["title"], u) if u else "- " + ref["title"])
        if links:
            parts.append("## See Also")
            parts.append("\n".join(links))

    md = "\n\n".join(p for p in parts if p and p.strip())
    return re.sub(r"\n{3,}", "\n\n", md).strip()
