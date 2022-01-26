import smtplib, ssl


def send_email(text):
    """
    Send an email with gmail.  Notice the newline '\n' character
    appended to the text before it is sent.  This is necessary so
    the text is not sent as part of the subject.
    """
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "<name@gmail.com>"  # Enter your address
    receiver_email = "<receiver@example.com>"  # Enter receiver address
    password = "password"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, f"\n{text}")
