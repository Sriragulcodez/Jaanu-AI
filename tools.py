import logging
import requests
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from livekit.agents import function_tool, RunContext

# Weather tool
@function_tool()
async def get_weather(context: RunContext, city: str) -> str:
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            return response.text.strip()
        return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Weather error: {e}")
        return f"Error retrieving weather for {city}."

# Web search tool
@function_tool()
async def search_web(context: RunContext, query: str) -> str:
    from langchain_community.tools import DuckDuckGoSearchRun
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        return results
    except Exception as e:
        logging.error(f"Web search error: {e}")
        return f"Error searching for '{query}'."

# Email tool
@function_tool()
async def send_email(
    context: RunContext,
    to_email: str,
    subject: str,
    message: str,
    cc_email: Optional[str] = None
) -> str:
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")
        if not gmail_user or not gmail_password:
            return "Gmail credentials not configured."
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        recipients = [to_email]
        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipients, msg.as_string())
        server.quit()
        return f"Email sent successfully to {to_email}"
    except Exception as e:
        logging.error(f"Email error: {e}")
        return f"Error sending email: {str(e)}"

# Singing tool
@function_tool()
async def sing_song(context: RunContext, song_name: str) -> str:
    """
    Sing a song melodically when requested.
    The AI will respond with lyrics in a friendly, romantic tone.
    """
    # You can integrate with an AI or return fixed lyrics for simplicity
    return f"Singing '{song_name}'... 🎵 La la la, this is your sweet song! 🎶"
