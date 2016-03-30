from flask_mail import Message
from keg import current_app

from pypicalc.app import PyPICalc


class IMailService(object):
    def send(self):
        raise NotImplemented


class MockMailService(IMailService):
    sent_messages = []

    def send(self, msg):
        if current_app.testing:
            self.sent_messages.append(msg)
        else:
            PyPICalc.mail.send(msg)


class MailService(IMailService):
    def send(self, msg):
        PyPICalc.mail.send(msg)


class ServiceManager(object):
    def __init__(self):
        if current_app.testing:
            self.mail = MockMailService()
        else:
            self.mail = MailService()

services = ServiceManager()


def send_contact_email(user_email, subject, body):
    msg = Message(subject, reply_to=user_email)
    msg.add_recipient('somebodyelse@example.com')
    msg.body = body
    services.mail.send(msg)


class TestSendContactEmail(object):

    def test_message_creation(self):
        send_contact_email('me@me.com', 'hi there', 'you rock!')
        assert len(services.mail.sent_messages) == 1
        msg = services.mail.sent_messages[0]

        assert msg.subject == 'hi there'
        assert msg.reply_to == 'me@me.com'
        assert msg.sender == 'fakesender@example.com'
        assert msg.recipients == ['somebodyelse@example.com']
