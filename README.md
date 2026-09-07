# Private Video Compressor Research

Research snapshot: **2026-09-07**

A practical comparison of privacy-first, open-source video compressors that process media locally in the browser or can be self-hosted.

## Goal

Find the best open-source alternative to [freevideocompressor.app](https://freevideocompressor.app/) with these priorities:

- Video files should **not be uploaded to a third-party server**.
- Prefer **client-side/browser-local processing**.
- Modern, simple UI.
- Open-source code that can be audited.
- Easy self-hosting on Docker / TrueNAS / HexOS.
- Good control over quality and target file size.
- Prefer active, maintained projects over abandoned demos.

## Bottom line

### Best architecture: VidKit

**Repository:** https://github.com/TondaRuzicka/vidkit

VidKit is the most technically interesting option because it uses a modern browser media pipeline with **WebCodecs + Mediabunny**, and can fall back to **FFmpeg.wasm** where needed.

Why it stands out:

- Browser-local processing.
- Modern codec architecture instead of relying only on FFmpeg compiled to WebAssembly.
- Privacy-oriented automated tests.
- MIT-licensed.
- Good base for a lightweight private compressor.

Main caveat: the project is still relatively small and has less real-world usage than more established alternatives.

### Best ready-to-self-host option: compress.lol

**Repository:** https://github.com/sowahq/compress.lol

A simple, focused client-side compressor with target-size UX and an existing Docker-oriented setup. It is closer to the simplicity of freevideocompressor.app and is easier to deploy without significant redesign.

### Best mature toolbox: ffmpeg-webCLI

**Repository:** https://github.com/tejaswigowda/ffmpeg-webCLI

A much broader browser media toolkit. Mature and feature-rich, but more complex than necessary if the only goal is simple video compression.

## Ranking

| Rank | Project | Privacy | Performance | Maturity | Simplicity | Self-host | Overall |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | VidKit | 5/5 | 5/5 | 3/5 | 5/5 | 4/5 | **9.3/10** |
| 2 | compress.lol | 5/5 | 3/5 | 4/5 | 5/5 | 5/5 | **8.8/10** |
| 3 | ffmpeg-webCLI | 5/5 | 3/5 | 5/5 | 3/5 | 4/5 | **8.5/10** |
| 4 | Compress Pro | 5/5 | 5/5 | 3.5/5 | 3/5 | 4/5 | **8.4/10** |
| 5 | FFmpeg-UI | 5/5 | 4/5 | 3/5 | 3/5 | 4/5 | **7.8/10** |
| 6 | addyosmani/video-compress | 5/5 | 2.5/5 | 3/5 | 5/5 | 4/5 | **7.3/10** |
| 7 | BrowserSnip | 5/5 | 3/5 | 2/5 | 3/5 | 4/5 | **6.9/10** |
| — | PrivateMedia | Unclear | Unclear | 1/5 | 4/5 | Unclear | **Not recommended yet** |

> Scores are qualitative research judgments, not formal benchmarks.

## Important distinction: two kinds of “private”

### Browser-local

```text
Video -> Browser -> Local codec/WASM -> Output
```

The actual video does not need to be uploaded to the web server hosting the application.

### Self-hosted server-side

```text
Video -> Your browser -> Your server -> FFmpeg -> Browser
```

This is still private relative to third parties, but the video **does leave the client device** and travels to your server.

For this project, browser-local processing is preferred.

## Recommended direction

If building a permanent personal service:

1. Start from **VidKit**.
2. Remove all optional analytics/telemetry.
3. Keep the WebCodecs-first pipeline.
4. Use FFmpeg.wasm only as a compatibility fallback.
5. Simplify the UI toward the one-screen workflow used by freevideocompressor.app and addyosmani/video-compress.
6. Provide target-size presets plus an advanced panel.
7. Host the static application behind Nginx/Caddy on Docker/TrueNAS/HexOS.
8. Add automated privacy tests that fail on unexpected network calls.

See [`docs/full-research.md`](docs/full-research.md) for the detailed evaluation.
