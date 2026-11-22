# Review: khalas 15s reel (v2, HyperFrames)

## Creative calls
- Two worlds. The problem lives in a messy, full-screen WhatsApp-style chat (beige wallpaper, real bubbles, timestamps). The fix lives in khalas electric blue (#2B3BFF) with yellow and white. No floating cards on an empty background.
- Type: Alexandria 900 (an Arabic face by an Egyptian designer) set on torn tape strips, slightly rotated, landing with a slap. Red rubber stamps and red marker circles carry the "lost" beats. TikTok-style stroked captions highlight each word as it's spoken.
- Transitions, each with a cause: hook → loss is a vertical whip. The loss shots are hard cuts on stamps. Loss → order is a match cut in the same chat. Inside the order scene, blue floods out of the order card. The card then files itself into a list. Order → night is a hard cut. Night chat → lock screen is a blur swap. The lock screen → CTA moves through the khalas app icon, which grows to fill the frame with blue.
- Kept from v1: the voice, the beat and the sound effects, all on the same timings.

## Measured
- `hyperframes check`: 0 errors. The warnings left are kept on purpose: background chat bubbles and notifications scroll past faster than their read time and sit in the platform UI zones as texture, and timestamps are under the 28px floor, as they are in the real app.
- Every headline and caption sits in the shared 9:16 safe zone (y 288–1248). The caption band's bottom edge is at 1248.
- Audio: −12.1 LUFS integrated, no silence. A speech-to-text pass on the final mix returns every line.
- Motion blur is off. The filter tier ghosted the slap entrances, so the moves render crisp.

## Not checked
- Nobody listened to the sound. It was measured and transcribed only.

## Weakest shot / next
- The night chat (9.0–10.6s) has empty dark space under the last message. A "✅ order confirmed" system line or a bigger chat would fill it.
- A native Egyptian voice (paid ElevenLabs plan) would lift the whole piece more than any visual change.
