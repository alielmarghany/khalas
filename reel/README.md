# khalas: 15s vertical reel (English)

`khalas-reel-15s.mp4` (English voice and text, centered layout): 1080x1920, 30fps, H.264 + AAC, 15.0s, −12 LUFS.

## Visuals: `hf/` (HyperFrames project, v3)
- `hf/compositions/stage.html`: the 3D phone scene (Three.js, vendored in `hf/assets/lib/`). The camera, lights and the live screen UI are all functions of time.
- `hf/compositions/type.html` (headlines) and `captions.html`. `hf/index.html` mounts them and places the voice, music and SFX.
- Preview: `npx hyperframes preview` · check: `npx hyperframes check` · render: `npx hyperframes render -q delivery -o ../khalas-reel-15s.mp4` (about 7 min on CPU)
- The v2 scenes are kept in `hf-v2-archive/`.
- Notes on the creative calls and known weak spots: `hf/REVIEW.md`.

## Audio: `src/audio/`
- `music.py` synthesizes the beat (128 BPM, maqsoum darbuka, hijaz riff).
- `stems_v3.py` writes the timed voice clips (`v3/`), the music ducked under the voice, and the SFX stem into `hf/assets/audio/`.
- Voice: ElevenLabs v4, stock voice "Chris" (male), in English; takes in `src/audio/v3/en/` (Arabic takes in `v3/chris/` and `v3/`). SFX: ElevenLabs sound generation. `voice-samples.mp3` holds the 8-voice comparison.

Fonts (SIL OFL): Alexandria, IBM Plex Sans Arabic, Aref Ruqaa, Bricolage Grotesque, Inter.

`khalas-reel-15s-ar.mp4`: the Arabic cut, with the same centered 3D film, Arabic headlines, captions and phone screens, and the Arabic male voice (Chris). Its HyperFrames project is `hf-ar/`; its audio is built with `VOICE=v3/chris OUT=…/hf-ar/assets/audio/ python3 src/audio/stems_v3.py`.
