import {micromark} from 'https://esm.sh/micromark@3'
import {gfm, gfmHtml} from 'https://esm.sh/micromark-extension-gfm@3'

const queryString = window.location.search;
const urlParams = [...new URLSearchParams(queryString).keys()];
const content = document.querySelector('.content');
const page = urlParams[0] || 'index';

function process() {
    // 1. Process all anchors (your existing logic)
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

    const images = content.querySelectorAll('img');
    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', () => {
            enlarge(img.src);
        });
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

function enlarge(url) {
    const overlay = document.createElement("div");
    overlay.className = "overlay";

    const image = document.createElement("img");
    image.src = url;
    image.style.position = "fixed"; 
    image.style.top = "50%";
    image.style.left = "50%";
    image.style.transform = "translate(-50%, -50%)";
    image.style.maxWidth = "90vw";
    image.style.maxHeight = "90vh";
    image.style.zIndex = "1000";
    image.style.border = "2px solid #333";
    image.style.boxShadow = "0 0 10px rgba(0, 0, 0, 0.5)";
    image.className = "large";

    if (document.querySelector(".overlay") !== null) {
        console.log("nope");
    } else {
        overlay.appendChild(image);
        document.body.appendChild(overlay);
        console.log("yep");
    }

    overlay.onclick = function () {
        document.body.removeChild(overlay);
    };
}

window.enlarge = enlarge;

load(page);
