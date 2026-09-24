// Check the assembled site at its GitHub Pages prefix using DeckTape's browser.
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const http = require('node:http');
const { createRequire } = require('node:module');
const path = require('node:path');

const npmRoot = execFileSync('npm', ['root', '--global'], { encoding: 'utf8' }).trim();
const load = createRequire(path.join(npmRoot, 'decktape', 'package.json'));
const puppeteer = load('puppeteer');
const root = path.resolve(__dirname, '../site');
const talks = fs.readdirSync(path.resolve(__dirname, '../talks')).filter(
  name => fs.existsSync(path.resolve(__dirname, '../talks', name, 'slides.qmd'))
);
const failures = [];
const server = http.createServer((req, res) => {
  const pathname = new URL(req.url, 'http://localhost').pathname;
  if (!pathname.startsWith('/woodpecker/')) {
    res.writeHead(404).end();
    return;
  }
  let file = path.resolve(root, pathname.slice('/woodpecker/'.length));
  if (pathname.endsWith('/')) file = path.join(file, 'index.html');
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
    failures.push('Missing resource: ' + pathname);
    res.writeHead(404).end();
    return;
  }
  const mime = { '.html': 'text/html', '.pdf': 'application/pdf', '.js': 'text/javascript',
    '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png' }[path.extname(file)];
  res.setHeader('Content-Type', mime || 'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});

async function main() {
  assert(talks.length > 0, 'No talk sources found');
  let browser;
  try {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}/woodpecker/`;
    browser = await puppeteer.launch({ headless: true, args: process.env.CI ? ['--no-sandbox'] : [] });
    const page = await browser.newPage();
    page.on('pageerror', error => failures.push(error.message));
    page.on('requestfailed', request => {
      // External fonts are optional; local publication assets must all work.
      if (request.url().startsWith(base)) failures.push(request.url());
    });
    await page.goto(base, { waitUntil: 'networkidle0' });
    const fixesLinks = await page.$$eval('a[href]', links => links
      .filter(link => new URL(link.href).pathname.endsWith('/fixes.html'))
      .map(link => ({ target: link.target, safe: link.relList.contains('noopener') })));
    assert(fixesLinks.length > 0, 'Missing Interactive Fix Browser links');
    assert(fixesLinks.every(link => link.target === '_blank' && link.safe));
    const tabs = await page.$$eval('.md-tabs__link', links => links.map(link => link.textContent.trim()));
    assert.equal(tabs.at(-1), 'Talks', 'Talks should be the final navigation tab');
    await page.goto(base + 'talks/', { waitUntil: 'networkidle0' });
    const links = await page.$$eval('article a.md-button', links => links.map(link => ({
      href: link.href, target: link.target, safe: link.relList.contains('noopener')
    })));
    assert.equal(links.length, talks.length * 2);
    for (const link of links) {
      assert.equal(link.target, '_blank');
      assert(link.safe);
      assert.equal((await fetch(link.href)).status, 200, link.href);
    }
    for (const talk of talks) {
      await page.goto(base + 'talks/' + talk + '/', { waitUntil: 'networkidle0' });
      await page.waitForFunction(() => window.Reveal && Reveal.isReady());
      const slides = await page.evaluate(async () => {
        await Promise.all([...document.images].map(image => image.decode()));
        return Reveal.getTotalSlides();
      });
      assert(slides > 0, 'Empty deck: ' + talk);
      console.log(`Verified ${talk}: ${slides} slides and all images loaded`);
    }
    assert.deepEqual(failures, []);
    console.log('Verified /woodpecker/ links, navigation, new-tab targets and slide assets.');
  } finally {
    if (browser) await browser.close();
    server.closeAllConnections();
    server.close();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
