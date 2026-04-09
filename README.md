# Draw.io Template Project

This repository provides a shared starting point for creating and maintaining `.drawio` diagrams with:

- a standard color palette
- standard default styles
- a shared custom icon library
- a repo-level VS Code setup for the Draw.io extension

The main goal is to make it easy for anyone on the team to clone the repo, open it in VS Code, and start creating diagrams with the same visual defaults and the same shared icon set.

---

## What this repo is for

Use this repo when you want:

- one or more `.drawio` files as the source of truth for a project
- multiple pages inside a single `.drawio` file for related diagrams
- a shared icon library checked into Git
- consistent diagram styling across contributors

This repo is optimized primarily for **VS Code / Cursor + the Draw.io extension**.

It also includes **`config/config.json`** for people using the **web browser version of draw.io / diagrams.net**, but browser behavior is different and more manual.

---

## Repository structure

A typical layout looks like this:

```text
.
├── .vscode/
│   └── settings.json
├── config/
│   └── config.json
├── icons/                          # source SVGs (optional for consumers)
├── libraries/
│   └── all-icons.xml               # generated Draw.io library
├── scripts/
│   └── build_drawio_icon_library.py
├── main.drawio                     # canonical diagram file (recommended hub)
└── README.md
```

### Important files

#### `.vscode/settings.json`

This file configures the VS Code / Cursor Draw.io extension for this repository. It includes things like:

- preset colors
- default vertex style
- default edge style
- custom fonts
- custom library loading

The shared settings use `hediet.vscode-drawio.*` keys, including a repo-relative custom library entry.

#### `libraries/all-icons.xml`

This is the shared custom icon library for the project.

This file must be a valid Draw.io library file. Entries include fields like `title`, `data`, `w`, `h`, `aspect`, and `tags`. It is **generated** from `icons/**/*.svg` by running:

```bash
python3 scripts/build_drawio_icon_library.py
```

Regenerate after adding or changing SVGs under `icons/`.

#### `config/config.json`

This file is for **browser-based draw.io / diagrams.net users** and for **draw.io desktop** (e.g. symlink or merge into the app’s Application Support `config.json`). It contains editor configuration such as:

- `defaultFonts`
- `presetColors`
- `customColorSchemes`
- `defaultVertexStyle`
- `defaultEdgeStyle`

This file is **not** used by the VS Code Draw.io extension (the extension uses `.vscode/settings.json`).

**Note:** Editor configuration is **not** embedded inside `.drawio` diagram files. The diagram XML holds pages and shapes only; palette and library availability come from the environment (workspace settings, desktop config, or manual browser steps).

#### `main.drawio`

**Canonical diagram file** for this repo. Treat it as the main hub for project visuals unless you intentionally add other `.drawio` files. It can contain multiple **pages** (tabs), each a `<diagram>` in the XML.

---

## Recommended workflow (humans)

The recommended workflow for this repository is:

1. Clone the repo
2. Open the repo root in VS Code or Cursor
3. Install the **Draw.io Integration** extension (publisher **Henning Dieterichs**, id `hediet.vscode-drawio`)
4. Confirm the workspace `.vscode/settings.json` is active
5. Open **`main.drawio`**
6. Use the shared icon library and default styles

This is the supported path.

---

## Workflow for AI agents

Use this section when an automated agent (or contributor following agent-style steps) should extend diagrams in this repo.

### Canonical file

- Treat **`main.drawio`** as the **single canonical diagram file** for new visuals unless the user specifies another path.
- The file is XML: `<mxfile>` → one or more `<diagram>` pages → `<mxGraphModel>` → `<root>` and `mxCell` elements.

### Adding a new page (tab)

When the user asks for a new diagram **page** with a given name:

1. **Name** — Set the `<diagram>` attribute **`name`** to the suggested page name (e.g. `Architecture-v2`, `S6`). Escape XML special characters (`&` → `&amp;`, etc.).
2. **Unique id** — Give each `<diagram>` a unique **`id`** (opaque string, e.g. `agent-` + random suffix or a UUID-like value) so it does not clash with existing pages.
3. **Structure** — Append a new **`<diagram>...</diagram>`** block **before** `</mxfile>`, after the last existing diagram. Inside it, use **`mxGraphModel`** with attributes consistent with existing pages (copy `pageWidth`, `pageHeight`, grid settings from `Page-1` unless the user wants different dimensions).
4. **Empty canvas** — Inside **`<root>`**, include exactly:
   - `<mxCell id="0"/>`
   - `<mxCell id="1" parent="0"/>`  
   Root ids `0` and `1` are normal **per page**.
5. **`pages` attribute** — On **`<mxfile>`**, set **`pages="<N>"`** where **N** is the **exact count** of `<diagram>` elements. A mismatch (e.g. `pages="5"` with only one diagram) can break the Draw.io UI.
6. **Validate** — Ensure the file remains well-formed XML.

### Editing diagram content

- New shapes are additional **`<mxCell>`** elements under that page’s **`<root>`**, usually with `parent="1"`, plus `vertex="1"` or `edge="1"`, `style`, `value`, and **`mxGeometry`** as needed.
- Align colors/fonts with **`.vscode/settings.json`** / **`config/config.json`** when brand consistency matters.
- **Icons:** In the UI, use the **Brand icons** library (from `libraries/all-icons.xml`). In raw XML, prefer simple shapes unless the user requires embedded images (data URIs are heavy).

### Optional: export or rebuild assets

- **Regenerate icon library** after changing `icons/`:

  ```bash
  python3 scripts/build_drawio_icon_library.py
  ```

- **Export one page with draw.io desktop** (page index is **1-based**):

  ```bash
  "/Applications/draw.io.app/Contents/MacOS/draw.io" -x -f svg -o out.svg -p 1 main.drawio
  ```

  Adjust `-p` for the tab index and paths for your OS.

### If the Draw.io editor does not open in Cursor / VS Code

That is an **IDE** issue, not the diagram XML:

1. Install **Draw.io Integration** (`hediet.vscode-drawio`).
2. Open **`main.drawio`** from the Explorer.
3. If it opens as plain XML, use **Reopen Editor With…** → **Draw.io** editor.
4. Open the **repository root** as the workspace so `.vscode/settings.json` applies.

Agents can still edit **`main.drawio` as XML** without the visual editor; the steps above apply either way.

### Agent checklist (short)

| Step | Action |
|------|--------|
| 1 | Open `main.drawio` and count existing `<diagram>` elements. |
| 2 | Add `<diagram name="…" id="…">` with empty `mxGraphModel` + `root` (`0`, `1`). |
| 3 | Set `<mxfile … pages="<count>">` to match the number of diagrams. |
| 4 | Save; have the user verify layout in Draw.io when possible. |

---

## VS Code / Cursor setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Open the repo root

Open the **repository root folder**, not a subfolder like `libraries/`.

The custom library path is repo-relative:

```json
"file": "${workspaceFolder}/libraries/all-icons.xml"
```

If the workspace root is wrong, the extension may not find the icon library.

### 3. Install the Draw.io extension

Install **Draw.io Integration** (search Extensions for Draw.io / `hediet`). Reload the window if prompted.

### 4. Verify workspace settings

Confirm `.vscode/settings.json` contains:

- `hediet.vscode-drawio.presetColors`
- `hediet.vscode-drawio.customColorSchemes`
- `hediet.vscode-drawio.defaultVertexStyle`
- `hediet.vscode-drawio.defaultEdgeStyle`
- `hediet.vscode-drawio.customFonts`
- `hediet.vscode-drawio.customLibraries`

These should be **workspace** settings (the file in the repo), not only user-global settings, unless you want them everywhere.

### 5. Reload the window

Run **Developer: Reload Window** after cloning or changing settings.

### 6. Open `main.drawio`

Open **`main.drawio`**. It should open in the Draw.io editor. If it opens as text, use **Reopen Editor With…** → Draw.io.

### 7. Confirm shared defaults

Check preset colors, default styles for new shapes, and the **Brand icons** library in the sidebar.

---

## Custom icon library behavior

The shared library lives at:

```text
libraries/all-icons.xml
```

Workspace settings load it via:

```json
"hediet.vscode-drawio.customLibraries": [
  {
    "libName": "Brand icons",
    "entryId": "all-icons",
    "file": "${workspaceFolder}/libraries/all-icons.xml"
  }
]
```

### What this means

- Icons **placed on the canvas** are stored **inside** the saved `.drawio` file.
- The **library panel** (list of draggable icons) is provided by the **editor configuration**, not by the diagram file alone.

### Library file shape

The generated file uses an **`mxlibrary`** wrapper around a **JSON array** of entries (see [draw.io custom library format](https://www.drawio.com/doc/faq/format-custom-shape-library)). Do not replace it with unstructured text.

---

## Browser usage: important differences

The browser version does **not** read `.vscode/settings.json`.

Browser-oriented configuration is in **`config/config.json`**. Users paste or merge that into **Extras → Configuration** (or **Settings → Configuration** on some themes), per [diagrams.net configuration](https://www.drawio.com/doc/faq/configure-diagram-editor).

The browser does **not** automatically load `libraries/all-icons.xml` from the repo; users may need to **File → Open Library** or host the library URL.

---

## Why browser usage may appear inconsistent

- Browser settings ≠ VS Code workspace settings.
- Persistence depends on browser storage / profile.
- Library visibility is per user unless they load the same library file.

**Recommended primary environment:** VS Code or Cursor with this repo as the workspace root.

---

## Safe usage rules

- Prefer **one hub** `.drawio` file (**`main.drawio`**) with **multiple pages** for related diagrams.
- **Keep `pages="N"` on `<mxfile>` equal to the real number of `<diagram>` elements.**
- `.drawio` files are XML—resolve merge conflicts carefully; never leave conflict markers inside the file.
- Prefer stable, simple styling if diagrams must open in both VS Code and browser.
- Keep **`libraries/all-icons.xml`** valid; regenerate with `scripts/build_drawio_icon_library.py` after icon changes.

---

## Troubleshooting

### Draw.io editor does not load in VS Code / Cursor

1. Confirm **Draw.io Integration** (`hediet.vscode-drawio`) is installed.
2. **Reopen Editor With…** → Draw.io.
3. Temporarily simplify `.vscode/settings.json` and reload if a bad setting blocks the webview.
4. Open the **repo root** as the workspace.

### Custom icon library does not appear

1. Repo root is the workspace folder.
2. File exists: `libraries/all-icons.xml`.
3. `.vscode/settings.json` includes `customLibraries` with `${workspaceFolder}/libraries/all-icons.xml`.
4. Reload the window and reopen `main.drawio`.

### Browser: colors or icons missing

Expected unless the user applied **`config/config.json`** in the browser and loaded the library manually. The browser does not use `.vscode/settings.json`.

---

## Contributor guidance

1. Keep `.vscode/settings.json` minimal and stable.
2. Keep `libraries/all-icons.xml` valid; run `python3 scripts/build_drawio_icon_library.py` after editing `icons/`.
3. Use repo-relative paths in workspace settings.
4. Do not assume browser users get VS Code behavior automatically.
5. Use **`main.drawio`** (or an agreed file) for diagram content; do not rely on embedding full editor `config.json` inside `.drawio` files—the standard app does not apply palette config from inside the diagram XML.

---

## Summary

### VS Code / Cursor users

- Clone, open repo root, install Draw.io Integration, use `.vscode/settings.json`, open **`main.drawio`**, use **Brand icons** and shared palette.

### AI agents

- Use **`main.drawio`** as the hub; add **new `<diagram>` pages** with the **suggested name** and a **unique id**; keep **`pages`** accurate; prefer XML-safe edits and user verification in the visual editor when possible.

### Browser users

- More manual: apply **`config/config.json`** in the editor; load **`libraries/all-icons.xml`** if needed.

### Source of truth

- **Diagram content** lives in **`.drawio`** files (recommended: **`main.drawio`** with multiple pages).
- **Palette, defaults, and library sidebar** come from **`.vscode/settings.json`**, **`config/config.json`**, and **`libraries/all-icons.xml`**, not from inside the diagram file.
