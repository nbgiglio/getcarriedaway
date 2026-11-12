# Lightbench

Projects sewing patterns at true size onto a cutting mat. Runs in the browser on a tablet or laptop connected to a projector. Live at https://getcarriedaway.art.

- Single static page: `index.html`. No build step.
- Hosted on GitHub Pages from `main` / root. `CNAME` sets the custom domain.
- Libraries load from cdnjs (pdf.js 3.11.174) and Google Fonts.
- Projects and calibration are stored in the browser's IndexedDB on each device. Nothing is uploaded.
