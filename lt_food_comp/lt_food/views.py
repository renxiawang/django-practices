# coding=utf-8
# Create your views here.
import ImageFile

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import Http404
from django.conf import settings

from lt_food.models import News
from lt_food.models import User
from lt_food.models import Product
from lt_food.models import SiteInfo

def index(request):
    ''' Index page '''

    latest_news_list = News.objects.all().order_by('-date')[:5]
    recommend_products_list = Product.objects.filter(category__startswith=u'推荐')
    return render_to_response('index.html', {'latest_news_list': latest_news_list, 'recommend_products_list': recommend_products_list, 'title': 'LT食品—首页'})

def login(request):
    ''' login page '''

    return render_to_response('login.html', context_instance=RequestContext(request))

def logout(request):
    ''' logout '''
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render_to_response('login.html', context_instance=RequestContext(request))

@csrf_protect
def verify_admin(request):
    ''' verify login user '''

    u_name = request.POST['username']
    u_password = request.POST['password']

    try:
        u = User.objects.get(name=u_name)
        if u.password == u_password:
            request.session['uid'] = u.id
    except:
        u = None

    if u:
        return HttpResponseRedirect('../admin/news')
    else:
        # raise Http404
        return render_to_response('login.html', {'message': 'Account information incorrect'}, context_instance=RequestContext(request))

@csrf_protect
def admin(request, selected=''):
    ''' admin functions:
        1. manage news
        2. manage products
        3. manage site information
    '''
    try:
        u = User.objects.get(id=request.session['uid'])
    except:
        u = None
        return render_to_response('login.html', {'message': 'Not login yet.'}, context_instance=RequestContext(request))

    # default page : news
    if selected == '':
        selected = 'news'

    # add new news
    if selected == 'new-news':
        new_news(request, u)
        selected = 'news'

    # modify news
    if selected == 'modify-news':
        modify_news(request)
        selected = 'news'

    # add new products
    if selected == 'new-product':
        new_products(request, u)
        selected = 'products'

    if selected == 'modify-product':
        modify_product(request)
        selected = 'products'

    # read record lists of news/products/site
    if selected == 'news':
        record_list = News.objects.all().order_by('-date')
    elif selected == 'products':
        record_list = Product.objects.all().order_by('id')
    elif selected == 'site':
        record_list = SiteInfo.objects.all().order_by('id')
    
    return render_to_response('admin.html', {'record_list': record_list, 'title': 'LT食品—后台管理', 'selected': selected}, context_instance=RequestContext(request))

def new_news(request, user):
    ''' add new news to database '''

    n = News(title=request.POST['news-title'], content=request.POST['news-title'], date=timezone.now(), publisher=user)
    n.save()

def modify_news(request):
    ''' modify existing news '''

    News.objects.filter(id=request.POST['news-id']).update(title=request.POST['modify-title'], content=request.POST['modify-content'])
    
def del_news(request, news_id):
    News.objects.filter(id=news_id).delete()
    record_list = News.objects.all().order_by('-date')
    return render_to_response('admin.html', {'record_list': record_list, 'title': 'LT食品—后台管理', 'selected': 'news'}, context_instance=RequestContext(request))

def new_products(request, user):
    ''' add new products to database '''

    f = request.FILES['product-pic']
    parser = ImageFile.Parser()
    for chunk in f.chunks():
        parser.feed(chunk)
    pic = parser.close()

    path = settings.LT_FOOD_DIR + '/product-imgs/' + request.FILES['product-pic'].name
    pic.save(path)

    p = Product(category=request.POST['product-category'], name=request.POST['product-name'], abstract=request.POST['product-abstract'], notice=request.POST['product-notice'], pic=request.FILES['product-pic'].name, publisher=user)
    p.save()

def modify_product(request):
    if len(request.FILES) != 0:
        f = request.FILES['modify-product-pic']
        parser = ImageFile.Parser()
        for chunk in f.chunks():
            parser.feed(chunk)
        pic = parser.close()

        path = settings.LT_FOOD_DIR + '/product-imgs/' + request.FILES['modify-product-pic'].name
        pic.save(path)
        
        Product.objects.filter(id=request.POST['product-id']).update(category=request.POST['modify-product-category'], name=request.POST['modify-product-name'], abstract=request.POST['modify-product-abstract'], notice=request.POST['modify-product-notice'], pic=request.FILES['modify-product-pic'].name)
    else:
        Product.objects.filter(id=request.POST['product-id']).update(category=request.POST['modify-product-category'], name=request.POST['modify-product-name'], abstract=request.POST['modify-product-abstract'], notice=request.POST['modify-product-notice'])

def del_product(request, product_id):
    Product.objects.filter(id=product_id).delete()
    record_list = Product.objects.all().order_by('id')
    return render_to_response('admin.html', {'record_list': record_list, 'title': 'LT食品—后台管理', 'selected': 'products'}, context_instance=RequestContext(request))
    
def about(request, selected):
    ''' about page '''

    if selected=='':
        selected = 'intro'

    comp_intro = SiteInfo.objects.filter(title__startswith=u"企业简介")[0]
    market_target = SiteInfo.objects.filter(title__startswith=u"经营范围")[0]
    mission = SiteInfo.objects.filter(title__startswith=u"经营理念")[0]
    culture = SiteInfo.objects.filter(title__startswith=u"管理文化")[0]

    return render_to_response('about.html', {'comp_intro': comp_intro, 'market_target': market_target, 'mission': mission, 'culture': culture, 'selected': selected, 'title': 'LT食品—关于我们'})

def products(request, selected):
    ''' products page '''

    if selected == '':
        selected = 'all'
    
    if selected == 'all':
        products_list = Product.objects.all().order_by('id')
    elif selected == 'recommend':
        products_list = Product.objects.filter(category__startswith=u'推荐')
    elif selected == 'jujube':
        products_list = Product.objects.filter(category__startswith=u'枣')
    elif selected == 'plum':
        products_list = Product.objects.filter(category__startswith=u'梅')
    
    return render_to_response('products.html', {'products_list': products_list, 'selected': selected, 'title': 'LT食品—产品展示'})

def contact(request):
    ''' contact page '''

    return render_to_response('contact.html', {'title': 'LT食品—联系我们'})

def news(request, news_id):
    ''' news page '''
    n = News.objects.get(id=news_id)
    return render_to_response('news.html', {'news': n})