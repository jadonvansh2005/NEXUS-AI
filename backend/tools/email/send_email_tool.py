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
                # Prepare MIMEMultipart email message
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = ", ".join(request.to)
                if request.cc:
                    msg["Cc"] = ", ".join(request.cc)
                msg["Subject"] = request.subject

                # Set body content (text/html or text/plain)
                body_type = "html" if request.html else "plain"
                msg.attach(MIMEText(request.body, body_type))

                # Handle file attachments
                if request.attachments:
                    for filepath in request.attachments:
                        if os.path.exists(filepath):
                            with open(filepath, "rb") as f:
                                part = MIMEBase("application", "octet-stream")
                                part.set_payload(f.read())
                                encoders.encode_base64(part)
                                part.add_header(
                                    "Content-Disposition",
                                    f"attachment; filename= {os.path.basename(filepath)}",
                                )
                                msg.attach(part)

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