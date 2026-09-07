# Privacy & Security Checklist

Use this checklist before deploying any candidate.

## Required

- [ ] Video processing stays client-side.
- [ ] No file upload endpoint exists in the normal compression path.
- [ ] No analytics SDK receives file metadata.
- [ ] No telemetry event includes file name, duration, codec, resolution or target size unless explicitly desired.
- [ ] No third-party CDN is required after deployment.
- [ ] Fonts/assets are self-hosted.
- [ ] FFmpeg/WebAssembly assets are self-hosted.
- [ ] CSP restricts unexpected outbound connections.
- [ ] COOP/COEP headers are configured correctly when SharedArrayBuffer is required.
- [ ] Application works after initial load with WAN disconnected where feasible.

## Automated privacy test idea

A Playwright test should:

1. Load the application.
2. Record all network requests.
3. Import a test video.
4. Run compression.
5. Download the result.
6. Fail if an unexpected host is contacted.
7. Fail if outbound request bodies contain file bytes or sensitive file metadata.
8. Inspect localStorage/sessionStorage/cookies for unnecessary tracking state.

## Recommended production policy

For a personal deployment, remove analytics entirely. A private utility does not need page-view tracking.
