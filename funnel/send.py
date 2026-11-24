#!/usr/bin/env python3
"""khalas outreach sender: a 3-email sequence to a list of companies, sent slowly and safely.

Dry run by default (writes previews to funnel/outbox/). Add --send to really send.

    python3 funnel/send.py                 # preview what would go out today
    python3 funnel/send.py --send          # send today's batch
    python3 funnel/send.py --status        # funnel numbers so far

Run it once a day (by hand or cron). Each run sends whatever is due:
  step 1 to new leads, step 2 three days after step 1, step 3 four days after step 2,
  up to --daily-cap emails, skipping anyone in suppress.csv.

SMTP settings come from environment variables (see funnel/README.md):
  SMTP_HOST SMTP_PORT SMTP_USER SMTP_PASS FROM_EMAIL FROM_NAME REPLY_TO POSTAL_ADDRESS BASE_URL
"""
import argparse, csv, os, random, re, smtplib, ssl, sys, time
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
LEADS = HERE / "leads.csv"
SUPPRESS = HERE / "suppress.csv"
STATE = HERE / "state" / "sent.csv"
OUTBOX = HERE / "outbox"
EMAILS = HERE / "emails"

# Days to wait after the previous step before sending the next one.
SCHEDULE = {1: 0, 2: 3, 3: 4}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")

FOOTER = {
    "ar": "\n\n--\nلو مش عايز إيميلات تانية مننا، رد بكلمة \"إلغاء\" ومش هنبعتلك تاني.\n{postal_address}\n",
    "en": "\n\n--\nDon't want more emails from us? Reply \"unsubscribe\" and we won't write again.\n{postal_address}\n",
}


def now():
    return datetime.now(timezone.utc)


def read_csv(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_leads():
    if not LEADS.exists():
        sys.exit(f"No {LEADS.relative_to(HERE.parent)} found. Copy leads.example.csv to leads.csv and fill it in.")
    seen, leads, bad = set(), [], 0
    for i, row in enumerate(read_csv(LEADS), 1):
        email = (row.get("email") or "").strip().lower()
        if not EMAIL_RE.match(email):
            bad += 1
            continue
        if email in seen:
            continue
        seen.add(email)
        lang = (row.get("lang") or "ar").strip().lower()
        leads.append({
            "id": (row.get("id") or "").strip() or f"L{i:04d}",
            "email": email,
            "first_name": (row.get("first_name") or "").strip(),
            "company": (row.get("company") or "").strip(),
            "lang": lang if lang in ("ar", "en") else "ar",
        })
    if bad:
        print(f"! skipped {bad} rows with a missing or invalid email")
    return leads


def load_suppressed():
    return {(r.get("email") or "").strip().lower() for r in read_csv(SUPPRESS)}


def load_state():
    """email -> (last_step, last_sent_at)"""
    st = {}
    for r in read_csv(STATE):
        step, at = int(r["step"]), datetime.fromisoformat(r["sent_at"])
        if r["email"] not in st or step > st[r["email"]][0]:
            st[r["email"]] = (step, at)
    return st


def record(email, lead_id, step):
    STATE.parent.mkdir(exist_ok=True)
    new = not STATE.exists()
    with STATE.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["email", "id", "step", "sent_at"])
        w.writerow([email, lead_id, step, now().isoformat(timespec="seconds")])


def due_step(email, state):
    if email not in state:
        return 1
    last, at = state[email]
    nxt = last + 1
    if nxt in SCHEDULE and now() - at >= timedelta(days=SCHEDULE[nxt]):
        return nxt
    return None


def template(lang, step):
    raw = (EMAILS / lang / f"{step}.txt").read_text(encoding="utf-8")
    first, body = raw.split("\n", 1)
    assert first.startswith("Subject:"), f"{lang}/{step}.txt must start with 'Subject:'"
    return first[len("Subject:"):].strip(), body.lstrip("\n")


def build(lead, step, cfg):
    subject, body = template(lead["lang"], step)
    fallback = {"ar": ("أهلاً", "البراند بتاعك"), "en": ("there", "your brand")}[lead["lang"]]
    link = cfg["base_url"] + "?" + urlencode({
        "ref": lead["id"], "lang": lead["lang"], "plan": "growth",
        "utm_source": "email", "utm_medium": "outreach", "utm_campaign": "founding", "utm_content": f"step{step}",
    })
    fields = {"first_name": lead["first_name"] or fallback[0], "company": lead["company"] or fallback[1], "link": link}
    if not lead["first_name"]:  # "أهلاً أهلاً" / "Hi there," reads oddly in the greeting otherwise
        body = body.replace("أهلاً {first_name}،", "أهلاً،").replace("Hi {first_name},", "Hi,")
        subject = subject.replace("{first_name}، ", "").replace("{first_name}, ", "")
        subject = subject[:1].upper() + subject[1:]
    subject, body = subject.format(**fields), body.format(**fields)
    body += FOOTER[lead["lang"]].format(postal_address=cfg["postal_address"])

    msg = EmailMessage()
    msg["From"] = formataddr((cfg["from_name"], cfg["from_email"]))
    msg["To"] = lead["email"]
    msg["Subject"] = subject
    msg["Reply-To"] = cfg["reply_to"]
    msg["Message-ID"] = make_msgid(domain=cfg["from_email"].split("@")[-1])
    msg["List-Unsubscribe"] = f"<mailto:{cfg['reply_to']}?subject=unsubscribe>"
    msg.set_content(body)
    return msg


def config(sending):
    e = os.environ.get
    cfg = {
        "host": e("SMTP_HOST", ""), "port": int(e("SMTP_PORT", "587")),
        "user": e("SMTP_USER", ""), "password": e("SMTP_PASS", ""),
        "from_email": e("FROM_EMAIL", e("SMTP_USER", "you@example.com")),
        "from_name": e("FROM_NAME", "Ali from khalas"),
        "postal_address": e("POSTAL_ADDRESS", ""),
        "base_url": e("BASE_URL", "https://alielmarghany.github.io/khalas/start.html"),
    }
    cfg["reply_to"] = e("REPLY_TO", cfg["from_email"])
    if sending:
        missing = [k for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASS", "POSTAL_ADDRESS") if not e(k)]
        if missing:
            sys.exit("Missing settings for --send: " + ", ".join(missing) + " (see funnel/README.md)")
    return cfg


def status(leads, state, suppressed):
    by_step = {1: 0, 2: 0, 3: 0}
    for em, (step, _) in state.items():
        by_step[step] = by_step.get(step, 0) + 1
    print(f"leads: {len(leads)} | suppressed: {len(suppressed)} | never emailed: {sum(1 for l in leads if l['email'] not in state)}")
    for s in (1, 2, 3):
        print(f"  finished at step {s}: {by_step.get(s, 0)}")
    print("Reservations: count rows in the waitlist sheet; the 'ref' column / utm_content shows which email converted.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--send", action="store_true", help="really send (default is a dry run)")
    ap.add_argument("--daily-cap", type=int, default=100, help="max emails this run (default 100)")
    ap.add_argument("--min-delay", type=float, default=25, help="min seconds between emails")
    ap.add_argument("--max-delay", type=float, default=70, help="max seconds between emails")
    ap.add_argument("--status", action="store_true", help="print funnel numbers and exit")
    args = ap.parse_args()

    leads, suppressed, state = load_leads(), load_suppressed(), load_state()
    if args.status:
        return status(leads, state, suppressed)

    cfg = config(args.send)
    queue = []
    for lead in leads:
        if lead["email"] in suppressed:
            continue
        step = due_step(lead["email"], state)
        if step:
            queue.append((lead, step))
    # Follow-ups first (they're time-sensitive), then new leads.
    queue.sort(key=lambda x: -x[1])
    queue = queue[: args.daily_cap]
    print(f"{len(queue)} emails due now (cap {args.daily_cap}): "
          + ", ".join(f"step {s}: {sum(1 for _, x in queue if x == s)}" for s in (1, 2, 3)))

    if not args.send:
        OUTBOX.mkdir(exist_ok=True)
        for lead, step in queue[:20]:
            (OUTBOX / f"{lead['id']}-step{step}.eml").write_bytes(bytes(build(lead, step, cfg)))
        print(f"Dry run. Previews of the first {min(20, len(queue))} written to {OUTBOX.relative_to(HERE.parent)}/. Add --send to send.")
        return

    ctx = ssl.create_default_context()
    smtp = smtplib.SMTP(cfg["host"], cfg["port"], timeout=60)
    smtp.starttls(context=ctx)
    smtp.login(cfg["user"], cfg["password"])
    sent = failed = 0
    try:
        for i, (lead, step) in enumerate(queue):
            try:
                smtp.send_message(build(lead, step, cfg))
                record(lead["email"], lead["id"], step)
                sent += 1
                print(f"  sent step {step} -> {lead['email']}")
            except smtplib.SMTPRecipientsRefused:
                failed += 1
                with SUPPRESS.open("a", encoding="utf-8") as f:  # bounced address: never retry
                    if SUPPRESS.stat().st_size == 0:
                        f.write("email,reason\n")
                    f.write(f"{lead['email']},bounced\n")
                print(f"  refused -> {lead['email']} (added to suppress.csv)")
            except smtplib.SMTPServerDisconnected:
                smtp = smtplib.SMTP(cfg["host"], cfg["port"], timeout=60)
                smtp.starttls(context=ctx)
                smtp.login(cfg["user"], cfg["password"])
            if i < len(queue) - 1:
                time.sleep(random.uniform(args.min_delay, args.max_delay))
    finally:
        try:
            smtp.quit()
        except Exception:
            pass
    print(f"Done: {sent} sent, {failed} refused.")


if __name__ == "__main__":
    main()
