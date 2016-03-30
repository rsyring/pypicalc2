from flask_mail import Message
import mock

from pypicalc.app import PyPICalc


def send_contact_email(user_email, subject, body):
    msg = Message(subject, reply_to=user_email)
    msg.add_recipient('somebodyelse@example.com')
    msg.body = body
    PyPICalc.mail.send(msg)


class WebController(object):
    def __init__(self, mail_func=send_contact_email):
        self.mail_func = mail_func

    def on_post(self, post_vars):
        email = post_vars['email']
        subject = post_vars['subject']
        message = post_vars['message']

        if email == '' or subject == '' or message == '':
            return 'all fields are required'

        self.mail_func(email, subject, message)
        return 'contact email sent'


class TestController(object):

    def test_missing_field(self):
        msce = mock.Mock()
        controller = WebController(msce)

        post_data = dict(email='me@me.com', subject='hi there', message='')
        retval = controller.on_post(post_data)
        assert retval == 'all fields are required'

        assert msce.call_count == 0

    def test_success(self):
        msce = mock.Mock()
        controller = WebController(msce)

        post_data = dict(email='me@me.com', subject='hi there', message='you rock!')
        retval = controller.on_post(post_data)
        assert retval == 'contact email sent'

        msce.assert_called_once_with('me@me.com', 'hi there', 'you rock!')
