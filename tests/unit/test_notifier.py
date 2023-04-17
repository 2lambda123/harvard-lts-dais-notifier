import pytest, sys
sys.path.append('app')
from notifier.dais_notifier import SmtpMailingService 

   
def test_send_email_with_no_recipients():
    '''Sends an email which should receive the default recipients'''
    subject = "Test DAIS Notification Email"
    body = "Test DAIS Notification Email\nBody"
    
    mailing_service = SmtpMailingService()
    retval = mailing_service.send_email(subject, body)
    
    #Check that the email was sent
    assert retval

def test_send_email_with_one_recipient():
    '''Sends an email with one recipient'''
    subject = "Test DAIS Notification Email"
    body = "Test DAIS Notification Email\nBody"
    recipients = "valdeva_crema@harvard.edu"
    mailing_service = SmtpMailingService()
    retval = mailing_service.send_email(subject, body, recipients = None)
    
    #Check that the email was sent
    assert retval
    
def test_send_email_with_two_recipients():
    '''Sends an email with two comma-delimited recipients '''
    subject = "Test DAIS Notification Email"
    body = "Test DAIS Notification Email\nBody"
    recipients = "DTS@HU.onmicrosoft.com, valdeva_crema@harvard.edu"
    mailing_service = SmtpMailingService()
    retval = mailing_service.send_email(subject, body, recipients = None)
    
    #Check that the email was sent
    assert retval