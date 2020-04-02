import requests 
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models


website_1 = "https://www.avito.ma/fr/maroc/{}"
website_2 = "https://www.jumia.ma/{}"


def home(request):
    return render(request, 'myapp/index.html')

def new_search(request):
    search = request.POST.get("search") 
    models.Search.objects.create(search=search)

    #max-price
    max_price = request.POST.get("max_price")
    if max_price in ('None', '', '\xa0'):
        max_price = 10000000000000000
    else:
        max_price = float(request.POST.get("max_price").replace(" ", ""))
    models.Search.objects.create(max_price=max_price)

    #min-price
    min_price = request.POST.get("min_price")
    if min_price in ('None', '', '\xa0'):
        min_price = 0
    else:
        min_price = float(request.POST.get("min_price").replace(" ", ""))
    models.Search.objects.create(min_price = min_price)


    # category = request.POST.get("category")
    # models.Search.objects.create(category = category)

    # city = request.POST.get("city")
    # models.Search.objects.create(city = city)
    
    #scraping website
    final_url_1 = website_1.format(search.replace(" ", "_"))
    final_url_2 = website_2.format(search.replace(" ", "-"))

    response_1 = requests.get(final_url_1)
    c1 = response_1.content
    soup_1 = BeautifulSoup(c1,"html.parser")

    response_2 = requests.get(final_url_2, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c2 = response_2.content
    soup_2 = BeautifulSoup(c2,"html.parser")

    #titles
    titles_1 = soup_1.find_all("h2",{"class":"fs14"}) 
    titles_2 = soup_2.find_all("span",{"class":"name"})

    #cities
    cities_1 = soup_1.find_all("span",{"class":"item-info-extra fs14"})
    cities_2 = []

    #price
    price_values_1 = soup_1.find_all("span",{"class":"price_value"}) 
    price_values_2 = soup_2.find_all("span",{"class":"price"})

    #links
    links_1 = soup_1.find_all("h2",{"class":"fs14"})
    links_2 = soup_2.find_all("a",{"class":"link"})

    imgs_1 = soup_1.find_all(True, {'class':['item-img no-thumb', 'item-img']})
    imgs_2 = soup_2.find_all('div', {'class':'image-wrapper default-state'})
   
    liste_1 = []
    for i in range (len(titles_1)):
        website = "avito.ma"
        post_title_1 = titles_1[i].text
        
        post_cities_1 = cities_1[i].text.replace("\n","").replace(' -Annonce de professionnel', '')
        
        post_values_1 = price_values_1[i].text
        if post_values_1 in ('None', '', '\xa0'):
            pass
        else:
            post_values_1 = float(price_values_1[i].text.replace(" ", ""))
        

        jump_1 = links_1[i].find_all("a")[0].get('href')
        
        real_link_1 = ""
        
        try:
            real_link_1 = imgs_1[i].find_all('img')[0].get('data-original')
        except:
            real_link_1 = "link to the NON img"

        liste_1.append((post_title_1, post_cities_1, post_values_1,real_link_1, jump_1, website))
    liste_2 = []
    for j in range (len(titles_2)):
        website = "Jumia.ma"
        post_title_2 = titles_2[j].text
        post_cities_2 = "e-commerce"
        post_values_2 = price_values_2[j].text
        if post_values_2 in ('None', '', ' ', '\xa0'):
            pass
        else:
            post_values_2 = float(price_values_2[j].text.replace("Dhs","").replace(" ", "").replace("\xa0",''))
        
        jump_2 = links_2[j].get('href')

        real_link_2 = ""
        try:
            real_link_2 = imgs_2[j].find_all('img')[0].get('data-src')
        except:
            real_link_2 = "link to the non imh"

        liste_2.append((post_title_2, post_cities_2, post_values_2,real_link_2, jump_2, website))




    for_front_end = {
        "search" : search,
        "max_price" : max_price,
        "min_price" : min_price,
        "liste_1" : liste_1,
        "liste_2" : liste_2,
        }
    return render(request, 'myapp/new_search.html', for_front_end)
