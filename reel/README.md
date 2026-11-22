# khalas: 15s vertical reel (Egyptian Arabic)

`khalas-reel-15s.mp4`: 1080x1920, 30fps, H.264 + AAC, 15.0s, −12 LUFS.

## Visuals: `hf/` (HyperFrames project)
- `hf/index.html` mounts one scene per file in `hf/compositions/`: hook, loss, order, night, cta, plus captions. It also places the voice, music and SFX tracks.
- Shared design tokens live in `hf/compositions/_base.css`. After editing that file, run `python3 inline-base.py` in `hf/` to copy it into every scene.
- Preview: `npx hyperframes preview` · check: `npx hyperframes check` · render: `npx hyperframes render -q delivery --page-motion-blur off -o ../khalas-reel-15s.mp4`
- Notes on the creative calls and known weak spots: `hf/REVIEW.md`.

## Audio: `src/audio/`
- `music.py` synthesizes the beat (128 BPM, maqsoum darbuka, hijaz riff).
- `stems.py` writes the timed voice clips, the music ducked under the voice, and the SFX stem into `hf/assets/audio/`.
- Voice: ElevenLabs v3, stock voice "Liam". SFX: ElevenLabs sound generation.

Fonts (SIL OFL): Alexandria, IBM Plex Sans Arabic, Aref Ruqaa, Bricolage Grotesque, Inter.
