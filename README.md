# Get Carrie’d Away

Cosplay and costuming portfolio for Carrie and Nick, plus the tools we build. Live at https://getcarriedaway.art.

| Path | Page |
|---|---|
| `/` | Home |
| `/carrie/` | Carrie's Work |
| `/nick/` | Nick's Work |
| `/tools/lightbench/` | Lightbench instructions |
| `/tools/lightbench/app/` | Lightbench app (single static page) |
| `/tools/helmetscaler/app/` | HelmetScaler: fit a helmet STL to a sized head, section view, strip cutter |
| `/tools/armorscaler/app/` | Armor Scaler: body shaped from tape measurements, STL export |

- Plain static HTML. The shared pages (home, portfolios, Lightbench instructions, 404) are generated: edit `build/pages.py`, then run `python3 build/pages.py .` — hand edits to those five HTML files are overwritten. Shared styles in `assets/site.css`, menu and filter script in `assets/site.js`.
- Brand: logo kit in `assets/brand/` (use the SVGs as-is). Logo fonts are Baloo 2 with "Away" in Pacifico; slogan font is Caveat. Site headings use Baloo 2, labels Caveat, body Nunito.
- Hosted on GitHub Pages from `main` / root. `CNAME` sets the custom domain.
- Placeholders in `[brackets]` are photos and copy still to supply. A photo goes in by replacing a placeholder's `<span class="label">` with `<img src="..." alt="...">`.
- Lightbench stores projects and calibration in the browser (IndexedDB) on each device. Nothing is uploaded.
- HelmetScaler loads three.js from jsDelivr and the two reference heads from `tools/helmetscaler/app/models/` (meshopt-compressed GLB, mm units). Presets live in localStorage. STLs never leave the browser.
- Armor Scaler uses the MakeHuman base mesh and targets (CC0), baked by `tools/armorscaler/build/build.py` into `tools/armorscaler/app/data/`. Rerun the script to rebuild the data.
