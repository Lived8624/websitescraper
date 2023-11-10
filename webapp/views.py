from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
from .models import Links

def home(request):
    if request.method == "POST":
        link_new = request.POST.get('page', '')
        urls = requests.get(link_new)

        if urls.status_code == 200:  # Check the HTTP status code
            beautysoup = BeautifulSoup(urls.text, 'html.parser')
            for link in beautysoup.find_all('a'):
                li_address = link.get('href')
                li_name = link.string
                Links.objects.create(address=li_address, stringname=li_name)
            return HttpResponseRedirect('/')
        else:
            error_message = f"An error occurred: HTTP status code {urls.status_code}"
            return render(request, "error.html", {'error_message': error_message})
    else:
        data_values = Links.objects.all()
        return render(request, "home.html", {'data_values': data_values})
