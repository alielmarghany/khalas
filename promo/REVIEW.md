# Khalas promo, vertical: review notes

1080×1920 · 30 fps · 45.5 s · English voiceover, music and sound effects · rendered to `../renders/khalas-promo-vertical.mp4`

## Current version

**Intro (0–10.5 s, `compositions/intro.html`).** It replaces the old WhatsApp-flood hook and the "Copy. Paste. Mistake." scene, and borrows the storytelling mechanics of the person's reference clip:
1. A card says "37 orders".
2. "WRONG." slams in and shatters the card into shards ("it's lying to you").
3. An iris opens onto paper.
4. A yellow order-blob drops in at 37.
5. Three critters bite it, each bite landing on the spoken number:
   - Missed replies −7
   - Typos −5
   - Lost addresses −3
6. The blob melts on "You actually shipped 22".
7. Everything after the intro moved back by 0.5 s.

**Intro sounds.** `glass-shatter.mp3` and `cartoon-bite.mp3` are CC0 from Freesound; see `assets/sfx/CREDITS.md`.

**Language.** Everything on screen is English-first:
- English lines are big, in Bricolage Grotesque 800.
- Each has a small Egyptian Arabic line underneath, in IBM Plex Sans Arabic.
- The customer chats, spreadsheet, order card and board labels stay in Egyptian Arabic, so the story still reads as Egyptian sellers.

**Voice.** ElevenLabs "Laura" (a free built-in, energetic social-media voice), model `eleven_v3`, with the `[excited]` tag and stability 0:
- 26 short phrase clips (`assets/voice/v01–v26.mp3`), each placed on its animation beat.
- Pauses inside each clip are capped at 0.12 s, and a few clips are sped up 10–30% to fit their slots.
- Earlier Jessica takes are not kept in the project.

**Music.** `assets/bgm/khalas-bed.mp3`:
- Cut from HeyGen music-library track 7ffd6fe7, starting 4.5 s in.
- Plays at volume 0.3 under the voice.

**Sound effects.** 37 cues from the bundled HyperFrames library. Each one's peak is placed one frame after the thing on screen it belongs to.

**Layout.** Centred on x = 540. Some text on the right now runs under TikTok's action buttons; that's the trade-off the person chose.

## Measured

- `check`: 0 errors.
- Delivery file: −15.5 LUFS, true peak −1.3 dBTP, no clipping.
- The mix was normalised with ffmpeg `loudnorm` after rendering, because the raw render was −18 LUFS.
- The sound was measured, not listened to.

## Remaining warnings and notes

- `outside_safe_zone` (TikTok right edge): a result of centring the layout.
- `line_unread` on the 99+ and 400 counters: only the final number needs to be read.
- The Arabic accent lines hold briefly in a few places. They are secondary text.
- The render tool doesn't normalise loudness itself. Re-renders need the same `loudnorm` pass, or higher clip volumes.
