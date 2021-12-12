from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings 
from django.contrib import messages
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from twilio.rest import Client
from .forms import ReviewsPost, RequestPost
from .models import Reviews, UserInformation, Request
from django.forms import ModelForm
from geopy import Nominatim
import csv
from django.conf import settings
from twilio.rest import Client
from .forms import SMSForm
from django.contrib.auth.decorators import user_passes_test

'''
REFERENCES 
Title: Twilio SMS PYthon Quickstate
Author: Twilio
Date: 11/13/2021
URL: https://www.twilio.com/docs/sms/quickstart/python
Software License: None

Title: geopy 2.2.0 Project Description
Author: Kostya Esmukov
Date: 11/27/2021
URL: https://pypi.org/project/geopy/
Software License: MIT 
'''


def send_sms(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST' and request.is_ajax():
        # create a form instance and populate it with data from the request:
        form = SMSForm(request.POST)
        curr_user = request.user
        persons = UserInformation.objects.all().filter(created_by=curr_user).order_by('-id').first()
        
        # check whether it's valid:
        if form.is_valid():
            try:
                phone_number = persons.phone_number
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

                message = client.messages.create(       # send TWILIO message with the instructions from tripDirections in map.html JS function.
                    to=str(phone_number),
                    from_=settings.TWILIO_NUMBER,
                    body=request.POST['dir_message'])
                
            except:
                messages.warning(request,
                                 format_html("You do not have a phone number on file and therefore cannot use 'Text Directions'<br><a href='/'>{}</a>", "Add It Here!"))
                
        else:
            messages.warning(request,
                                 format_html("You do not have a phone number on file and therefore cannot use 'Text Directions'<br><a href='/'>{}</a>", "Add It Here!"))

    return render(request, 'map.html') # after message is sent, render the map.html page as previously seen.


def index(request):
    return HttpResponse("Guide Index")


class InputForm(ModelForm):
    class Meta:
        model = UserInformation
        fields = '__all__'


def user_view(request):
    try:
        entries = InputForm(request.POST)
        entries.save()
        return HttpResponseRedirect(reverse('guide:thanks'))  # Redirect to the thanks page
    except:
        return render(request, 'index.html')


def info_success(request):
    return render(request, "thanks.html")


def default_map(request):
    form = SMSForm()
    mapbox_access_token = 'mapbox_access_token'
    curr_user = request.user
    lat = 0
    long = 0
    # If the user is not logged in and tries to automatically direct to the map page, the second conditional
    # statement below will create an internal server error (500)
    # Need to first ensure that the user is not anonymous
    if not request.user.is_anonymous:
        # If the user is in the UserInformation model, get the latitude and longitude of their address
        if UserInformation.objects.all().filter(created_by=curr_user):
            persons = UserInformation.objects.all().filter(created_by=curr_user).order_by('-id').first()
            address = persons.address.strip()
            city = persons.city.strip()
            state = persons.state.strip()
            zipcode = persons.zipcode.strip()
            # Concatenate the address
            req_addr = address + " " + city + " " + state + " " + zipcode
            # Get the latitude and longitude of the user's address
            geolocator = Nominatim(user_agent="uvaguide")
            location = geolocator.geocode(req_addr)
            # If the latitude and longitude are valid coordinates, set the variables
            # If the address cannot be mapped to coordinates, Geopy returns None
            if location:
                lat = location.latitude
                long = location.longitude
    # Pass the gathered information to the map template
    return render(request, 'map.html', {'mapbox_access_token': mapbox_access_token, 'lat': lat, 'long': long})


class ReviewsView(generic.CreateView):
    model = Reviews
    form_class = ReviewsPost
    template_name = 'reviews.html'
    fields = '__all__'

    def get(self, request):
        form = ReviewsPost()
        return render(request, self.template_name, {'form': form})


def listR(request):
    reviews_list = Reviews.objects.all()
    context = {'reviews_list': reviews_list}
    if request.POST.get('location') is not None:
        location = request.POST.get("location")
        review = request.POST.get("review")
        dt = Reviews(location=location, review=review)
        dt.save()
    return render(request, "reviews/list.html", context)


class RequestView(generic.CreateView):
    model = Request
    form_class = RequestPost
    template_name = 'request.html'

    def get(self,request):
        form = RequestPost()
        return render(request, self.template_name, {'form' : form})


def reqList(request):
    request_list = Request.objects.all()
    context = {'request_list': request_list}
    if request.POST.get('address') is not None:
        name = request.POST.get("name")
        address = request.POST.get("address")
        geolocator = Nominatim(user_agent="uvaguide")
        loc = geolocator.geocode(address) 
        if hasattr(loc,'latitude') and (loc.latitude is not None) and hasattr(loc, 'longitude') and (loc.longitude is not None) and loc.latitude > 37.5 and loc.latitude < 38.5 and loc.longitude < -78 and loc.longitude > -79 and not(Request.objects.filter(latitude=loc.latitude).exists() and Request.objects.filter(longitude=loc.longitude).exists()):
            latitude = loc.latitude
            longitude = loc.longitude
            r = Request(name=name, address=address, latitude=latitude,longitude=longitude)
            r.save()
        elif hasattr(loc,'latitude') and (loc.latitude is not None) and hasattr(loc, 'longitude') and (loc.longitude is not None) and Request.objects.filter(latitude=loc.latitude).exists() and Request.objects.filter(longitude=loc.longitude).exists():
            return render(request, 'request/duplicate.html', context)
        elif hasattr(loc,'latitude') and (loc.latitude is not None) and hasattr(loc, 'longitude') and (loc.longitude is not None) and not((loc.latitude > 37.5 and loc.latitude < 38.5) and (loc.longitude < -78 and loc.longitude > -79)):
            return render(request, 'request/outofrange.html', context)
        else:
            return render(request, 'request/failure.html')
    return render(request, 'request/success.html', context)


@user_passes_test(lambda u: u.is_staff)
def csvView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    for req in Request.objects.all().values_list('name', 'address', 'latitude', 'longitude').distinct():
        writer.writerow(req)
    response['Content-Disposition'] = 'attachment; filename = "requested_pois.csv"'
    return response
    

def sendSMS(request):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(to=request.POST.get('recipient'),
                                   from_=settings.TWILIO_NUMBER,
                                   body=request.POST.get('directions'))
    return HttpResponse("Message send success", 200)
