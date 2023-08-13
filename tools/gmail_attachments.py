from simplegmail import Gmail
from simplegmail.query import construct_query
from pathlib import Path
import re
from dateutil import parser  # type: ignore
from tqdm import tqdm
from os.path import splitext


gmail = Gmail(client_secret_file="_creds/client_secret.json", creds_file="_creds/gmail_token.json")
sender_mail_rgx = re.compile(r".* <(?P<mail>.+)>|(?P<mailonly>.+)")
filename_rgx = re.compile(r"[^a-zA-Z0-9-_äöüÄÖÜß]")


# after is inclusive, before is exclusive
query = {
    "attachment": True,
    "before": "2020/01/01",
    # "after": "2020/01/01",
    "exclude_spec_attachment": [["ics"], ["smime.p7s"], ["asc"], ["OpenPGP_signature"]],
}
msgs = gmail.get_messages(query=construct_query(query), attachments="reference", include_spam_trash=False)

print(f"Found {len(msgs)} messages with attachments")

out_path = Path("_out/gmail/")
out_path.mkdir(exist_ok=True)


errors = []
total = 0
for m in tqdm(msgs):
    sender_match = sender_mail_rgx.match(m.sender)
    if not sender_match:
        errors.append(f"Can't identify sender: '{m.sender}' in '{m.subject}'")
        continue

    sender = (sender_match.group("mail") or sender_match.group("mailonly")).replace("@", "_at_")
    sender = filename_rgx.sub("_", sender)
    sender_path = out_path / sender
    sender_path.mkdir(exist_ok=True)

    if not m.date:
        errors.append(f"Can't identify date: '{m.date}' in '{m.subject}'")
        continue

    date = parser.parse(m.date).date().strftime("%Y-%m-%d")
    subject = filename_rgx.sub("_", m.subject)
    subject = subject if len(subject) <= 50 else subject[:49] + "…"
    attachment_path = sender_path / f"[{date}] {subject}".strip()
    attachment_path.mkdir(exist_ok=True)

    for a in tqdm(m.attachments, leave=False):
        root, ext = splitext(a.filename)
        if len(root) > 50:
            root = root[:47] + "…"

        file = root + ext
        target = attachment_path / file
        if not target.exists():
            a.save(filepath=str(target))
            total += 1

print("Errors:")
for e in errors:
    print("  " + e)


print(f"Total attachments saved: {total}")
