from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .task import *
import threading
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth # type: ignore
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required




def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
               return redirect('dashboard')
        else:
            messages.info(request, 'Invalid password or username')
            return redirect(request.get_full_path())
    else:
        template = 'login.html'
        return render(request, template)
    

def logout(request):
    auth.logout(request)
    return redirect('/')


# Create your views here.
def home(request):
    template = 'home.html'
    return render(request, template)

@login_required(login_url='login/')
def dashboard(request):
        count_website = WesiteModel.objects.count()
        count_openai = OpenaiAPIModel.objects.count()
        count_youtube = YoutubeAPIModel.objects.count()
        count_bulkpost = BulkKeywordModel.objects.count()
        count_singlepost = SingleKeywordModel.objects.count()
        context = {'count_website':count_website, 'count_openai':count_openai, 'count_youtube':count_youtube, 'count_bulkpost':count_bulkpost, 'count_singlepost':count_singlepost }
        template = 'dashboard.html'
        return render(request, template, context=context)
    
@login_required(login_url='login/')
def OpenaiAPI(request):
        api_data = OpenaiAPIModel.objects.all()
        template = 'openaiapi.html'
        if request.method == 'POST':
            form = OpenaiAPIForm(request.POST)
            context = {'openaiapi_form':form}
            if form.is_valid():
                name = form.cleaned_data['name']
                API_Key = form.cleaned_data['apikey']
                engine = form.cleaned_data['api_engine']
                obj = OpenaiAPIModel(name=name, API_Key=API_Key, engine=engine)
                obj.save()
                return redirect('/api')
            else:
                return redirect('/api')
                    
        else:
            form = OpenaiAPIForm()
            context = {'openaiapi_form':form, 'api_data':api_data}
            return render(request, template, context=context)
        
    
@login_required(login_url='login/')
def YoutubeAPI(request):
        api_data = YoutubeAPIModel.objects.all()
        template = 'youtubeapi.html'
        if request.method == 'POST':
            form = YoutubeAPIForm(request.POST)
            context = {'youtubeapi_form':form}
            if form.is_valid():
                name = form.cleaned_data['name']
                API_Key = form.cleaned_data['apikey']
                obj = YoutubeAPIModel(name=name, API_Key=API_Key)
                obj.save()
                return redirect('/youtubeapi')
            else:
                return redirect('/youtubeapi')
                    
        else:
            form = YoutubeAPIForm()
            context = {'youtubeapi_form':form, 'api_data':api_data}
            return render(request, template, context=context)


@login_required(login_url='login/')
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


@login_required(login_url='login/')   
def single_website(request, website_id):
        template = "single_website.html"
        single_website = WesiteModel.objects.get(pk=website_id)
        context = {'single_website': single_website,'website_id': website_id}
        return render(request, template, context)

@login_required(login_url='login/') 
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


@login_required(login_url='login/') 
def delete_website(request, website_id):
        website = WesiteModel.objects.get(pk=website_id)
        website.delete()
        return redirect('/website')

@login_required(login_url='login/') 
def delete_api(request, api_id):
        api = OpenaiAPIModel.objects.get(pk=api_id)
        api.delete()
        return redirect('/api')

@login_required(login_url='login/') 
def delete_youtube_api(request, api_id):
        api = YoutubeAPIModel.objects.get(pk=api_id)
        api.delete()
        return redirect('/youtubeapi')


@login_required(login_url='login/') 
def delete_completed_bulk_post(request, post_id):
        api = BulkKeywordModel.objects.get(pk=post_id)
        api.delete()
        return redirect('/completepost')
    

@login_required(login_url='login/')    
def delete_completed_single_post(request, post_id):
        api = SingleKeywordModel.objects.get(pk=post_id)
        api.delete()
        return redirect('/completepost')

@login_required(login_url='login/') 
def delete_error_bulk_post(request, post_id):
        api = BulkKeywordModel.objects.get(pk=post_id)
        print(api)
        api.delete()
        return redirect('/errorpost')
    

@login_required(login_url='login/')    
def delete_error_single_post(request, post_id):
        api = SingleKeywordModel.objects.get(pk=post_id)
        api.delete()
        return redirect('/errorpost')


@login_required(login_url='login/')    
def delete_pending_bulk_post(request, post_id):
        api = BulkKeywordModel.objects.get(pk=post_id)
        api.delete()
        return redirect('/bulkpost')
    
@login_required(login_url='login/')    
def delete_pending_single_post(request, post_id):
        api = SingleKeywordModel.objects.get(pk=post_id)
        api.delete()
        return redirect('/singlepost')    

scheduler_thread = None
@login_required(login_url='login/')   
def bulkpost(request):
        template = 'bulkpost.html'
        website = WesiteModel.objects.all()
        openaiapi = OpenaiAPIModel.objects.all()
        youtubeapi = YoutubeAPIModel.objects.all()
        keyword_pending = BulkKeywordModel.objects.filter(status='Pending')
        context = {'keyword_pending': keyword_pending, 'openaiapi':openaiapi, 'youtubeapi':youtubeapi, 'website':website}
        
        if request.method == 'POST':
            try:
                keyword_list = request.POST.get('keyword_list')
                keywords = keyword_list.split('\n')
                
                website_id = request.POST['website_id']
                url = WesiteModel.objects.get(pk=website_id).website_url
                username = WesiteModel.objects.get(pk=website_id).username
                app_pass = WesiteModel.objects.get(pk=website_id).app_pass
                
                openaiapi_id = request.POST['openaiapi_id']
                openai_key = OpenaiAPIModel.objects.get(pk=openaiapi_id).API_Key
                openai_engine = OpenaiAPIModel.objects.get(pk=openaiapi_id).engine
                
                try:
                    youtubeapi_id = request.POST['youtubeapi_id']
                    youtube_key = YoutubeAPIModel.objects.get(pk=youtubeapi_id).API_Key 
                except:
                    youtube_key = ''
                
                category = request.POST['category']
                status = request.POST['status']
                
                print('website_url : ',url)
                print('website_username : ',username)
                print('website_app_pass : ',app_pass)
                print('openai_api_key : ',openai_key)
                print('youtube_api_key : ',youtube_key)
                print('category : ', category)
                print('status : ', status)
                print('openai_engine : ', openai_engine)
                
                for keyword in keywords:
                    keyword = keyword.strip()
                    if keyword:
                        BulkKeywordModel.objects.create(name=keyword, status='Pending')

                global scheduler_thread
                if scheduler_thread is None or not scheduler_thread.is_alive():
                    # Start the task scheduler in a separate thread
                    scheduler_thread = threading.Thread(target=BulkKeywordsJob, args=(url, username, app_pass, openai_key, openai_engine, youtube_key, category, status))
                    scheduler_thread.start()
                return redirect('bulkpost')
            except:
                return redirect('bulkpost')
        else:
            return render(request, template, context=context)


scheduler_thread2 = None
@login_required(login_url='login/')     
def singlepost(request):
        website = WesiteModel.objects.all()
        website = WesiteModel.objects.all()
        openaiapi = OpenaiAPIModel.objects.all()
        youtubeapi = YoutubeAPIModel.objects.all()
        keyword_pending = SingleKeywordModel.objects.filter(status='Pending')
        context = {'keyword_pending': keyword_pending, 'openaiapi':openaiapi, 'youtubeapi':youtubeapi, 'website':website}
        template = 'singlepost.html'
        if request.method == 'POST':
            try:
                keyword = request.POST['keyword']
                outline = request.POST['outline']
                website_id = request.POST['website_id']
                url = WesiteModel.objects.get(pk=website_id).website_url
                username = WesiteModel.objects.get(pk=website_id).username
                app_pass = WesiteModel.objects.get(pk=website_id).app_pass
                
                openaiapi_id = request.POST['openaiapi_id']
                openai_key = OpenaiAPIModel.objects.get(pk=openaiapi_id).API_Key
                openai_engine = OpenaiAPIModel.objects.get(pk=openaiapi_id).engine
                
                try:
                    youtubeapi_id = request.POST['youtubeapi_id']
                    youtube_key = YoutubeAPIModel.objects.get(pk=youtubeapi_id).API_Key 
                except:
                    youtube_key = ''
                
                category = request.POST['category']
                status = request.POST['status']
                
                SingleKeywordModel.objects.create(name=keyword, outline=outline, status='Pending')
                
                print('website_url : ',url)
                print('website_username : ',username)
                print('website_app_pass : ',app_pass)
                print('openai_api_key : ',openai_key)
                print('youtube_api_key : ',youtube_key)
                print('category : ', category)
                print('status : ', status)
                print('openai_engine : ', openai_engine)
                
                global scheduler_thread2
                if scheduler_thread2 is None or not scheduler_thread2.is_alive():
                      # Start the task scheduler in a separate thread
                      scheduler_thread2 = threading.Thread(target=SingleKeywordsJob, args=(url, username, app_pass, openai_key, openai_engine, youtube_key, category, status))
                      scheduler_thread2.start()
                return redirect('singlepost')
            except:
                return redirect('singlepost')
        else:   
            redirect('singlepost')
            
        return render(request, template, context=context)

@login_required(login_url='login/') 
def completepost(request):
        BulkKeyword = BulkKeywordModel.objects.filter(status='Completed').order_by('name')
        SingleKeyword = SingleKeywordModel.objects.filter(status='Completed').order_by('name')
        context = {'BulkKeyword':BulkKeyword, 'SingleKeyword':SingleKeyword}
        template = 'completepost.html'
        return render(request, template, context=context)

@login_required(login_url='login/')    
def errorpost(request):
        BulkKeyword = BulkKeywordModel.objects.filter(status='Failed').order_by('name')
        SingleKeyword = SingleKeywordModel.objects.filter(status='Failed').order_by('name')
        context = {'BulkKeyword':BulkKeyword, 'SingleKeyword':SingleKeyword}
        template = 'errorpost.html'
        return render(request, template, context=context)
    
@login_required(login_url='login/')
def single_post_view(request, post_id):
    templeate = 'single_post_view.html'
    single_post = SingleKeywordModel.objects.get(pk=post_id)
    context = {'single_post':single_post}
    return render(request, templeate, context=context)

@login_required(login_url='login/')
def bulk_post_view(request, post_id):
    templeate = 'bulk_post_view.html'
    bulk_post = BulkKeywordModel.objects.get(pk=post_id)
    context = {'bulk_post':bulk_post}
    return render(request, templeate, context=context)