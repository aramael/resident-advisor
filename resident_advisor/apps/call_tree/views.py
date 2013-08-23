from .helpers import call_tree_outbound_call, url_with_get
from .models import RACallProfile
from .wrappers import twilio
from django.conf import settings
from twilio.rest import TwilioRestClient
from twilio import twiml


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