# Full Research

Research snapshot: **2026-09-07**

This document compares privacy-first video compressors with an emphasis on **browser-local processing**, open-source auditability, modern UX, and practical self-hosting on Docker / TrueNAS / HexOS.

## Evaluation criteria

The ranking prioritizes:

1. Whether the actual video stays on the client device.
2. Whether the source code is publicly auditable.
3. Processing architecture and performance potential.
4. Project maintenance and real-world maturity.
5. UI simplicity for a one-purpose compressor.
6. Ease of self-hosting.
7. Control over quality and target output size.

> Scores in this repository are qualitative research judgments, not formal benchmarks.

---

## 1. freevideocompressor.app

Website: https://freevideocompressor.app/

The site presents itself as a browser-side video compressor using FFmpeg WebAssembly. It states that media is processed locally and is not uploaded for compression. Its privacy-oriented UX is the reference point for this research: select/drop a video, choose compression settings, process locally, download the result.

### Open-source status

No official public repository for the website itself was found during this research. That means the service can be used as a UX reference, but its complete application code cannot be independently audited in the same way as the GitHub projects below.

### Privacy claim

The site states that compression runs client-side and that the actual video is not uploaded for processing. It also describes an offline-capable model after the application/FFmpeg assets are loaded.

### Verdict

**Good UX/privacy reference, but not the preferred foundation because the complete site code was not found as an official public repository.**

---

## 2. VidKit — recommended architecture

Repository: https://github.com/TondaRuzicka/vidkit

### Why it is the strongest technical candidate

VidKit is interesting because it does not treat FFmpeg.wasm as the only possible browser processing engine. Its approach combines modern browser media APIs with a fallback path:

```text
                 +-> WebCodecs / modern browser pipeline
Video -> Browser |
                 +-> FFmpeg.wasm fallback
```

The project uses **WebCodecs-oriented processing + Mediabunny**, with FFmpeg.wasm available where a compatibility fallback is needed.

This is preferable to pushing every operation through a CPU-heavy WebAssembly FFmpeg build when the browser can handle common codecs more directly.

### Notable strengths

- Client-side processing model.
- Modern WebCodecs-oriented architecture.
- Uses Mediabunny in its media pipeline.
- FFmpeg.wasm remains available as a compatibility fallback.
- MIT license.
- Includes automated privacy-oriented testing.
- Good foundation for a focused, modern compressor.
- Target-size-friendly UX direction.
- Recent project activity was observed during the research snapshot.

### Privacy testing

A particularly strong point is the existence of automated browser tests intended to detect unwanted network behavior. The project has used Playwright-based privacy checks around network requests and browser storage while exercising actual media processing.

The test strategy includes ideas such as:

- Observe network requests while compression runs.
- Reject unexpected external hosts.
- Reject outbound request bodies containing file data.
- Exercise both normal media paths and FFmpeg fallback paths.
- Check cookies.
- Check `localStorage`.
- Check `sessionStorage`.

This is substantially stronger than relying only on a README statement such as “your files never leave your device.”

### Analytics caveat

The project has used **Umami-style cookieless analytics** for page-level analytics. This is not the same thing as uploading the video, but for a personal private deployment it is unnecessary.

Recommended action: **remove analytics entirely**.

Then the server is responsible only for serving static HTML/JS/WASM assets; the video can remain on the user's device.

### Dependency / architecture note

During the research snapshot, VidKit used the modern `@ffmpeg/ffmpeg` 0.12 generation and a current browser-media stack rather than the older FFmpeg.wasm generation used by some historical demos.

### Main weakness

VidKit is comparatively small. Its architecture is attractive, but it has less community validation and long-term battle testing than the more established FFmpeg browser projects.

### Verdict

**Best base if the goal is to build the cleanest long-term private compressor.**

---

## 3. compress.lol — recommended ready-to-deploy option

Repository: https://github.com/sowahq/compress.lol

### Why it is attractive

This project is much closer to the intended product shape than a general video editor:

> Drop a video -> choose target size -> compress -> download.

### Strengths

- Focused specifically on compression.
- Client-side FFmpeg.wasm processing model.
- Simple target-size workflow.
- Modern FFmpeg.wasm generation compared with older browser demos.
- Docker/self-hosting friendly.
- Open-source and easy to inspect.
- More community exposure than the smallest alternatives.

### Privacy model

The important architecture is:

```text
Browser -> FFmpeg.wasm -> Download
```

rather than:

```text
Browser -> Your server -> FFmpeg -> Browser
```

So self-hosting can still mean the web server only serves the application; the actual media file does not have to travel to the server.

### Community / real-world caveats

Real-world feedback around compress.lol and similar FFmpeg.wasm workloads highlights the practical limits of browser-side transcoding:

- 4K transcodes can be slow.
- Memory use can be high.
- Mobile browsers can struggle on larger jobs.
- Progress can appear stalled on some browser/device combinations.
- Target-size estimation can be imperfect in edge cases.
- Self-hosting threaded FFmpeg.wasm can fail if cross-origin isolation / SharedArrayBuffer headers are missing.

These issues do not necessarily indicate poor project quality; several are consequences of running a full transcoder inside a browser sandbox.

### Large-file limit

The project/documentation has historically warned about browser/WASM practical limits around very large inputs. Treat multi-gigabyte files as a stress case rather than the default browser workflow.

### Verdict

**Best choice when the priority is “deploy something simple now” rather than redesigning the processing architecture.**

---

## 4. ffmpeg-webCLI — strongest mature browser toolbox

Repository: https://github.com/tejaswigowda/ffmpeg-webCLI

### Strengths

- Broad feature set.
- Compression.
- Conversion.
- Trim.
- Resize.
- GIF workflows.
- Audio tools.
- Subtitle operations.
- Batch/power-user workflows.
- Raw FFmpeg-style operations.
- PWA/offline-friendly design.
- Uses workers to reduce UI blocking.
- More established than the smallest alternatives.

### Maturity

This is one of the more visible and community-tested browser FFmpeg projects in the shortlist, with recent major-version work observed during the research snapshot and public technical discussion around it.

### Weaknesses for this use case

The problem is not capability but scope. It is a media toolbox rather than a deliberately minimal compressor.

For a service intended to feel like freevideocompressor.app, much of the interface and feature surface is unnecessary.

### Performance caveat

Like other FFmpeg.wasm-first solutions, it remains constrained by browser memory and WebAssembly performance versus native FFmpeg. Large 4K workloads are not its ideal use case.

### Verdict

**Excellent reference or power-user option, but not the cleanest base for a one-purpose compressor.**

---

## 5. Compress Pro

Repository: https://github.com/Scorpio3310/compress-pro

### Why it is interesting

Compress Pro is broader than video and includes other local compression tools. Its engineering approach is notable because it uses modern browser capabilities and workers rather than assuming everything must be processed through FFmpeg.wasm.

### Strengths

- Modern browser processing ideas.
- WebCodecs usage where applicable.
- Worker-based processing.
- Supports multiple media/document utility categories.
- MIT-licensed.
- Automated testing focus.
- Build transparency/provenance ideas.

### Build provenance

A useful engineering idea in the project is exposing build information such as build date / commit identity so a deployed version can be related back to its source revision.

### Weakness

It is much broader than the requirement. Images, PDFs, archives, fonts and other utilities create unnecessary product surface if the objective is simply “private video compressor.”

### Verdict

**Strong architecture reference; less attractive as the final product UI.**

---

## 6. FFmpeg-UI

Repository: https://github.com/bennypepper/FFmpeg-UI

### Why it matters

This project is worth keeping on the shortlist because it represents a different path: use a native/local FFmpeg environment instead of forcing everything through browser WebAssembly.

For multi-gigabyte 4K video, native FFmpeg is often the more practical architecture.

### When to prefer native/local FFmpeg

Use a native desktop/Tauri-style solution when priorities are:

- Very large videos.
- Long 4K files.
- Maximum encode speed.
- Hardware acceleration.
- Fewer browser memory constraints.

### Verdict

**Better than browser-only solutions for serious large-file transcoding, but not as frictionless as a web app.**

---

## 7. addyosmani/video-compress

Repository: https://github.com/addyosmani/video-compress

### What it gets right

Its UI and controls are very close to the desired product:

- Target file size.
- CRF / quality controls.
- Target bitrate.
- Resolution controls.
- FPS controls.
- Codec choices.
- Preview-oriented workflow.

### Why the recommendation changed

This was initially the strongest-looking candidate because its UX is excellent for the task. Deeper inspection changed the recommendation.

The project has historically used an **older FFmpeg.wasm generation** than newer alternatives. Issue reports have also included format-specific failures such as MOV compression problems.

So the UI remains a useful reference, but the underlying implementation is not the best architecture to adopt unchanged for a new 2026 build.

### Verdict

**Excellent UX reference. Prefer VidKit's architecture with an Addy-style interface.**

---

## 8. BrowserSnip

Repository: https://github.com/ningtoba/BrowserSnip

### Strengths

- Client-side media operations.
- Useful collection of video tools.
- Open-source.
- Simple utility concept.
- Uses a modern FFmpeg.wasm generation compared with older examples.

### Weaknesses

- Smaller community footprint.
- Browser/WASM performance limitations remain.
- Documentation acknowledges that browser WASM processing can be dramatically slower than native FFmpeg.
- Practical file-size guidance is more conservative than what would be ideal for a general-purpose compressor.
- Less compelling than VidKit for architecture or compress.lol for focused deployment.

### Verdict

**Legitimate option, but no clear reason to prefer it over the top recommendations.**

---

## 9. PrivateMedia

Repository: https://github.com/kopivo/PrivateMedia

### Concern

This initially looked appealing because the description emphasized local/private media processing and a large tool set.

Deeper inspection reduced confidence. During the research snapshot, the repository appeared much less complete and battle-tested than its presentation suggested, with very little community validation.

### Verdict

**Do not use as the primary base until the source tree, maintenance quality, release process and real-world usage are substantially clearer.**

---

# Browser-local vs self-hosted server-side

These are not the same privacy model.

## Browser-local

```text
Video -> Browser -> Local codec/WASM -> Output
```

The web server provides the application code, but the video itself does not have to leave the computer doing the compression.

## Self-hosted server-side

```text
Video -> Browser -> Your server -> Native FFmpeg -> Browser
```

This is still private relative to third parties, but the video leaves the client device and is transferred to your own server.

For this project, **browser-local is preferred** unless very large-file performance requires a server/native path.

---

# WebAssembly vs WebCodecs

This distinction is one of the most important findings.

## FFmpeg.wasm-first model

```text
Video
  |
Browser
  |
FFmpeg compiled to WebAssembly
  |
CPU-heavy processing
  |
Output
```

### Benefits

- Strong privacy model.
- Huge FFmpeg feature compatibility.
- Easy static hosting.
- Works without uploading media to a server.

### Costs

- High RAM usage.
- Slower than native FFmpeg in many workloads.
- Browser memory constraints.
- Large-file and 4K pain points.
- Hardware acceleration is harder / less consistent than native encoders.
- Multi-threaded WASM can require correct COOP/COEP headers and SharedArrayBuffer support.

## WebCodecs-first model

```text
                 +-> WebCodecs / browser codec path
Video -> Browser |
                 +-> FFmpeg.wasm fallback
```

### Benefits

- More modern use of browser-native media capabilities.
- Potentially lower overhead.
- Better long-term architecture for common supported codecs.
- Better opportunity to benefit from optimized/native browser codec paths.
- FFmpeg remains available only where compatibility is needed.

### Recommendation

For a new build, prefer **WebCodecs-first + FFmpeg fallback** rather than **FFmpeg.wasm for everything**.

---

# Recommended ranking

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

---

# Final proposed product

The ideal private compressor would combine the best pieces of multiple projects.

## From VidKit

- Modern WebCodecs-first processing.
- FFmpeg.wasm fallback compatibility.
- Automated privacy tests.

## From addyosmani/video-compress

- Clear quality controls.
- Friendly preview.
- Advanced options hidden behind a simple first screen.

## From compress.lol

- Target file size as the primary workflow.
- Very simple “drop -> compress -> download” experience.

## Suggested UI

```text
+--------------------------------+
|                                |
|        Drop video here         |
|                                |
| Original size: 387 MB          |
|                                |
| Target: [ 50 MB ]              |
|                                |
| Quality:  Balanced             |
|                                |
|       [ Compress ]             |
|                                |
+--------------------------------+
```

Optional advanced panel:

- Codec.
- Resolution.
- Frame rate.
- Quality / CRF.
- Bitrate.
- Audio quality.
- Strip metadata.

---

# Deployment recommendation for TrueNAS / HexOS

Serve the application as static assets behind Nginx/Caddy in Docker:

```text
TrueNAS / HexOS
   |
Docker
   |
Nginx / Caddy
   |
Static HTML / JS / WASM
   |
Browser downloads application
   |
Video remains on the client device
```

Recommended hardening:

- Remove analytics.
- Self-host JS/WASM assets.
- Self-host fonts/icons.
- Add a strict Content-Security-Policy.
- Configure COOP/COEP if SharedArrayBuffer is required.
- Use HTTPS.
- Pin versions.
- Add automated privacy tests that fail on unexpected outbound requests.

---

# Large-file rule

If the expected workflow regularly includes **5–20 GB 4K videos**, do not optimize around FFmpeg.wasm.

Use native FFmpeg or a desktop wrapper with native codecs and hardware acceleration.

Browser-local processing is ideal for convenience and privacy, but native video pipelines remain the stronger choice for very large workloads.

---

# Final recommendation

## If building the best long-term personal service

**Start from VidKit**, remove analytics, retain the WebCodecs-first architecture, keep FFmpeg.wasm as fallback, and simplify the UI around target size.

## If deploying something immediately

**Use compress.lol** as the first ready-to-self-host candidate, then validate it with MP4/MOV, multiple browsers, target-size accuracy, and large-file stress tests.

## If the files are routinely huge

Use **native FFmpeg / a desktop-native wrapper** instead of browser-only WASM.
