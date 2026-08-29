# Chronicle Rating — Context Menu Button

[![Latest Release](https://img.shields.io/github/v/release/thegoddamnbeckster/Chronicle_Rating_Context?label=Chronicle_Rating_Context&color=1a5276)](https://github.com/thegoddamnbeckster/Chronicle_Rating_Context/releases/latest)

A tiny Kodi addon whose entire job is adding a **"Rate on Chronicle"** button to the
context menu for movies and episodes in your video library, and handing off to
[Chronicle_Rating](https://github.com/thegoddamnbeckster/Chronicle_Rating) to actually
show the rating dialog and submit it to your self-hosted
[Chronicle](https://github.com/thegoddamnbeckster/Chronicle) server.

**Addon ID:** `context.chronicle.rate`
**Version:** 1.0.1
**Kodi:** 19 "Matrix" and later
**Requires:** [Chronicle_Rating](https://github.com/thegoddamnbeckster/Chronicle_Rating) installed and connected

---

## Why this is a separate addon

Kodi's `kodi.context.item` extension point has to live in its own standalone addon —
declaring it inside `script.chronicle.rating`'s own `addon.xml`, alongside that addon's
`xbmc.service` and `xbmc.python.script` extensions, was tried first and confirmed live
not to work: the "Rate on Chronicle" item never actually appeared in Kodi's context menu
at all, even though the extension was declared correctly on paper.

This isn't a one-off Chronicle quirk — [SIMKL's own official Kodi
scrobbler](https://github.com/thegoddamnbeckster/SIMKLScrobbler) hits the exact same
constraint and solves it the same way: a dedicated `context.simkl.rate` addon whose only
job is the menu registration, delegating to the real addon via `RunScript`. This repo
mirrors that split precisely.

## How it works

```
Kodi context menu (movie/episode)
    │
    │  user picks "Rate on Chronicle"
    ▼
addon.py
    │  reads ListItem.DBTYPE / ListItem.DBID for whatever's focused
    ▼
RunScript(script.chronicle.rating, action=rate, media_type=<movie|episode>, dbid=<id>)
    │
    ▼
script.chronicle.rating's default.py
    resolves the item via fresh VideoLibrary JSON-RPC lookups (not ListItem
    infolabels — those aren't reliably populated for episodes in every view),
    then shows the real star-rating dialog and submits to Chronicle.
```

`addon.py` never talks to Chronicle directly, never shows any UI of its own, and never
does DBID-to-metadata resolution itself — all of that lives in `script.chronicle.rating`,
which this addon requires. If that addon isn't installed or isn't connected, the context
menu item still appears, but selecting it does nothing useful until it is.

## Installation

Install via Kodi's **Install from zip file**, or copy this directory directly into Kodi's
`addons/` folder and restart Kodi:

```
<Kodi userdata>/addons/context.chronicle.rate/
```

Requires `script.chronicle.rating` to be installed too — install that one first (see its
own README for setup).

## Repository Structure

```
Chronicle_Rating_Context/
├── addon.xml
├── addon.py                      # Reads the focused item, delegates via RunScript
├── icon.png                      # Chronicle's own "C" icon
├── LICENSE
└── resources/
    └── language/resource.language.en_gb/strings.po
```

No `lib/`, no `service.py` — this addon has nothing to do beyond the single `addon.py`
entry point above.

## License

MIT — see [LICENSE](LICENSE).
