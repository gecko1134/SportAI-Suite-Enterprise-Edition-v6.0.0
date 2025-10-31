import os, base64
from pathlib import Path
from typing import List

def send_pdf_via_sendgrid(
    to_emails: List[str],
    subject: str,
    body_text: str,
    pdf_path: Path,
    from_email: str = "no-reply@nationalsportsdome.com",
) -> dict:
    """Send a PDF via SendGrid. Requires SENDGRID_API_KEY in env.
    Returns a dict with 'ok': bool and 'message': str
    """
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        return {"ok": False, "message": "Missing SENDGRID_API_KEY environment variable."}
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
    except Exception as e:
        return {"ok": False, "message": f"SendGrid import failed: {e}"}

    if not Path(pdf_path).exists():
        return {"ok": False, "message": f"PDF not found: {pdf_path}"}

    with open(pdf_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        plain_text_content=body_text,
    )

    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType("application/pdf")
    attachment.file_name = FileName(Path(pdf_path).name)
    attachment.disposition = Disposition("attachment")
    message.add_attachment(attachment)

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            return {"ok": True, "message": f"Sent (status {response.status_code})."}
        return {"ok": False, "message": f"Failed with status {response.status_code}: {response.body}"}
    except Exception as e:
        return {"ok": False, "message": f"Send failed: {e}"}
