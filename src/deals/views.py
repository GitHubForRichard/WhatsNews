from django.shortcuts import render, redirect
import math
import requests
import urllib3
import os
import shutil
# Disable warning message being printed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
from datetime import timedelta, timezone, datetime
from .models import Deal

def deal_list(request):

    deal_scrape(request)

    deal = Deal.objects.all()

    context = {
        'deal_list': deal,
    }
    return render(request, "deals/templates/deals/list.html", context)


# Create your views here.
def deal_scrape(request):

    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    url = "https://www.dealmoon.com/cn/popular-deals"

    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, "html.parser")

    # provide a parameter (class) to search for
    # return a list
    deals = soup.find_all('ul', {'class' : 'Topclick_list clearfix'})

    print(len(deals))

    Deal.objects.all().delete()

    for ul in deals:
        for deal in ul.find_all("li"):
            link = deal.findAll("a")[0].get('href')
            title = deal.findAll("a")[0].get('title')
            local_filename = "default.jpg"
            imageSource = deal.findAll("img")[0].get('src')

            media_root = '/Users/Che Liu/PycharmProjects/dashboard/media_root'
            if not imageSource.startswith(("data:image", "javascript")):
                # take the image url to store the image file
                local_filename = imageSource.split('/')[-1].split("?")[0]
                if(local_filename != "placeholder.jpg"):
                    r = session.get(imageSource, stream=True, verify=False)
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            f.write(chunk)
                    current_image_absolute_path = os.path.abspath(local_filename)
                    shutil.copy(current_image_absolute_path, media_root)
            new_deal = Deal()
            # print("Local File Path " + str(local_filename))
            new_deal.title = str(title)
            new_deal.image = local_filename
            new_deal.url = link
            new_deal.save()


    return redirect('/deals')
