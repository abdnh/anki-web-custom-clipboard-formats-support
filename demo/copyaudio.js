// ==UserScript==
// @name copy_audio
// @namespace Violentmonkey Scripts
// @match *://*/*
// @grant none
// ==/UserScript==

const CORS_SERVER = "http://127.0.0.1:6868/";

async function copyAudio(audio) {
    const data = await fetch(CORS_SERVER + audio.src);
    const blob = await data.blob();
    await navigator.clipboard.write([
        // https://developer.chrome.com/blog/web-custom-formats-for-the-async-clipboard-api/
        new ClipboardItem({
            [`web ${blob.type}`]: blob,
        }),
    ]);
}

function attachAudioPlayListener(audio) {
    audio.addEventListener("play", () => {
        copyAudio(audio);
    });
}

for (const audio of document.querySelectorAll("audio")) {
    attachAudioPlayListener(audio);
}

const observer = new MutationObserver((records) => {
    for (const record of records) {
        for (const node of record.addedNodes) {
            if (node instanceof Audio) {
                attachAudioPlayListener(node);
            }
        }
    }
});

observer.observe(document, {
    childList: true,
    subtree: true,
});
