from django.contrib.messages import get_messages


def check_message(response, message):
    """Check if a specific message is present in the response's messages."""
    messages = list(get_messages(response.wsgi_request))
    if len(messages) == 1:
        return str(messages[0]) == message


def fake_is_bind(is_bound):
    """Create a fake LDAP binding function based on the given binding state."""
    if is_bound:
        return lambda email, password: True
    return lambda email, password: False


def get_templates(response):
    """Get a list of template names used in the response."""
    return [template.name for template in response.templates]
