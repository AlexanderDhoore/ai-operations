// Render original screenshots inside a small CSS shadow, without resampling them.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '../..');
const widths = JSON.parse(fs.readFileSync(path.join(__dirname, 'widths.json'), 'utf8'));
const output = path.join(root, 'assets/screenshots');
const displayWidths = {};

function imageTag(alt, source) {
  const name = path.posix.basename(source);
  if (!displayWidths[name]) return null;
  const folder = path.posix.dirname(source).replace(/\/screenshots$/, '');
  const original = path.posix.join(folder, name);
  const framed = path.posix.join(folder, 'screenshots', name);
  const escaped = alt.replaceAll('&', '&amp;').replaceAll('"', '&quot;');
  return `<a href="${original}"><img src="${framed}" alt="${escaped}" width="${displayWidths[name]}"></a>`;
}

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROMIUM_EXECUTABLE ? { executablePath: process.env.CHROMIUM_EXECUTABLE } : {}),
    args: ['--no-sandbox'],
  });
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  try {
    for (const [name, contentWidth] of Object.entries(widths)) {
      const data = fs.readFileSync(path.join(root, 'assets', name)).toString('base64');
      await page.setContent(`<style>html,body{margin:0;background:transparent}img{display:block}</style><img src="data:image/png;base64,${data}">`);
      const size = await page.locator('img').evaluate(async img => {
        await img.decode();
        return { width: img.naturalWidth, height: img.naturalHeight };
      });
      if (contentWidth > size.width || contentWidth <= 0) throw Error(`Invalid display width: ${name}`);
      const scale = contentWidth / size.width;
      // At the intended Markdown width: 12px margin, 2px offset, 6px blur.
      const padding = Math.ceil(12 / scale);
      await page.setViewportSize({ width: size.width + 2 * padding, height: size.height + 2 * padding });
      await page.locator('img').evaluate((img, { padding, scale }) => {
        img.style.margin = `${padding}px`;
        img.style.boxShadow = `0 ${2 / scale}px ${6 / scale}px rgba(0,0,0,0.18)`;
      }, { padding, scale });
      await page.screenshot({ path: path.join(output, name), omitBackground: true });
      displayWidths[name] = Math.round((size.width + 2 * padding) * scale);
    }
  } finally {
    await browser.close();
  }

  const docs = fs.readdirSync(root).filter(n => /^\d\d-.*\.md$/.test(n)).map(n => path.join(root, n));
  docs.push(path.join(root, 'resources/pi/README.md'));
  for (const file of docs) {
    let text = fs.readFileSync(file, 'utf8');
    text = text.replace(/\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)/g,
      (match, alt, source) => imageTag(alt, source) || match);
    text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g,
      (match, alt, source) => imageTag(alt, source) || match);
    text = text.replace(/<img\b[^>]*>/g, tag => {
      const source = tag.match(/src="([^"]+)"/);
      if (!source) return tag;
      const name = path.posix.basename(source[1]);
      if (!displayWidths[name]) return tag;
      const folder = path.posix.dirname(source[1]).replace(/\/screenshots$/, '');
      tag = tag.replace(/src="[^"]+"/, `src="${path.posix.join(folder, 'screenshots', name)}"`);
      tag = tag.replace(/\swidth="[^"]*"/, '');
      return tag.replace(/>$/, ` width="${displayWidths[name]}">`);
    });
    fs.writeFileSync(file, text);
  }
  console.log(`Rendered and linked ${Object.keys(widths).length} screenshots. Originals and diagrams unchanged.`);
})().catch(error => { console.error(error); process.exitCode = 1; });
