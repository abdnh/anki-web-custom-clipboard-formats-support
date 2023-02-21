A demo of Chrome's custom clipboard formats. You need to run a local server for the demo to work because it `fetch()`s the local audio to get its blob and copy it to the clipboard. If you use Python run the following:

```
python -m http.server
```

If you play the audio in the demo page then go to Anki and paste (with the add-on installed), the audio should be written to your media folder and a sound tag like `[sound:alarm.wav]` pasted.

The [copyaudio.js](copyaudio.js) script can also be used a userscript (written for Violentmonkey) that copies any currently playing audio to the clipboard.
