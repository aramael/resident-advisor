import urllib
import phonenumbers

from django.shortcuts import resolve_url


def call_tree_outbound_call(client, tree, from_, to):

    outgoing_call_url = url_with_get({'to': to, 'call_tree_id': tree.pk})

    client.calls.create(to=to, from_=from_, url=outgoing_call_url)

    return True


def url_with_get(to, **kwargs):

    if kwargs is not None:

        cleaned_kwargs = {}

        for key, value in kwargs.iteritems():
            if isinstance(value, list):
                value = ','.join(value)
            cleaned_kwargs[key] = value

        query_args = '?' + urllib.urlencode(cleaned_kwargs)
    else:
        query_args = ''

    if isinstance(to, dict):
        to = resolve_url(**to)
    else:
        to = resolve_url(to)

    return to + query_args


def format_phone_number(phoneNumber):

    if not phoneNumber:
        return

    if phoneNumber[0] == '+':
        # Phone number may already be in E.164 format.
        parse_type = None
    else:
        # If no country code information present, assume it's a US number
        parse_type = "US"

    phone_representation = phonenumbers.parse(phoneNumber, parse_type)
    return phonenumbers.format_number(phone_representation, phonenumbers.PhoneNumberFormat.E164)


def get_conference_name(tree, prefix='resident-advisor-'):

    # Convert Tree to Nice Name
    name = tree.nice_name
    name = name.lower()
    name = name.replace(' ', '-')

    return prefix + name + '-' + str(tree.pk)