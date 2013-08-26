import requests

from .helpers import call_tree_outbound_call, url_with_get
from .models import RACallProfile
from .wrappers import twilio
from django.conf import settings
from django.http import HttpResponse
from twilio.rest import TwilioRestClient
from twilio import twiml
from json import dumps as json_encode
from pyzipcode import ZipCodeDatabase

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
    zcdb = ZipCodeDatabase()

    search_kwargs = {
        'country': 'US',
    }

    if 'location' in request.POST and request.POST['location']:

        # Parse Results into More Easily Searchable Things

        request_payload = {
            'sensor': 'false',
            'address': request.POST['location'],
        }

        r = requests.get('http://maps.googleapis.com/maps/api/geocode/json', params=request_payload)

        location_parse = r.json()

        if 'results' in location_parse:

            location_parse = location_parse['results'][0]['address_components']

            for component in location_parse:
                if 'types' in component:
                    if 'postal_code' in component['types']:
                        search_kwargs['postal_code'] = component['short_name']
                    if 'administrative_area_level_1' in component['types']:
                        search_kwargs['region'] = component['short_name']
    else:
        if 'area_code' in request.POST and request.POST['area_code']:
            search_kwargs['area_code'] = request.POST['area_code']

        if 'search_term' in request.POST and request.POST['search_term']:
            search_kwargs['contains'] = request.POST['search_term']

    numbers = client.phone_numbers.search(**search_kwargs)

    json_numbers = []

    for number in numbers[:9]:

        if number.postal_code:
            zipcode = zcdb[number.postal_code]

            city = zipcode.city
            state = zipcode.state
            locale = city + ', ' + state

        else:
            city = None,
            state = number.region
            locale = state

        json_numbers.append({
            'friendly_name': number.friendly_name,
            'phone_number': number.phone_number,
            'postal_code': number.postal_code,
            'city': city,
            'state': state,
            'location': locale,
        })

    data = {
        'success': True,
        'numbers': json_numbers,
    }

    return HttpResponse(json_encode(data))
