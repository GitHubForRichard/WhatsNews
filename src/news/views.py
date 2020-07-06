from django.shortcuts import render, redirect
import requests
import urllib3
import os
import shutil
# Disable warning message being printed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
from datetime import timedelta, timezone, datetime
from .models import Headline, UserProfile, coronavirusCount

def news_list(request):

    scrape(request)

    headlines = Headline.objects.all()[3:]
    topNews1 = Headline.objects.all()[0]
    topNews2 = Headline.objects.all()[1]
    topNews3 = Headline.objects.all()[2]
    confirmCase = coronavirusCount.objects.all()[0]
    confirmCaseToday = coronavirusCount.objects.all()[1]
    deathCase = coronavirusCount.objects.all()[2]
    curedCase = coronavirusCount.objects.all()[3]

    # print("Headline size:" + str(len(headlines)))
    context = {
        'object_list': headlines,
        # 'virus_count': counts,
        'confirm_case': confirmCase,
        'confirm_case_today': confirmCaseToday,
        'death_case': deathCase,
        'cured_case': curedCase,
        'top_news1' : topNews1,
        'top_news2': topNews2,
        'top_news3': topNews3,
        # 'hide_me': hide_me,
        # 'next_scrape': math.ceil(next_scrape)
    }
    return render(request, "news/templates/news/home.html", context)


# Create your views here.
def scrape(request):
    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    url = "https://www.singtaousa.com/sf/455-%E7%BE%8E%E5%9C%8B/"

    coronaVirusUrl = "https://www.dealmoon.com/guide/934164"

    # grab the html from the session
    content = session.get(url, verify=False).content
    virusContent = session.get(coronaVirusUrl, verify=False).content

    soup = BeautifulSoup(content, "html.parser")
    virusSoup = BeautifulSoup(virusContent, "html.parser")

    # provide a parameter (class) to search for
    # return a list
    posts = soup.find_all('div', {'class' : 'news-wrap'})
    counts = virusSoup.find_all('div', {'class' : 'edit-content guide-edit ga_event_statistics_content_guide'})

    Headline.objects.all().delete()
    coronavirusCount.objects.all().delete()

    coronaVirusData = counts[0].findAll("td")[0:4]

    i = 0
    while i < 4:
        new_count = coronavirusCount()
        new_count.virusCount = coronaVirusData[i].text
        new_count.save()
        i += 1



    for post in posts:
        link = post.findAll("a")[0].get('href')
        title = post.findAll("a")[0].get('title')
        description = ""
        dateText = post.findAll("div", {"class", "time"})[0].text

        find_description = post.findAll("div", {"class", "no_in_mobile txt_id_m"})


        if len(find_description) > 0:
            description = find_description[0].text

        local_filename = "default.jpg"
        if len(post.findAll("img")) > 0:
            imageSource = post.findAll("img")[0].get('src')
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

        findDiv = post.find('div', class_='emptyDefine')

        if findDiv is not None:
            imageSource = post.find('div', class_='emptyDefine').get('style').split('background-image:')[-1][5:-1]
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

        # print("Local File Path " + str(local_filename))
        new_headline = Headline()
        new_headline.title = str(title)
        new_headline.image = local_filename
        new_headline.url = link
        new_headline.description = str(description)
        new_headline.dateText = str(dateText)
        new_headline.save()


    return redirect('/home/')
