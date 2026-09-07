# Next Steps

## Recommended implementation path

1. Fork or clone **VidKit**.
2. Remove optional analytics.
3. Audit every outbound request.
4. Keep WebCodecs as the preferred path.
5. Keep FFmpeg.wasm only as fallback where needed.
6. Redesign the first screen around target file size.
7. Add presets: Small / Balanced / High Quality.
8. Add an advanced panel for CRF/bitrate/resolution/FPS.
9. Package as a static Docker image behind Nginx/Caddy.
10. Add automated privacy tests.
11. Run a browser/format/file-size test matrix.

## Product target

A private, modern compressor that feels as simple as freevideocompressor.app while being fully auditable and self-hostable.
