import {micromark} from 'https://esm.sh/micromark@3'
import {gfm, gfmHtml} from 'https://esm.sh/micromark-extension-gfm@3'

const queryString = window.location.search;
const urlParams = [...new URLSearchParams(queryString).keys()];
const content = document.querySelector('.content');
const page = urlParams[0] || 'index';

function process() {
    const links = document.querySelectorAll('a');
    
    links.forEach(link => {
        const hasHref = link.getAttribute('href');
        if (!hasHref) return;
        const isExternal = link.hostname && link.hostname !== window.location.hostname;
        const isImageFile = /\.(png|jpe?g|gif|webp|svg)$/i.test(link.getAttribute('href'));
        const containsImg = link.querySelector('img');

        if (isExternal || isImageFile || containsImg) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
}


function load(url) {
  fetch(`../pages/${url}.md`)
  .then(response => {
    if (!response.ok) {
      throw new Error('HTTP error: ' + response.status);
    }
    return response.text();
  })
  .then(textData => {
    content.innerHTML = micromark(textData, {
      allowDangerousHtml: true,
      extensions: [gfm()],
      htmlExtensions: [gfmHtml()]
    })
    process();
  })
  .catch(error => {
    console.error('Fetch:', error);
    load('404');
  });
}

load(page);