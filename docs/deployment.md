# Deployment Notes — Docker / TrueNAS / HexOS

## Preferred architecture

Host only the static application on the server.

```text
TrueNAS / HexOS
   |
Docker
   |
Nginx or Caddy
   |
Static HTML / JS / WASM
   |
Browser downloads app
   |
Video remains on client device
```

The server should not receive the video file during compression.

## Important headers for threaded WebAssembly

Some FFmpeg.wasm configurations require cross-origin isolation / SharedArrayBuffer.

Typical headers:

```nginx
add_header Cross-Origin-Opener-Policy same-origin always;
add_header Cross-Origin-Embedder-Policy require-corp always;
```

Exact requirements depend on the implementation and external assets.

## Recommended deployment hardening

- Self-host JS/WASM bundles.
- Self-host fonts/icons.
- Disable analytics.
- Use a strict Content-Security-Policy.
- Avoid third-party script tags.
- Put the service behind HTTPS.
- Pin application versions rather than using floating `latest` dependencies in production.
- Test Chrome, Firefox and mobile browsers separately.

## Validation test matrix

Before relying on the service, test:

| Input | Browser | Expected |
|---|---|---|
| MP4 100 MB | Chrome desktop | Pass |
| MP4 500 MB | Chrome desktop | Pass |
| MOV 500 MB | Chrome desktop | Pass/fallback |
| MP4 1 GB | Chrome desktop | Stress test |
| MP4 100 MB | Firefox desktop | Pass |
| MP4 100 MB | Android Chrome | Pass |
| 4K clip | Chrome desktop | Performance test |

Also verify:

- Target-size accuracy.
- Peak RAM usage.
- Whether the tab remains responsive.
- Whether cancelling a job releases memory.
- Whether processing still succeeds after internet access is disconnected.
