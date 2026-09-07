# Site Tests

Test videos are generated with ffmpeg (small synthetic clips, no copyrighted material):

- test_small.mp4 — 5s, 640x360, ~80KB
- test_medium.mp4 — 15s, 1280x720, ~280KB

## How to run the site locally

```bash
cd site
python3 -m http.server 8877
# open http://localhost:8877/ (EN) or http://localhost:8877/he/ (HE)
```

## Verification checklist

- [x] EN page loads, all assets 200 (js/css/fonts/worker)
- [x] HE page loads (RTL), all assets 200
- [x] Drop zone accepts file, shows controls
- [x] Preset chips switch; custom slider appears on Custom
- [ ] Real compression run (browser, ffmpeg.wasm from CDN)
- [ ] Output MP4 plays and matches target size
