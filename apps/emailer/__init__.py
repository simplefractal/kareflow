from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class BaseEmailEngine(object):
    """
    Base email engine for rendering a template and sending it.
    Example implementation:

    class WelcomeEmail(BaseEmailEngine):
        '''
        A welcome email once a user signs up for our service.
        '''
        template = 'welcome.html'
        def __init__(self, user):
            self.user = user
        def get_recipients(self):
            return [self.user.email]

    >>> from emailer import WelcomeEmail
    >>> first_user = User.objects.get(id=1)
    >>> WelcomeEmail(first_user).send()
    """
    from_address = "youremail@address.com"

    def render(self):
        return render_to_string(self.template, self.get_context())

    def send(self):
        message = EmailMessage(
            self.make_subject_line(),
            self.render(),
            self.from_address,
            self.get_recipients,
            headers={'Reply-To': self.from_address}
        )
        message.content_subtype = "html"
        message.send()

    def get_recipients(self):
        raise NotImplementedError
