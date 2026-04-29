"""Email-related tool builders."""

from typing import Callable

from agents import Agent, function_tool
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To

from sdr.config import Settings
from sdr.prompts import HTML_INSTRUCTIONS, SUBJECT_INSTRUCTIONS


def build_send_html_email_tool(settings: Settings) -> Callable:
    @function_tool
    def send_html_email(subject: str, html_body: str) -> dict[str, str]:
        """Send an HTML email with the given subject and body."""
        sg = sendgrid.SendGridAPIClient(api_key=settings.sendgrid_api_key)
        from_email = Email(settings.sender_email)
        to_email = To(settings.recipient_email)
        content = Content("text/html", html_body)
        mail = Mail(from_email, to_email, subject, content).get()
        sg.client.mail.send.post(request_body=mail)
        return {"status": "success"}

    return send_html_email


def build_email_manager_tools(settings: Settings) -> list:
    subject_writer = Agent(
        name="Email subject writer",
        instructions=SUBJECT_INSTRUCTIONS,
        model="gpt-4o-mini",
    )
    subject_tool = subject_writer.as_tool(
        tool_name="subject_writer",
        tool_description="Write a subject for a cold sales email",
    )

    html_converter = Agent(
        name="HTML email body converter",
        instructions=HTML_INSTRUCTIONS,
        model="gpt-4o-mini",
    )
    html_tool = html_converter.as_tool(
        tool_name="html_converter",
        tool_description="Convert a text email body to an HTML email body",
    )

    return [subject_tool, html_tool, build_send_html_email_tool(settings)]
