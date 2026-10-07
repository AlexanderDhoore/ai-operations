# Screenshot presentation

Assignment screenshots use a soft shadow with a narrow transparent margin.
Original PNGs stay in `assets/`. Display copies live in `assets/screenshots/`,
and clicking one opens the untouched original. Diagrams, logos and illustrations
are excluded.

`widths.json` sets each screenshot's displayed content width in pixels. Choose
it by comparing ordinary screenshot text with the surrounding Markdown text,
not by forcing every image to the same width. Do not enlarge small captures.
GitHub's responsive image styling can shrink images further on narrow screens.

`render.cjs` places each original at its native resolution in a browser layout,
adds an external CSS shadow, and captures a transparent PNG. It never rescales
or redraws the source screenshot. At the intended display width the margin is
about 12 pixels, with a 2-pixel downward shadow offset and 6-pixel blur. There
is no added border. Markdown width attributes include the margin.

To regenerate after adding an original or changing a display width, run with
Node.js and Playwright available in your tooling environment:

```bash
node tools/screenshots/render.cjs
```

For an existing Playwright installation or a specific Chromium executable,
set `PLAYWRIGHT_MODULE` and `CHROMIUM_EXECUTABLE`. These are authoring tools,
not student dependencies. The script updates the numbered assignments and
Pi setup guide. It can be rerun without nesting frames or duplicating links.

Review the rendered pages after changing sizes. Preserve readable details,
keep the margin small, and leave the original image available for enlargement.
