from flask_mail import Message

from pypicalc.app import PyPICalc


def send_contact_email(user_email, subject, body):
    msg = Message(subject, reply_to=user_email)
    msg.add_recipient('somebodyelse@example.com')
    msg.body = body
    PyPICalc.mail.send(msg)


class TestSendContactEmail(object):

    def test_message_creation(self):

        with PyPICalc.mail.record_messages() as outbox:
            send_contact_email('me@me.com', 'hi there', 'you rock!')
            assert len(outbox) == 1
            msg = outbox[0]

        assert msg.subject == 'hi there'
        assert msg.reply_to == 'me@me.com'
        assert msg.sender == 'fakesender@example.com'
        assert msg.recipients == ['somebodyelse@example.com']
