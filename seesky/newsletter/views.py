from django.shortcuts import render
from django.http import HttpResponse
from newsletter.my_custom import NominatimGeocoding

pages = [
    {'active': ''}
]

def show_page(request):
    if request.method == 'POST':
        place = request.POST['place']
    else:
        place = ""
    place = NominatimGeocoding(place)
    context = {
        'title': 'Strona główna',
        'place': place,
    }
    if not place.error:
        pass


    return render(request, 'show.html', context)


def newsletter_page(request):
    return HttpResponse('To jest strona g')


def main_page(request,):
    return HttpResponse(f'Długość to {lat} a szerokość {long}')
