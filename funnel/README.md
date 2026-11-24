# khalas outreach funnel

```
Email 1 (day 0) ──► Email 2 (day 3) ──► Email 3 (day 7)
        │                 │                  │
        └──────── link ───┴──────────────────┘
                          ▼
              start.html  (3 easy steps)
      1. pick plan  →  2. name, brand, WhatsApp  →  3. reserve for 99 EGP
```

| Piece | File |
|---|---|
| Checkout page, 3 steps, Arabic/English | `../start.html` (served at `https://alielmarghany.github.io/khalas/start.html`) |
| Email copy, Egyptian Arabic | `emails/ar/1.txt`, `2.txt`, `3.txt` |
| Email copy, English | `emails/en/1.txt`, `2.txt`, `3.txt` |
| Sender (throttled, dry run by default) | `send.py` |
| Lead list format | `leads.example.csv` |

Every link carries `?ref=<lead id>&utm_content=step<N>`, so you can tell which company and which email converted.

## 1. Build the list (1,000 companies)

Copy `leads.example.csv` to `leads.csv`. Columns: `id,email,first_name,company,lang` (`lang` is `ar` or `en`; `first_name` may be empty).

Use addresses that companies **publish for business contact** (their website, Facebook/Instagram page, Google Maps listing), or that you got from a source that permits this use. Don't buy scraped lists: they bounce, get your domain blacklisted, and may break Egypt's Personal Data Protection Law (151/2020) and GDPR/CAN-SPAM for non-Egyptian recipients.

`leads.csv`, `suppress.csv`, `state/` and `outbox/` are git-ignored: contact data never goes into this public repo.

## 2. Set up sending

Don't send from a personal Gmail: it caps at ~500/day and cold volume will flag the account. Use a separate domain or subdomain (e.g. `hello@getkhalas.com`) with **SPF, DKIM and DMARC** set, and an SMTP provider such as Brevo, Zoho Mail, Amazon SES, Mailgun or Google Workspace. Warm the address up for 1–2 weeks (start at 20–30/day).

```bash
export SMTP_HOST=smtp-relay.brevo.com SMTP_PORT=587
export SMTP_USER=... SMTP_PASS=...            # from your provider, never commit these
export FROM_EMAIL=ali@yourdomain.com FROM_NAME="Ali from khalas"
export REPLY_TO=ali@yourdomain.com
export POSTAL_ADDRESS="Elmarghany Enterprises, <street>, Cairo, Egypt"   # required by anti-spam law
```

## 3. Run it daily

```bash
python3 funnel/send.py                 # dry run: shows what's due, writes previews to funnel/outbox/
python3 funnel/send.py --send          # sends up to 100, 25–70 s apart
python3 funnel/send.py --status        # funnel numbers
```

At 100/day, 1,000 companies get email 1 in about 10 days, and the whole sequence finishes in about 3 weeks. Follow-ups always go before new leads. Raise `--daily-cap` only once your domain is warmed up and bounces stay under 2%.

## 4. Stop people who said no (or yes)

Add an address to `suppress.csv` (`email,reason`) when someone replies "unsubscribe"/"إلغاء", replies at all, or reserves a spot. Hard bounces are added automatically. Check replies every day: a reply is your warmest lead, so answer it by hand.

## 5. Make step 3 even smoother (optional, in `start.html` CONFIG)

- `FORM_PREFILL`: Google Form editor → ⋮ → *Get pre-filled link* → paste each `entry.NNNN` id so the name, brand, WhatsApp, plan and `ref` typed in step 2 carry into the form (no typing twice; `ref` lets you attribute reservations to emails).
- `PAY_URL`: a direct Paymob / Fawry / InstaPay payment link for 99 EGP. When set, step 3 goes straight to payment instead of the form.
- `CONTACT_WHATSAPP`: shows a "Confirm on WhatsApp" button with the order details prefilled.

## What to measure

| Stage | Healthy cold-email range |
|---|---|
| Delivered (not bounced) | > 97% |
| Replies | 2–8% |
| Click to `start.html` | 3–10% |
| Reserved (99 EGP) | 0.5–3% of emailed |

From 1,000 companies, expect roughly 5–30 reservations from email alone. Answering replies quickly is what moves that number most.
