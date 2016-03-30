from flask_mail import Message

from pypicalc.app import PyPICalc


def send_contact_email(user_email, subject, body):
    msg = Message(subject, reply_to=user_email)
    msg.add_recipient('somebodyelse@example.com')
    msg.body = body
    PyPICalc.mail.send(msg)


class WebController(object):
    def on_post(self, post_vars):
        email = post_vars['email']
        subject = post_vars['subject']
        message = post_vars['message']

        if email == '' or subject == '' or message == '':
            return 'all fields are required'

        send_contact_email(email, subject, message)
        return 'contact email sent'


class TestController(object):

    def test_missing_field(self):
        controller = WebController()
        post_data = dict(email='me@me.com', subject='hi there', message='')
        retval = controller.on_post(post_data)
        assert retval == 'all fields are required'

    def test_success(self):
        controller = WebController()
        post_data = dict(email='me@me.com', subject='hi there', message='you rock!')
        retval = controller.on_post(post_data)
        assert retval == 'contact email sent'
