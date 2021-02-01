import json, os, sys, operator
from pip._vendor import requests
from slugify import Slugify

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Hela_robot.settings'

import django

django.setup()

from plats_bank.models import City, Job_type, Job_ad

api_key = "YicmXHhlMFx4ZGRceDgxXHg4ZVx4ZDZpXHhjMlx4YjFceGYwXHgxZS5ceGFhXHhjNFx4OGVqXV1ceGFmXHg5OCc"
city_list_url = "https://taxonomy.api.jobtechdev.se/v1/taxonomy/specific/concepts/municipality?include-legacy-information=true&include-deprecated=false&deprecated=false"
jobb_type_list_url = "https://taxonomy.api.jobtechdev.se/v1/taxonomy/specific/concepts/ssyk?include-legacy-information=false&include-deprecated=false&deprecated=false&relation=related"
job_ads_url = "https://jobsearch.api.jobtechdev.se/search?"
headers = {'api-key': api_key, 'accept': 'application/json', 'x-feature-disable-smart-freetext': 'false',
           'x-feature-enable-false-negative': 'false'
           }


def test_search_loop_through_hits():
    response = requests.get(city_list_url, headers=headers)
    response.raise_for_status()  # check for http errors
    json_response = json.loads(response.content.decode('utf8'))
    hits = json_response
    for hit in hits:
        try:
            city_name = hit['taxonomy/definition']
            lau_2_code_2015 = hit['taxonomy/lau-2-code-2015']
            City(name=city_name, lau_2_code_2015=lau_2_code_2015).save()
        except django.db.utils.IntegrityError:
            print("City allready exsist")


def jobb_type_list_maker():
    response = requests.get(jobb_type_list_url, headers=headers)
    response.raise_for_status()  # check for http errors
    json_response = json.loads(response.content.decode('utf8'))
    hits = json_response
    for hit in hits:
        # print(hit)
        definition = hit['taxonomy/definition']
        af_id = hit['taxonomy/id']
        name = hit['taxonomy/preferred-label']
        ssyk_code_2012 = hit['taxonomy/ssyk-code-2012']
        print(name + '->' + af_id)
        try:
            Job_type(definition=definition, name=name, ssyk_code_2012=ssyk_code_2012, af_id=af_id).save()
        except django.db.utils.IntegrityError:
            print("Jobb type allready exsist")


def job_ads_url_maker(lau_2_code_2015, af_id):
    job_ads_url = 'https://jobsearch.api.jobtechdev.se/search?'
    q = 'occupation-group=' + af_id + '&municipality=' + lau_2_code_2015 + '&offset=0&limit=1'
    return job_ads_url + q


def job_ad_finder():
    citys = City.objects.all()
    for city_obj in citys:
        job_types = Job_type.objects.all()
        for job_type in job_types:
            job_type_code = str(job_type.af_id)
            url = job_ads_url_maker(str(city_obj.lau_2_code_2015), job_type_code)
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # check for http errors
            json_response = json.loads(response.content.decode('utf8'))
            if json_response['total']['value'] > 0:
                # print(json_response['total']['value'])#print total
                # print(json_response['hits'])
                for hit in json_response['hits']:
                    if hit['application_details']['url'] != None:
                        # print(hit['application_details']['url'])#print anons url
                        url = hit['application_details']['url']
                        id = hit['id']
                        title = hit['headline']
                        description = hit['description']['text']
                        company = hit['employer']['name']
                        city = City.objects.get(lau_2_code_2015=str(city_obj.lau_2_code_2015))
                        job_type = (Job_type.objects.get(af_id=job_type_code))
                        application_deadline = hit['application_deadline']
                        try:
                            print(title + "==>" + str(city))
                            Job_ad(af_id=id,
                                   application_deadline=application_deadline,
                                   title=title,
                                   description=description,
                                   city=city,
                                   company=company,
                                   ad_url=url,
                                   job_type=job_type).save()
                        except django.db.utils.IntegrityError:
                            print("Annos allready added")


test_search_loop_through_hits()
jobb_type_list_maker()
job_ad_finder()
