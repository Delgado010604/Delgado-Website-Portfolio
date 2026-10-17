"""Build the static portfolio from src/, using only Python's standard library.

Run normally to regenerate HTML, or use --check to detect stale output.
"""

import argparse
import json
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "src"
PAGE_TITLES = {
    "index.html": "Web Developer | UI/UX | Data Analytics",
    "projects.html": "Selected projects",
    "profile.html": "About",
    "role.html": "Education & focus",
    "techstack.html": "Toolkit",
    "certificates.html": "Credentials",
    "contact.html": "Contact",
}


def render(template, **values):
    """Substitute trusted HTML fragments into a source template."""
    source = (SOURCE / template).read_text(encoding="utf-8")
    return Template(source).substitute(values).strip()


def text(value):
    """Escape plain content before inserting it into HTML or attributes."""
    return escape(str(value), quote=True)


def render_tags(items):
    return '<div class="tags">' + "".join(
        f"<span>{text(item)}</span>" for item in items
    ) + "</div>"


def render_navigation(items, current_page):
    links = []
    for item in items:
        current = ' aria-current="page"' if current_page == item["url"] else ""
        links.append(
            f'<a href="{text(item["url"])}"{current}>{text(item["label"])}</a>'
        )
    current = ' aria-current="page"' if current_page == "contact.html" else ""
    links.append(
        f'<a class="nav-contact" href="contact.html"{current}>'
        'Let’s talk <span aria-hidden="true">↗</span></a>'
    )
    return "\n".join(links)


def render_project(project, full=False):
    slug = text(project["slug"])
    if full:
        features = "".join(f"<li>{text(item)}</li>" for item in project["features"])
        details = f'<ul class="project-features">{features}</ul>'
    else:
        details = (
            f'<a class="text-link" href="projects.html#{slug}">'
            'Explore project <span aria-hidden="true">↗</span></a>'
        )
    return render(
        "components/project.html",
        classes="project project-full" if full else "project",
        slug=slug,
        art=render(f'components/art-{project["art"]}.html'),
        number=text(project["number"]),
        technology=text(project["technologies"][0].upper()),
        name=text(project["name"]),
        headline=text(project["headline"]),
        description=text(project["description"]),
        tags=render_tags(project["technologies"]),
        details=details,
    )


def render_certificate(certificate, index):
    filename = certificate["file"]
    if Path(filename).name != filename or "jpcs" in filename.lower():
        raise ValueError(f"Invalid certificate file: {filename}")
    if not (ROOT / "assets/certificates" / filename).is_file():
        raise FileNotFoundError(f"Certificate missing: {filename}")
    credential = certificate["credential"]
    return render(
        "components/certificate.html",
        category=text(certificate["category"]),
        number=f"{index:02}",
        issuer=text(certificate["issuer"]),
        title=text(certificate["title"]),
        credential=(
            f'<p class="credential-id">ID: {text(credential)}</p>' if credential else ""
        ),
        date=text(certificate["date"]),
        href="assets/certificates/" + quote(filename),
    )


def build_pages():
    data = json.loads((SOURCE / "data/portfolio.json").read_text(encoding="utf-8"))
    projects = data["projects"]
    shared = {
        "closing": render("components/closing.html"),
        "orbital": render("components/orbital.svg"),
        "projects": "\n".join(render_project(project, full=True) for project in projects),
        "certificates": "\n".join(
            render_certificate(certificate, index)
            for index, certificate in enumerate(data["certificates"], start=1)
        ),
        "certificate_count": len(data["certificates"]),
        "project_count": f"{len(projects):02}",
        "toolkit": "\n".join(
            render(
                "components/tool-group.html",
                number=text(group["number"]),
                title=text(group["title"]),
                description=text(group["description"]),
                tags=render_tags(group["items"]),
            )
            for group in data["toolkit"]
        ),
    }
    shared.update({f"project_{i}": render_project(p) for i, p in enumerate(projects)})
    return {
        filename: render(
            "layout.html",
            title=text(title),
            navigation=render_navigation(data["navigation"], filename),
            body=render(f"pages/{filename}", **shared),
        ) + "\n"
        for filename, title in PAGE_TITLES.items()
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check output without writing files")
    args = parser.parse_args()
    pages = build_pages()
    if args.check:
        stale = [
            filename for filename, html in pages.items()
            if not (ROOT / filename).is_file()
            or (ROOT / filename).read_text(encoding="utf-8") != html
        ]
        if stale:
            parser.exit(1, "Regenerate stale pages: " + ", ".join(stale) + "\n")
        print(f"All {len(pages)} pages match their source templates.")
        return
    for filename, html in pages.items():
        (ROOT / filename).write_text(html, encoding="utf-8", newline="\n")
    print(f"Built {len(pages)} pages from src/.")


if __name__ == "__main__":
    main()
