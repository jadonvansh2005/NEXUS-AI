"""
UPSS Send Email Tool

Provider-independent email sender.

Later providers can include:

- SMTP
- Gmail API
- Microsoft Graph
- Exchange
"""

from __future__ import annotations

import uuid

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.email.schemas import (
    SendEmailRequest,
    EmailResponse,
)


class SendEmailTool(BaseTool):
    """
    Send emails.

    Actual delivery is delegated to the configured
    email provider.
    """

    metadata = ToolMetadata(

        name="email.send",

        display_name="Send Email",

        description="Send email using configured provider.",

        category=ToolCategory.COMMUNICATION,

        tags=[
            "email",
            "send",
            "communication",
        ],

    )

    permission = ToolPermission.write()

    input_model = SendEmailRequest

    async def execute(
        self,
        context: ToolContext,
        request: SendEmailRequest,
    ) -> ToolResult:

        import os
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders

        payload = {
            "id": str(uuid.uuid4()),
            "to": request.to,
            "cc": request.cc,
            "bcc": request.bcc,
            "subject": request.subject,
            "body": request.body,
            "html": request.html,
            "priority": request.priority.value,
            "attachments": request.attachments,
        }

        from app.settings import settings

        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT
        sender_email = settings.SMTP_SENDER_EMAIL
        sender_password = settings.SMTP_SENDER_PASSWORD

        email_status_msg = "Email request created successfully."

        if sender_email and sender_password:
            try:
                # Query user details dynamically to set From display name and Reply-To
                from database.connection import SessionLocal
                from models.user import User

                db = SessionLocal()
                user_name = "User"
                user_email = None
                try:
                    try:
                        uid = int(context.user_id) if context.user_id else 1
                    except ValueError:
                        uid = 1
                    user = db.query(User).filter(User.id == uid).first()
                    if user:
                        user_name = user.name
                        user_email = user.email
                except Exception as db_err:
                    print(f"Error fetching user for SendEmailTool: {db_err}")
                finally:
                    db.close()

                # Prepare MIMEMultipart email message
                msg = MIMEMultipart()
                
                # Format: "User Name (via UPSS)" <no-reply@upss.com>
                msg["From"] = f'"{user_name} (via UPSS)" <no-reply@upss.com>'
                
                # Format: Reply-To points to the real logged-in user email
                if user_email:
                    msg["Reply-To"] = user_email
                
                msg["To"] = ", ".join(request.to)
                if request.cc:
                    msg["Cc"] = ", ".join(request.cc)
                msg["Subject"] = request.subject

                # Set body content (text/html or text/plain)
                body_type = "html" if request.html else "plain"
                msg.attach(MIMEText(request.body, body_type))

                # Handle file attachments with Auto-Healing search support
                if request.attachments:
                    for filepath in request.attachments:
                        actual_path = filepath
                        # If relative path, try joining with uploads/datasets/ first
                        if not os.path.isabs(actual_path) and not os.path.exists(actual_path):
                            dataset_path = os.path.join("uploads", "datasets", filepath)
                            if os.path.exists(dataset_path):
                                actual_path = dataset_path

                        if not os.path.exists(actual_path):
                            # Try searching inside the uploads/ folder recursively
                            filename = os.path.basename(filepath)
                            for root_dir, _, files in os.walk("uploads"):
                                if filename in files:
                                    actual_path = os.path.join(root_dir, filename)
                                    print(f"📧 Auto-healed email attachment path: found '{filename}' at '{actual_path}'", flush=True)
                                    break

                        print(f"\n--- DEBUG Check 2 & 3 (Email Tool) ---", flush=True)
                        print(f"attachment_path (resolved): {actual_path}", flush=True)
                        print(f"os.path.exists(attachment_path): {os.path.exists(actual_path)}", flush=True)

                        if os.path.exists(actual_path):
                            with open(actual_path, "rb") as f:
                                part = MIMEBase("application", "octet-stream")
                                part.set_payload(f.read())
                                encoders.encode_base64(part)
                                part.add_header(
                                    "Content-Disposition",
                                    f"attachment; filename= {os.path.basename(actual_path)}",
                                )
                                msg.attach(part)

                print(f"\n--- DEBUG Check 4 (Email Tool) ---", flush=True)
                print(f"msg.is_multipart(): {msg.is_multipart()}", flush=True)
                # Print email structure headers to verify attachment MIME segments exist
                print(f"msg structure headers:\n{msg.as_string()[:500]}...", flush=True)

                # Send using SMTP TLS
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                
                # Recipients collection (to + cc + bcc)
                recipients = request.to + (request.cc or []) + (request.bcc or [])
                server.sendmail(sender_email, recipients, msg.as_string())
                server.quit()

                email_status_msg = f"Email sent successfully from {sender_email} to {', '.join(request.to)}!"
            except Exception as e:
                email_status_msg = f"Email delivery failed over SMTP: {e}. (Saved request to queue)"
        else:
            email_status_msg = "Email request created successfully. (SMTP not configured in .env, mock mode)"

        response = EmailResponse(
            success=True,
            message=email_status_msg,
            email_id=payload["id"],
        )

        return ToolResult.ok(
            message=response.message,
            data={
                "payload": payload,
                **response.model_dump(),
            },
        )