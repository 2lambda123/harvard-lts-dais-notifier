import os, os.path, logging
import smtplib
from email.message import EmailMessage
from tenacity import retry, stop_after_attempt

logger = logging.getLogger('dais-notifier')
class SmtpMailingService():
    __SMTP_SEND_MESSAGE_MAX_RETRIES = 2
    


    def send_email(self, subject, body, recipients = None):
        logger.info("Creating email message with subject {} and body {}...".format(subject, body))
        email_sender = os.getenv("EMAIL_FROM")
        if recipients is None:
            email_destination = os.getenv("EMAIL_DEFAULT_RECIPIENT")
        else:
            email_destination = recipients
        
        message = self.__create_message(subject, body, email_destination)
        logger.info(
            "Sending email with subject {}, via SMTP...".format(subject)
        )
        
        return self.__send_smtp_message(message)

    def __create_message(self, email_subject, email_body, email_destination):
        logger.info("Creating email message with subject {} and body {}...".format(email_subject, email_body))

        email_sender = os.getenv("EMAIL_FROM")
        logger.info(
            "Sender is {}, and destination is {}, for email with subject {}".format(
                email_sender,
                email_destination,
                email_subject
            )
        )

        message = EmailMessage()
        message.set_content(email_body)

        instance = os.getenv("ENV", "instance unknown")
        message['Subject'] = "(" + instance + ") " + email_subject
        message['From'] = email_sender
        message['To'] = email_destination

        return message

    @retry(
        stop=stop_after_attempt(__SMTP_SEND_MESSAGE_MAX_RETRIES)
    )
    def __send_smtp_message(self, message):
        email_host = os.getenv("EMAIL_HOST")
        email_port = os.getenv("EMAIL_PORT")

        try:
            smtp = smtplib.SMTP(email_host, email_port)
            smtp.send_message(message)
            smtp.quit()
        except smtplib.SMTPException as e:
            logger.error(str(e))
            raise e

        logger.info("Email sent")
        return True
