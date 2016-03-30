from flask_mail import Message
import mock

from pypicalc.app import PyPICalc


def send_contact_email(user_email, subject, body, send_func=PyPICalc.mail.send):
    msg = Message(subject, reply_to=user_email)
    msg.add_recipient('somebodyelse@example.com')
    msg.body = body
    send_func(msg)


class TestSendContactEmail(object):

    def test_message_creation(self):
        m_send_func = mock.Mock()
        send_contact_email('me@me.com', 'hi there', 'you rock!', m_send_func)

        assert m_send_func.call_count == 1
        pos_args, kwargs = m_send_func.call_args
        msg = pos_args[0]

        assert msg.subject == 'hi there'
        assert msg.reply_to == 'me@me.com'
        assert msg.sender == 'fakesender@example.com'
        assert msg.recipients == ['somebodyelse@example.com']
