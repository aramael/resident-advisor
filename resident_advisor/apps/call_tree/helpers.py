import urllib

from django.shortcuts import resolve_url


def call_tree_outbound_call(client, from_, phoneNumber):

    outgoing_call_url = url_with_get('')

    client.calls.create(to=phoneNumber, from_=from_, url=outgoing_call_url)

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