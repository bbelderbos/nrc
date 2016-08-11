from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def get_sender():
    return open("mail").read().strip()

def get_recipients():
    with open("recipients") as f:
        return [email.strip() for email in f.readlines()]

HOST = "localhost"
SENDER = get_sender()
RECIPIENTS = get_recipients()

class Mail:

    def _create_msg_object(self, subject, content):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER
        msg['To'] = ", ".join(RECIPIENTS)
        part = MIMEText(content, 'html')
        msg.attach(part)
        return msg
    
    def send_email(self, subject, content):
        msg = self._create_msg_object(subject, content)
        s = smtplib.SMTP(HOST)
        s.sendmail(SENDER, RECIPIENTS, msg.as_string())
        s.quit()

if __name__ == "__main__":
    ma = Mail()
    subject = "test subject"
    content = "some content blabla"
    ma.send_email(subject, content)
