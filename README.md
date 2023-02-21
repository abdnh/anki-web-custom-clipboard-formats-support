This is an Anki add-on that adds support for pasting clipboard content stored in Chrome's [Web custom formats](https://developer.chrome.com/blog/web-custom-formats-for-the-async-clipboard-api/). All media formats supported by Anki should work.

See the [demo](demo) subfolder for an example of how websites can take advantage of Web custom formats. The [copyaudio.js](./demo/copyaudio.js) script is a userscript (written for Violentmonkey) that copies any currently playing audio to the clipboard.

By default, the add-on runs a local server that's used by copyaudio.js to act as a proxy to bypass possible CORS issues when fetching audio URLs. You can disable this from the config if you don't need it.
