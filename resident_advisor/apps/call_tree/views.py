from .helpers import call_tree_outbound_call, url_with_get
from .models import RACallProfile
from .wrappers import twilio
from django.conf import settings
from django.http import HttpResponse
from twilio.rest import TwilioRestClient
from twilio import twiml
from json import dumps as json_encode


@twilio
def call_recieve(request):

    r = twiml.Response()

    caller_number = request.POST.get('From', None)

    try:
        caller = RACallProfile.objects.get(formatted_phone_number=caller_number)
    except RACallProfile.DoesNotExist:
        r.reject()
        return r

    # Connect Caller to the Conference Call
    r.say('We are now calling all of the resident advisors in the call tree. Please wait as they are connected.')
    with r.dial() as d:
        d.conference('resident-advisor-call-tree')

    # Dial Everyone Else to Conference Call

    client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)

    calls = RACallProfile.objects.all().exclude(formatted_phone_number=caller_number)

    for call in calls:
        call_tree_outbound_call(client, request.POST['To'], call.phone_number)

    return r

@twilio
def outgoing_call(request):

    r = twiml.Response()

    with r.gather(numDigits='1', action=url_with_get('conference_connect')) as g:
        g.say('East Campus Alert Call. Press any key to connect', loop=20)

    r.say('Sorry, we missed you we will try calling again in a few moments.')

    r.hangup()

    return r


@twilio
def conference_connect(request):

    r = twiml.Response()

    r.say('You have been connected.')

    with r.dial() as d:
        d.conference('resident-advisor-call-tree')

    return r


def number_search(request):

    client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)

    search_kwargs = {
        'country': 'US',
    }

    if 'area_code' in request.POST and request.POST['area_code']:
        search_kwargs['area_code'] = request.POST['area_code']

    if 'search_term' in request.POST and request.POST['search_term']:
        search_kwargs['contains'] = request.POST['search_term']

    numbers = client.phone_numbers.search(**search_kwargs)

    json_numbers = []

    for number in numbers:
        json_numbers.append({
            'friendly_name': number.friendly_name,
            'phone_number': number.phone_number,
            'postal_code': number.postal_code,
        })

    data = {
        'success': True,
        'numbers': json_numbers,
    }

    return HttpResponse(json_encode(data))
