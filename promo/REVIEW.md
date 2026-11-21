# Khalas promo, vertical: review notes

1080×1920 · 30 fps · 45 s · English voiceover, music and sound effects · rendered to `../renders/khalas-promo-vertical.mp4`

## Current version

**Language.** Everything on screen is English-first:
- English lines are big, in Bricolage Grotesque 800.
- Each has a small Egyptian Arabic line underneath, in IBM Plex Sans Arabic.
- The customer chats, spreadsheet, order card and board labels stay in Egyptian Arabic, so the story still reads as Egyptian sellers.

**Voice.** ElevenLabs "Liam" (a free built-in voice), model `eleven_v3`, one file per line in `assets/voice/vo01–vo09.mp3`:
- The text animations are re-timed to land on the spoken words.
- `vo02` has its long pause before "Mistake" trimmed to 0.3 s.
- No Egyptian voices: ElevenLabs' free plan doesn't allow them through the API.

**Music.** `assets/bgm/khalas-bed.mp3`:
- Cut from HeyGen music-library track 7ffd6fe7, starting 4.5 s in.
- Plays at volume 0.3 under the voice.

**Sound effects.** 37 cues from the bundled HyperFrames library. Each one's peak is placed one frame after the thing on screen it belongs to.

**Layout.** Centred on x = 540. Some text on the right now runs under TikTok's action buttons; that's the trade-off the person chose.

## Measured

- `check`: 0 errors.
- Delivery file: −14.8 LUFS, true peak −0.7 dBTP, no clipping.
- The mix was normalised with ffmpeg `loudnorm` after rendering, because the raw render was −18 LUFS.
- The sound was measured, not listened to.

## Remaining warnings and notes

- `outside_safe_zone` (TikTok right edge): a result of centring the layout.
- `line_unread` on the 99+ and 400 counters: only the final number needs to be read.
- The Arabic accent lines hold briefly in a few places. They are secondary text.
- The render tool doesn't normalise loudness itself. Re-renders need the same `loudnorm` pass, or higher clip volumes.
