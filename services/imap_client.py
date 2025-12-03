import imaplib
import email
import os
import re
from datetime import datetime
from dotenv import load_dotenv


class EmailClient:
    def __init__(self):
        load_dotenv()
        email = os.getenv("EMAIL")
        password = os.getenv("APP_PASS")
        self.conn = imaplib.IMAP4_SSL("imap.gmail.com")
        self.conn.login(email, password)

    def get_purchase_notifications(self, last_purchase_date=""):
        emails = []
    
        # Select mailbox
        self.conn.select('"[Gmail]/All Mail"')
        search_str = ""
        if last_purchase_date:
            date = self.format_date(last_purchase_date)
            search_str = f'(SINCE "{str(date)}" FROM "PC Financial" SUBJECT "Purchase")'
        else:
            search_str = f'(FROM "PC Financial" SUBJECT "Purchase")'
        status, data = self.conn.search(None, search_str)
        msgs = data[0].split()
        if not msgs:
            return emails  # nothing new
    
        for msg in msgs:
            status, msg_data = self.conn.fetch(msg, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
    
            # Extract text
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                        lines = body.split("\r\n")
                        merchant = lines[9].split(":")[1].strip()
                        amount = float(re.sub(r'[^\d.]', '', lines[10]))
                        date_str = lines[11].split(":")[1].strip()
    
                        emails.append({
                            "merchant": merchant,
                            "amount": amount,
                            "date": date_str,
                        })
        return emails

    def format_date(self, date):
        formatted = date.strftime("%d-%b-%Y")
        return formatted
        

if __name__ == ("__main__"):
    conn = EmailClient()
