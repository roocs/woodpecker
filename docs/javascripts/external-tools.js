// Keep the documentation open when launching the standalone fixes browser.
function configureToolLinks() {
  document.querySelectorAll('a[href]').forEach((link) => {
    const url = new URL(link.href, document.baseURI);
    if (url.origin === location.origin && url.pathname.endsWith('/fixes.html')) {
      link.target = '_blank';
      link.relList.add('noopener', 'noreferrer');
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', configureToolLinks);
} else {
  configureToolLinks();
}
