import os
import json
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv
import re

load_dotenv()  # Loads from .env

def validate_email(email):
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def send_email(event, context):
    try:
        # Check if event has body
        if 'body' not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Request body is missing"})
            }

        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid JSON format in request body"})
            }

        # Validate required fields
        required_fields = ["receiver_email", "subject", "body_text"]
        missing_fields = [field for field in required_fields if field not in body or not body[field]]
        
        if missing_fields:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Missing required fields",
                    "missing_fields": missing_fields
                })
            }

        receiver_email = body["receiver_email"]
        subject = body["subject"]
        body_text = body["body_text"]

        # Validate email format
        if not validate_email(receiver_email):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid receiver email format"})
            }

        # Check if environment variables are set
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        
        if not email_user or not email_pass:
            return {
                "statusCode": 500,
                "body": json.dumps({"message": "Email service configuration is missing"})
            }

        # Create and send email
        msg = EmailMessage()
        msg.set_content(body_text)
        msg["Subject"] = subject
        msg["From"] = formataddr(("Sender", email_user))
        msg["To"] = receiver_email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email_user, email_pass)
                smtp.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            return {
                # 401 Unauthorized for authentication failures
                "statusCode": 401,
                "body": json.dumps({"message": "Email authentication failed"})
            }
        except smtplib.SMTPRecipientsRefused:
            return {
                # 400 Bad Request for client errors (invalid input)
                "statusCode": 400,
                "body": json.dumps({"message": "Recipient email refused by server"})
            }
        except smtplib.SMTPServerDisconnected:
            return {
                # 503 Service Unavailable for server disconnections
                "statusCode": 503,
                "body": json.dumps({"message": "Email service unavailable"})
            }
        except smtplib.SMTPException as e:
            return {
                # 502 Bad Gateway for SMTP failures
                "statusCode": 502,
                "body": json.dumps({"message": f"Email sending failed: {str(e)}"})
            }

        return {
            # 200 OK for successful operations
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully!"})
        }

    except Exception as e:
        return {
            # 500 Internal Server Error for unexpected errors
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error",
                "error": str(e)
            })
        }
    




