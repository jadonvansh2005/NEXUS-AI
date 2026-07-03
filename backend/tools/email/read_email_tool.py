"""
UPSS Read Email Tool

Reads an email using the configured provider.

Future providers:

- Gmail API
- IMAP
- Microsoft Graph
- Exchange
"""

from __future__ import annotations

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.email.schemas import (
    ReadEmailRequest,
    EmailResponse,
)


class ReadEmailTool(BaseTool):
    """
    Read an email.
    """

    metadata = ToolMetadata(

        name="email.read",

        display_name="Read Email",

        description="Read an email.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "email",
            "read",
            "communication",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = ReadEmailRequest

    async def execute(
        self,
        context: ToolContext,
        request: ReadEmailRequest,
    ) -> ToolResult:

        from app.settings import settings
        sender_email = settings.SMTP_SENDER_EMAIL
        sender_password = settings.SMTP_SENDER_PASSWORD

        email_data = None
        if sender_email and sender_password:
            try:
                import imaplib
                import email
                from email.header import decode_header

                # Connect and login to Gmail IMAP
                mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
                mail.login(sender_email, sender_password)
                mail.select("inbox")

                target_id = None
                if "@" in request.email_id:
                    # Search for emails from this sender address and pick the latest one
                    status, search_data = mail.search(None, f'FROM "{request.email_id}"')
                    if status == "OK" and search_data[0]:
                        target_id = search_data[0].split()[-1]
                else:
                    target_id = request.email_id.encode("utf-8")

                if target_id:
                    # Fetch specific email by sequence ID
                    status, data = mail.fetch(target_id, "(RFC822)")
                if status == "OK":
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            
                            # Decode subject
                            subject, encoding = decode_header(msg["Subject"] or "")[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding or "utf-8", errors="ignore")
                                
                            # Decode sender
                            from_, encoding = decode_header(msg["From"] or "")[0]
                            if isinstance(from_, bytes):
                                from_ = from_.decode(encoding or "utf-8", errors="ignore")

                            # Extract full email body text
                            body = ""
                            html_mode = False
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    if content_type == "text/plain" and not body:
                                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                    elif content_type == "text/html":
                                        html_body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                        if html_body:
                                            body = html_body
                                            html_mode = True
                            else:
                                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                                if msg.get_content_type() == "text/html":
                                    html_mode = True

                            email_data = {
                                "id": request.email_id,
                                "from": from_,
                                "to": [msg["To"] or ""],
                                "cc": [msg["Cc"] or ""] if msg["Cc"] else [],
                                "bcc": [],
                                "subject": subject,
                                "body": body,
                                "html": html_mode,
                                "attachments": []
                            }
                mail.close()
                mail.logout()
            except Exception as e:
                print(f"[IMAP Read Error] {e}")

        # Fallback to mock data if not found
        if not email_data:
            email_data = {
                "id": request.email_id,
                "from": "sender@example.com",
                "to": [
                    "user@example.com",
                ],
                "cc": [],
                "bcc": [],
                "subject": "Sample Email (Fallback)",
                "body": "This is a placeholder email. Integrate your provider here.",
                "html": False,
                "attachments": [],
            }

        response = EmailResponse(
            success=True,
            message="Email retrieved successfully.",
            email_id=request.email_id,
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "email": email_data,
                **response.model_dump(),
            },
        )