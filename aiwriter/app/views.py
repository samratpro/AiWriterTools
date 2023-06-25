from django.shortcuts import render, redirect
from .forms import *
from .models import *


# Create your views here.
def home(request):
    template = 'home.html'
    return render(request, template)

def dashboard(request):
    template = 'dashboard.html'
    return render(request, template)

def website(request):
    website_data = WesiteModel.objects.all()
    template = 'website.html'
    if request.method == 'POST':
        form = WebsiteForms(request.POST)
        context = {'website_form':form}
        if form.is_valid():
            website_name = form.cleaned_data['website_name']
            website_url = form.cleaned_data['website_url']
            username = form.cleaned_data['username']
            app_pass = form.cleaned_data['app_pass']
            obj = WesiteModel(website_name=website_name, website_url=website_url, username=username, app_pass=app_pass)
            obj.save()
            return redirect('/website')
        else:
            return redirect('/website')
            
    else:
        form = WebsiteForms()
        context = {'website_form':form, 'website_data':website_data}
        return render(request, template, context=context)
    
def single_website(request, website_id):
    template = "single_website.html"
    single_website = WesiteModel.objects.get(pk=website_id)
    context = {'single_website': single_website,'website_id': website_id}
    return render(request, template, context)

def update_website(request, website_id):
    template = "update_website.html"
    website = WesiteModel.objects.get(pk=website_id)

    if request.method == "POST":
        update_form = WebsiteForms(request.POST)
        if update_form.is_valid():
            website.website_name = update_form.cleaned_data['website_name']
            website.website_url = update_form.cleaned_data['website_url']
            website.username = update_form.cleaned_data['username']
            website.app_pass = update_form.cleaned_data['app_pass']
            website.save()
            return redirect('/website')
    else:
        update_form = WebsiteForms(initial={
            'website_name': website.website_name,
            'website_url': website.website_url,
            'username': website.username,
            'app_pass': website.app_pass
        })
    context = {'update_form': update_form,'website_id': website_id}
    return render(request, template, context)

def delete_website(request, website_id):
    website = WesiteModel.objects.get(pk=website_id)
    website.delete()
    return redirect('/website')


def bulkpost(request):
    template = 'bulkpost.html'
    keyword_pending = BulkKeywordModel.objects.filter(status='Pending')
    context = {'keyword_pending': keyword_pending}
    if request.method == 'POST':
        keyword_list = request.POST.get('keyword_list')
        keywords = keyword_list.split('\n')

        for keyword in keywords:
            keyword = keyword.strip()
            if keyword:
                BulkKeywordModel.objects.create(name=keyword)

        return redirect('bulkpost')
    else:
        return render(request, template, context=context)  
    
 

def singlepost(request):
    website = WesiteModel.objects.all()
    template = 'singlepost.html'
    context = {'website':website}
    if request.method == 'POST' and 'keyword' in request.POST and 'outline' in request.POST and 'website_id' in request.POST:
        keyword = request.POST['keyword']
        outline = request.POST['outline']
        website_id = request.POST['website_id']
        targeted_website = WesiteModel.objects.get(pk=website_id)
        website_url = targeted_website.website_name
        website_username = targeted_website.username
        website_app_pass = targeted_website.app_pass
        
    return render(request, template, context=context)

def completepost(request):
    template = 'completepost.html'
    return render(request, template)