# Angel Delgado — Portfolio

A static, responsive portfolio covering mobile development, embedded systems, and data analytics.

## Preview

Serve this directory with any static web server, for example:

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765. There are no build dependencies. The HTML pages can also be opened directly; email copying depends on browser clipboard permissions.

## Content

- Overview, projects, about, toolkit, credentials, and contact pages.
- The existing `role.html` address remains available for education and areas of focus, linked from About.
- All 14 supplied certificates except JPCS are stored in `assets/certificates/` and linked from the filterable credentials page.
- CDSA displays December 2025 per the owner's correction. The supplied original PDF is unchanged.
- The current revised resume is available from the download buttons. It lists five selected certifications; the website retains all 14.
- Contact details and project descriptions follow the supplied resume. Role and toolkit descriptions reflect coursework and project familiarity. The contact form opens a draft in the visitor's email application; it does not send messages through a server.
- Project illustrations are original schematic diagrams, not app screenshots or live telemetry.

## Editing

The seven HTML files at the root are ready-to-serve output. Edit the source files below, then regenerate the HTML:

```sh
python build_portfolio.py
```

| Location | What to edit |
| --- | --- |
| `src/data/portfolio.json` | Projects, certificates, toolkit, and navigation |
| `src/layout.html` | Shared document, header, navigation, and footer |
| `src/pages/` | Content and layout specific to each page |
| `src/components/` | Reusable project cards, credentials, diagrams, and closing section |
| `assets/css/main.css` | Theme variables, page styles, and responsive rules |
| `assets/css/no-script.css` | Mobile navigation when JavaScript is disabled |
| `assets/js/main.js` | Navigation, credential filters, and contact interactions |
| `assets/certificates/` | Original certificate files referenced by the data |

The generator uses only Python's standard library and does nothing when imported. It validates certificate file references and escapes text from the data file. Project and certificate counts are calculated from the data.

Check that generated files match their source without changing them:

```sh
python build_portfolio.py --check
```

To add a credential, copy its file into `assets/certificates/`, add an entry with its exact filename to `src/data/portfolio.json`, and regenerate the pages. Use an existing category, or update the filter buttons in `src/pages/certificates.html` when introducing a new one. JPCS files are rejected by the generator.

Google Fonts supplies DM Sans and Space Grotesk, with local system fallbacks. Navigation, project content, and credential links work without JavaScript. JavaScript adds the mobile menu, credential filters, email copying, and email draft preparation. The hero artwork responds subtly to pointer movement on desktop. Reduced-motion preferences are respected.
