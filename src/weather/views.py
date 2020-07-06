from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.

def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=56f8912a2740163d803cf6f4cf35e567"

    # return all the cities in the database
    cities = City.objects.all()
    weather_data = []

    # only true if the form is sumitted
    if request.method == "POST":
        # added actual request data to form for processing
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    for city in cities:
        # request the API data and convert the JSON to Python data types
        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        print(weather['city'])
        # add the data for the current city into our list
        weather_data.append(weather)
    context = {'weather_data': weather_data,
               'form' : form}
    return render(request, 'weather/templates/weather/index.html', context)