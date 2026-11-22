# khalas: 15s vertical reel (Egyptian Arabic)

`khalas-reel-15s.mp4`: 1080x1920, 30fps, H.264 + AAC, 15.0s, about −13 LUFS.

Rebuild:
1. `cd src && node snap.js all` renders `frames/` from `reel.html`, where `render(t)` sets each frame from the time `t`.
2. `cd src/audio && python3 music.py && python3 mix.py` makes the beat, then mixes in the voice, the sound effects and the music, which ducks under the voice.
3. `ffmpeg -framerate 30 -i frames/f%04d.jpg -i audio/mix.wav -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4`

Voice: ElevenLabs v3, stock voice "Liam", Egyptian Arabic script. Sound effects: ElevenLabs sound generation. Music: synthesized in numpy (128 BPM, maqsoum darbuka, hijaz riff).
Fonts: Lalezar, Cairo, IBM Plex Sans Arabic, Inter, Bricolage Grotesque (all SIL OFL).
