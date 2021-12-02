from django.shortcuts import render
from django.http import HttpResponse
from newsletter.my_custom import NominatimGeocoding

pages = [
    {'active': ''}
]

def main_page(request):
    place = NominatimGeocoding("Zagórz")

    context ={

        'title': 'Strona główna',
        'place': place,
    }
    print(context)
    return render(request, 'main.html', context)


def newsletter_page(request):
    return HttpResponse('To jest strona g')


def show_page(request, lat=0, long=0):
    return HttpResponse(f'Długość to {lat} a szerokość {long}')
