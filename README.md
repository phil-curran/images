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

This repo is optimized primarily for **VS Code + the Draw.io extension**.

It also includes a `config.json` file for people using the **web browser version of draw.io / diagrams.net**, but browser behavior is different and more manual.

---

## Repository structure

A typical layout looks like this:

```text
.
├── .vscode/
│   └── settings.json
├── libraries/
│   └── all-icons.xml
├── config.json
├── MASTER.drawio
└── README.md
```

### Important files

#### `.vscode/settings.json`

This file configures the VS Code Draw.io extension for this repository. It includes things like:

- preset colors
- default vertex style
- default edge style
- custom fonts
- custom library loading

The shared settings use `hediet.vscode-drawio.*` keys, including a repo-relative custom library entry.

#### `libraries/all-icons.xml`

This is the shared custom icon library for the project.

This file must be a valid Draw.io library file. The icon entries inside it include fields like `title`, `data`, `w`, `h`, `aspect`, and `tags`.

#### `config.json`

This file is for **browser-based draw.io / diagrams.net users**. It contains draw.io-style editor configuration such as:

- `defaultFonts`
- `presetColors`
- `customColorSchemes`
- `defaultVertexStyle`
- `defaultEdgeStyle`

This file is **not** used by the VS Code Draw.io extension.

#### `*.drawio`

These are the actual diagram files. These are the real project artifacts and should be treated as the source of truth for diagram content.

---

## Recommended workflow

The recommended workflow for this repository is:

1. Clone the repo
2. Open the repo root in VS Code
3. Install the Draw.io extension for VS Code
4. Confirm the workspace `.vscode/settings.json` is active
5. Open or create a `.drawio` file
6. Use the shared icon library and default styles

This is the supported path.

---

## VS Code setup

### 1. Clone the repository

Clone the repository normally:

```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Open the repo root in VS Code

Open the **repository root folder** in VS Code, not a subfolder like `libraries/`.

This matters because the custom library path in workspace settings is repo-relative:

```json
"file": "${workspaceFolder}/libraries/all-icons.xml"
```

If you open the wrong folder as the workspace root, the extension may fail to find the icon library.

#### Correct

Open:

```text
<repo-root>
```

#### Incorrect

Do not open only:

```text
<repo-root>/libraries
```

or another nested folder unless you also update the workspace setting.

### 3. Install the VS Code Draw.io extension

Install the Draw.io extension for VS Code.

Search the Extensions panel for Draw.io, or install the extension published by the `hediet` project.

After installation, reload VS Code if prompted.

### 4. Verify that workspace settings are active

Open the workspace settings JSON and confirm the repo settings are present.

You should see a `.vscode/settings.json` file containing keys like:

- `hediet.vscode-drawio.presetColors`
- `hediet.vscode-drawio.customColorSchemes`
- `hediet.vscode-drawio.defaultVertexStyle`
- `hediet.vscode-drawio.defaultEdgeStyle`
- `hediet.vscode-drawio.customFonts`
- `hediet.vscode-drawio.customLibraries`

If these settings are not active, the repo is not configured correctly in your VS Code workspace.

#### Important

The shared settings file must be applied as **workspace settings**, not copied into user-global settings unless you intentionally want that behavior everywhere.

The repo is designed so that cloning and opening the repo root should automatically apply the workspace settings.

### 5. Reload the VS Code window

After cloning, installing the extension, or changing the settings file, run:

- `Developer: Reload Window`

This helps ensure the Draw.io extension reloads the workspace settings and library configuration.

### 6. Open a `.drawio` file

Open an existing `.drawio` file such as `MASTER.drawio`, or create a new one.

The file should open in the Draw.io custom editor.

If it opens as plain text instead:

1. Right click the file
2. Choose **Reopen Editor With...**
3. Select the Draw.io editor

### 7. Confirm the shared defaults are active

After opening a diagram, verify:

- the shared preset colors are available
- new shapes use the expected default styling
- the custom icon library is available

---

## Custom icon library behavior

This repo includes a shared custom icon library at:

```text
libraries/all-icons.xml
```

The VS Code workspace settings point the Draw.io extension at that file using:

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

If the repo root is opened correctly and the extension loads successfully, the shared icon library should be available in the Draw.io sidebar.

### Important limitation

The icon library is **not stored inside the `.drawio` file just because you can see it in the UI**.

The `.drawio` file stores the actual diagram content, pages, and any icons already placed on the canvas.

The library itself is loaded by the editor environment.

That means:

- if you drag icons from the library onto the diagram and save the file, those placed icons are part of the `.drawio` file
- but the visibility and availability of the **library itself** depends on the editor configuration, not on saving the diagram

For VS Code users, the repo’s workspace settings are what make the library available automatically.

---

## Browser usage: important differences

This repo can also be used with the browser version of draw.io / diagrams.net, but the behavior is different.

### The browser does not use `.vscode/settings.json`

The browser version does **not** read the repository’s `.vscode/settings.json`.

That file is only meaningful to the VS Code Draw.io extension.

So if someone opens a `.drawio` file in the browser, they should not expect the VS Code workspace configuration to load automatically.

### The browser uses `config.json`, not `settings.json`

The browser-side configuration lives in `config.json`, which contains draw.io editor config like:

- `defaultFonts`
- `presetColors`
- `customColorSchemes`
- `defaultVertexStyle`
- `defaultEdgeStyle`

This file exists so browser users can manually load or apply the shared browser configuration.

### The browser also does not automatically load the icon library from the repo

Opening a `.drawio` file in the browser does **not** automatically load the repo’s custom library file into the Shapes sidebar.

A browser user may need to manually load or import the shared icon library.

---

## Why browser usage may appear inconsistent

Using the same `.drawio` file in VS Code and the browser can still work, but browser users need to understand these differences:

- browser settings are separate from VS Code settings
- browser configuration persistence depends on the browser profile and local storage
- the browser does not automatically read `.vscode/settings.json`
- the browser does not automatically attach the repo’s library or sidebar state to the `.drawio` file
- a library being visible for one user does not mean it will appear automatically for another user unless they also load or configure it

For that reason, the recommended supported workflow is still:

**Use VS Code as the primary editing environment for this repo.**

---

## Safe usage rules

### Use one `.drawio` file as the source of truth per project

A good pattern is:

- one master `.drawio` file per project
- multiple pages inside that file for related diagrams and slides
- one shared icon library in `libraries/all-icons.xml`
- one shared `.vscode/settings.json`

This keeps the editing model simple and reduces fragmentation.

### Do not hand-edit `.drawio` files unless necessary

A `.drawio` file is XML and can break if merge conflict markers or malformed XML are introduced.

If a merge conflict happens, resolve it carefully.

Do not leave markers like:

```text
<<<<<<< HEAD
=======
>>>>>>> branch
```

inside a `.drawio` file.

### Be careful with unsupported or newer style syntax

If a diagram opens in the browser but hangs in VS Code, one possible cause is unsupported style syntax in the file. Keep diagram styling simple and stable where possible.

### Keep the custom library file valid

The shared icon library must remain a proper Draw.io library file.

The library file must not be just a raw JSON array. It must be wrapped as a Draw.io library file.

At minimum, it should look structurally like:

```xml
<mxlibrary>
[
  {
    "title": "example",
    "data": "data:image/svg+xml;base64,...",
    "w": 64,
    "h": 64,
    "aspect": "fixed",
    "tags": "example"
  }
]
</mxlibrary>
```

---

## Troubleshooting

### Problem: the Draw.io editor does not load in VS Code

Try the following:

1. Remove recent changes to `.vscode/settings.json`
2. Reload the window
3. Open the `.drawio` file again
4. Re-add settings incrementally if necessary

A malformed or problematic workspace setting can interfere with editor startup.

### Problem: the custom icon library does not appear

Check these in order:

1. Confirm you opened the repo root in VS Code
2. Confirm the file exists at:

```text
<repo-root>/libraries/all-icons.xml
```

3. Confirm `.vscode/settings.json` contains the expected `customLibraries` entry
4. Reload the VS Code window
5. Reopen the `.drawio` file
6. Search for a known icon title in the library

### Problem: the library file exists but still does not load

Check whether `all-icons.xml` is a valid Draw.io library file.

The file content must not be just a raw JSON array. It must be wrapped as a Draw.io library file.

### Problem: someone uses the browser and says the colors or icons are missing

That is expected unless they have separately loaded the browser-side config and library.

The browser does not consume `.vscode/settings.json`.

They need to use the browser-oriented repo assets, not the VS Code settings file.

---

## Contributor guidance

If you update this repository, follow these rules:

1. Keep `.vscode/settings.json` minimal and stable
2. Keep `libraries/all-icons.xml` valid
3. Prefer repo-relative paths in workspace settings
4. Do not assume browser users automatically get VS Code behavior
5. Use `.drawio` files for diagram content, not for storing editor configuration expectations

---

## Summary

### VS Code users

Supported path.

They should:

- clone the repo
- open the repo root
- install the Draw.io extension
- let `.vscode/settings.json` configure the extension
- use the shared icon library and palette

### Browser users

Possible, but more manual.

They should:

- understand that `.vscode/settings.json` does not apply in the browser
- use `config.json` separately
- manually ensure the icon library is available if needed

### Source of truth

The `.drawio` files are the source of truth for the diagrams themselves.

The icon library and editor settings are shared repo assets that support the editing experience, but they are not automatically embedded into the `.drawio` file just because the diagram was saved.