# coding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import Http404
from django.conf import settings

from collections import OrderedDict

import requests
import re
import mongodb
import stopwords

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

@csrf_protect
def list_search_results(request):
    keywords = request.POST['keywords']

    # segment words
    payload={'data': keywords, 'respond': 'json', 'ignore': 'yes'}
    r = requests.post("http://www.xunsearch.com/scws/api.php", data=payload)
    words = r.json()['words']

    tokens = []
    for one in words:
        tokens.append(one['word'])

    search_keywords = ' '.join(stopwords.del_stopwords(tokens))
    print search_keywords
    
    results = mongodb.find_matches(search_keywords)
    people = []

    for one in results:
        person_tmp = dict()
        person_tmp['score'] = one['score']
        person_tmp['id'] = one['obj']['_id']
        person_tmp['name'] = one['obj']['name']
        if 'description' in one['obj']:
            person_tmp['description'] = one['obj']['description'][0]['content'][0:90].strip() + '......'
        else:
            person_tmp['description'] = u'暂无介绍'

        people.append(person_tmp)

    return render_to_response('results.html', {'results': people, 'keywords':keywords, 'segmented_keywords': search_keywords}, context_instance=RequestContext(request))

@csrf_protect
def display_personal_details(request, pid):
    person = mongodb.find_one_person(pid)
    basic_info = {}
    work_exp = []
    edu_exp = []
    descriptions = []
    data_source = {}
    avatar = ''

    for k, v in person.iteritems():
        if k == 'dataSource':
            if v.find('baidu') != -1:
                data_source['baidu'] = v
            else:
                data_source['hudong'] = v
        elif k == 'photo':
            avatar = v
        elif k == 'description':
            descriptions = v
        elif k == 'workExperience':
            #work_exp = v[0]
            work_exp = v
        elif k == 'educations':
            #edu_exp = v[0]
            edu_exp = v
        elif k not in ['_id', 'baidu_id', 'hudong_id', 'timestamp', 'keywords', 'awards']:
            basic_info[k] = v
        else:
            pass

    print work_exp
    personal_details = dict()
    personal_details['basic_info'] = sort_basic_info(basic_info)
    personal_details['work_exp'] = work_exp
    personal_details['edu_exp'] = edu_exp
    personal_details['descriptions'] = descriptions
    personal_details['data_source'] = data_source
    personal_details['avatar'] = avatar

    return render_to_response('personal_details.html', personal_details, context_instance=RequestContext(request))

def sort_basic_info(basic_info):
    d = OrderedDict()
    
    if 'name' in basic_info:
        d[u'姓名'] = basic_info['name']
    if 'nickName' in basic_info:
        d[u'昵称'] = basic_info['nickName']
    if 'gender' in basic_info:
        d[u'性别'] = basic_info['gender']
    if 'nationality' in basic_info:
        d[u'国籍'] = basic_info['nationality']
    if 'race' in basic_info:
        d[u'民族'] = basic_info['race']
    if 'birthPlace' in basic_info:
        d[u'出生地'] = basic_info['birthPlace']
    if 'address' in basic_info:
        d[u'现居地址'] = basic_info['address']
    if 'birthday' in basic_info:
        d[u'生日'] = basic_info['birthday']
    if 'constellation' in basic_info:
        d[u'星座'] = basic_info['constellation']
    if 'politicalStatus' in basic_info:
        d[u'政治面貌'] = basic_info['politicalStatus']
    if 'height' in basic_info:
        d[u'身高'] = basic_info['height']
    if 'weight' in basic_info:
        d[u'体重'] = basic_info['weight']
    if 'BWH' in basic_info:
        d[u'三围'] = basic_info['BWH']
    
    return d