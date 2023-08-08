# cron.py
from .models import *
from time import sleep
import openai
from random import choice
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import requests
import shutil
import os
import json
import base64
from time import sleep
from googleapiclient.discovery import build
from bing_image_downloader import downloader
import people_also_ask
import re


def BulkKeywordsJob(url, username, app_pass, openai_api, engine, youtube_api, cat_name, post_status):
    pending_keywords = BulkKeywordModel.objects.filter(status='Pending')
    
    openai_key = openai_api.strip()
    website_url = url.strip()
    Username = username.strip()
    App_pass = app_pass.strip()
    status = post_status.strip()
    category_name = cat_name.strip()
    
    print(openai_key)
    print(website_url)
    
    # Prompt list
    outline_prompt = 'Write outline on this topic'
    outline_prompt_format= 'outline must be H2 : format, not underscore, not symbol, not hyphen, not number and no indentation, under each H2 : will have 4 H3 : not need sub heading for H3 :\n and an important command is, outlines not answer \n and another important command is, do not give me me "Introduction" and "Conclusion, each heading length must be less than 7 words"'
    paragraph_prompt = 'Write article paragraph section, interesting, and organized way like human writing but not unnecessary words and do not mention keyword and directly give answer without any similes'
    paragraph_prompt_instruction = 'You are content writing expert output length will be 120 words and 12 to 15 words will have per sentence'
    
    # Wordpress posting code-----------------
    json_url = website_url + 'wp-json/wp/v2'
    token = base64.standard_b64encode((Username + ':' + App_pass).encode('utf-8'))  # we have to encode the usr and pw
    headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
    
    def image_operation_bing(command):
        print('Image operation ..............')
        try:
            os.mkdir('bulkimg')
        except FileExistsError:
            pass
        try:
            downloader.download(command, limit=1, output_dir='bulkimg', filter='.jpg' )
            try:
                im = Image.open('bulkimg/' +command +'/Image_1.jpg')
            except:
                try:
                    im = Image.open('bulkimg/' +command +'/Image_1.png')
                except:
                    im = Image.open('bulkimg/' +command +'/Image_1.JPEG')

            # Define the desired size
            desired_size = (670, 330)
            # Calculate the cropping area based on the desired size
            width, height = im.size
            left = (width - desired_size[0]) / 2
            upper = (height - desired_size[1]) / 2
            right = (width + desired_size[0]) / 2
            lower = (height + desired_size[1]) / 2

            # Crop the image
            cropped_image = im.crop((left, upper, right, lower)) # type: ignore
            cropped_image.save('bulkimg/' +command +'.jpg')
        except:
            pass

    
    def body_img(command, bulkmodel):
        bulkmodel.error = 'Body Img...'
        bulkmodel.save()
        image_operation_bing(command)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            print(' Body IMG : --------- ',image)
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            print('Body Image:\n.......\n.........\n.........\n', image_wp, '...........\n.........\n.....\n')
            return image_wp
        except:
            return ''

    def feature_image(command, bulkmodel):
        bulkmodel.error = 'Feature Img...'
        bulkmodel.save()
        image_operation_bing(command)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            print(' Body IMG : --------- ',image)
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            f_img = [post_id, image_wp]
            return f_img
        except:
            f_img = [0, '']
            return f_img 
        

    def text_format(text):
        print('Text formating .................')
        if len(text) > 0:
            rc1 = choice([3, 4])
            rc2 = choice([10, 11])
            rc3 = choice([16, 17])
            p_format = text.replace('?', '?---').replace('.', '.---').replace('!', '!---').strip().split(sep='---')
            p = '<p>' + ''.join(p_format[:rc1]) + '</p>' + '<p>' + ''.join(p_format[rc1:7]) + '</p>' + '<p>' + ''.join(p_format[7:rc2]) + '</p>' + '<p>' + ''.join(p_format[rc2:13]) + '</p>' + '<p>' + ''.join(p_format[13:rc3]) + '</p>' + '<p>' + ''.join(p_format[rc3:20]) + '</p>' + '<p>' + ''.join(p_format[20:]) + '</p>'
            text = p.replace('  ', ' ').replace('<p></p>', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p> ','<p>').replace('\n','').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace('9.', '').replace('10.', '').replace('<p>  ','<p>').replace('<p> ','<p>').replace('.','. ').replace('.  ','. ').replace('!!','')
            return text
        else:
            return 'Text dose not Generated from OpenAI' 

    def keyword_format(text):
        print('Text formating .................')
        if len(text) > 0:
            rc1 = choice([3, 4])
            rc2 = choice([10, 11])
            rc3 = choice([16, 17])
            p_format = text.replace('?', '?---').replace('.', '.---').replace('!', '!---').strip().split(sep='---')
            p = '<p>' + ''.join(p_format[:rc1]) + '</p>' + '<p>' + ''.join(p_format[rc1:7]) + '</p>' + '<p>' + ''.join(p_format[7:rc2]) + '</p>' + '<p>' + ''.join(p_format[rc2:13]) + '</p>' + '<p>' + ''.join(p_format[13:rc3]) + '</p>' + '<p>' + ''.join(p_format[rc3:20]) + '</p>' + '<p>' + ''.join(p_format[20:]) + '</p>'
            text = p.replace('  ', ' ').replace('<p></p>', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p> ','<p>').replace('\n','').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace('9.', '').replace('10.', '').replace('<p>  ','<p>').replace('<p> ','<p>').replace('.','. ').replace('.  ','. ').replace('!!','')
            return text
        else:
            return 'Text dose not Generated from OpenAI' 
        
    
    openai.api_key = openai_key
    def text_render(prompt, bulkmodel, temp=0.7):
        try:
            res = openai.Completion.create(model=engine.strip(),prompt=prompt,temperature=temp,max_tokens=2000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
            text = res['choices'][0]['text'].strip() # type: ignore
            bulkmodel.error = 'Text rendering...'
            bulkmodel.save()
            print('Text render .................')
            return text
        except:
            sleep(30)
            try:
                res = openai.Completion.create(model=engine.strip(),prompt=prompt,temperature=1.5,max_tokens=2000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
                text = res['choices'][0]['text'].strip() # type: ignore
                bulkmodel.error = 'Text rendering...'
                bulkmodel.save()               
                print('Text render .................')
                return text
            except:
                sleep(60)
                try:
                    res = openai.Completion.create(model=engine.strip(),prompt=prompt,temperature=1.5,max_tokens=2000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
                    text = res['choices'][0]['text'].strip() # type: ignore
                    bulkmodel.error = 'Text rendering...'
                    bulkmodel.save()  
                    print('Text render .................')
                    return text
                except Exception as oops:
                    print('Text render fail .................')
                    bulkmodel.error = 'OpenAI error and error Message is : ' + str(oops)
                    bulkmodel.status = 'Failed'
                    bulkmodel.save()
                    return 'openaierror'
    
    
    def formated_outline(keyword, bulkmodel):
        bulkmodel.error = 'Outline Formating...'
        bulkmodel.save()  
        while True:
            outline = text_render(f'{outline_prompt} """{keyword}""" \n{outline_prompt_format}\n H1: {keyword}', bulkmodel)
            if 'h2' in outline or 'H2' in outline or outline == 'openaierror':
                break
        outlines = list()
        for line in outline.splitlines():
            if len(line) > 1 and not 'introduction' in line.lower() and not 'objective' in line.lower() and not 'conclusion' in line.lower():
                if 'h2' in line.lower():
                    line_format = line.replace('H2','').replace('h2','').replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h3>'+line_format.capitalize()+'</h3>')
                else:
                    line_format = line.replace('H3','').replace('h3','').replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h4>'+line_format.capitalize()+'</h4>')
        return outlines
    
    
    def content_body(keyword, bulkmodel):
        print('Content body .................')
        bulkmodel.error = 'Content Body...'
        bulkmodel.save()  
        outlines = formated_outline(keyword, bulkmodel)
        print(outlines)
        prompt_remember = ''
        content_body_data = ''
        for heading in outlines:
            prompt_remember = heading
            if 'h3' in heading.lower():
                clean_heading = heading.replace('H3', '').replace('h3', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').strip()
                print(f'Para Section H2 : {heading} .................')
                body_img_src = body_img(clean_heading.strip() + ' '+keyword.strip(), bulkmodel) 
                section = text_format(text_render(f'{paragraph_prompt} \n Prompt Rember : {prompt_remember}\n, article title is : {keyword}, heading is : {clean_heading} \n{paragraph_prompt_instruction}\n', bulkmodel))
                prompt_remember = section
                content_body_data += heading + body_img_src + section
            else:
                print(F'Para Section H3 : {heading}.................')
                clean_heading = heading.replace('H4', '').replace('h4', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').replace('H4','').replace('h4','').strip()
                section = text_format(text_render(f'{paragraph_prompt} \n Prompt Rember : {prompt_remember}\n, article title is : {keyword}, heading is : {clean_heading} \n{paragraph_prompt_instruction}\n', bulkmodel))
                prompt_remember = section
                content_body_data += heading + section
        print('Content body done .................')
        return content_body_data   
    
    
    def create_category(cat_name, bulkmodel):
        bulkmodel.error = 'Category...'
        bulkmodel.save()  
        print('Category .................') 
        id = 0
        if len(cat_name) > 0:
            data = {"name":cat_name}
            try:
                cat = requests.post(json_url + '/categories', headers=headers, json=data)
                id = str(json.loads(cat.content.decode('utf-8'))['id'])
            except KeyError:
                cat = requests.get(json_url + '/categories', headers=headers)
                cat_id = json.loads(cat.content.decode('utf-8'))
                for cat in cat_id:
                    if cat_name.lower() == cat['name'].lower():
                        id = str(cat['id'])
        return id  
    
    def youtubevid(self, bulkmodel):
        bulkmodel.error = 'Youtube...'
        bulkmodel.save()  
        print('Youtube API .................')
        if len(youtube_api) > 0:
            youtube = build('youtube', 'v3', developerKey=youtube_api.strip())
            try:
                request = youtube.search().list(q=self, part='snippet', type='video', maxResults=1)
                res = request.execute()
                id = res['items'][0]['id']['videoId']
                youtube_url = '<!-- wp:html --><figure  style="text-align: center"><iframe width="640" height="360" src="https://www.youtube.com/embed/' + id + '?rel=0&amp;enablejsapi=1"></iframe></figure><!-- /wp:html --><!-- wp:separator {"align":"center"} --><hr class="wp-block-separator aligncenter"/><!-- /wp:separator -->'
            except:
                youtube_url = ' *** Youtube API Has Been Finished *** '
            return youtube_url
        else:
            return ''

    def faq(keyword, bulkmodel):
        print('FAQ .................')
        bulkmodel.error = 'FAQ...'
        bulkmodel.save()  
        try:
            questions = people_also_ask.get_related_questions(keyword, 5)
        except:
            prompt = f'Topic:{keyword}\nWrite 5 related questions on this topic\n1.'
            outline = text_render(prompt, bulkmodel)
            questions = outline.splitlines()
        faq_body = ''
        schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type": "FAQPage","mainEntity":['
        for q in questions:
            q_filter = re.sub(r'[0-9]. ','', q)
            q_h3 = '<strong>'+q_filter.title()+'</strong>'
            q_body_raw = text_render(f'Write a short answer to this question within four sentence {q_filter}', bulkmodel)
            q_body = '<!-- wp:paragraph --><p>'+q_body_raw+'</p><!-- /wp:paragraph -->'
            faq_body += q_h3 + q_body
            question = '{"@type": "Question","name": "'+q_filter.replace('"','').title()+'",'
            ans = '"acceptedAnswer": {"@type": "Answer","text": "'+q_body_raw.replace('"','')+'"}},'
            schema += question + ans
        schema += ']}</script>' 
        schema_final = schema.replace(',]}</script>',']}</script>') 
        faq_final = faq_body + schema_final
        return faq_final
      
    
    for keyword_model in pending_keywords:
        keyword = keyword_model.name
        print('kw: ',keyword)
        introduction = keyword_format(text_render(f'Write a article introduction on this keyword intro start with technical terms, not like """are you""" and keyword must be include in output do not give me direct solution in intro section, intro last sentence must be interesting to read the full article, keyword: {keyword}\nand length approx 100 words\n', keyword_model, 0.5))
        if keyword_model.status != 'Failed':
            excerpt = text_render(f'Write a short summary,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 25 words\n',keyword_model, 0.5)
            conclusion_para = text_format(text_render(f'keyword: {keyword}\nWrite an web article bottom summary\n and length approx 60 words\n', keyword_model, 0.5))
            
            h2_title = text_render(f'Write an h2 heading on this keyword within 55 characters before starting the main article and the keyword must be directly included in the title \n keyword : {keyword}\n', keyword_model, 0.3).replace('"','').title()
            summary = text_render(f'Write a short briefing before starting the main article after intro,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 70 words\n',keyword_model, 0.5)
           
            feature_img_raw = feature_image(keyword.strip(), keyword_model)
            image_id = feature_img_raw[0]
            print('Feature Image id ..........:', image_id)
            img_source = feature_img_raw[1]
            print('Feature Image img_source ..........:', img_source)

           
            post_body = introduction + '<h2>'+ h2_title.replace('#','') +'</h2>' + img_source + summary + content_body(keyword, keyword_model) + youtubevid(keyword, keyword_model) + "<h4> FAQ's </h4>" + faq(keyword, keyword_model) + '<h2>Conclusion</h2>' + conclusion_para

            category_id = create_category(category_name, keyword_model)
            title = text_render(f'Write an SEO title on this keyword within 55 characters and the keyword must be directly included in the title \n keyword : {keyword}\n', keyword_model, 0.3).replace('"','').title()
            slug = keyword.replace(' ', '-')

            # Post Data
            if category_id == 0:
                post = {'title': title,'slug': slug,'status': status,'content': post_body,'format': 'standard','excerpt': excerpt,'featured_media': int(image_id)}
            else:
                post = {'title': title,'slug': slug,'status': status,'content': post_body,'categories': [category_id],'format': 'standard','excerpt': excerpt,'featured_media': int(image_id)}
                
            
            # Posting Request
            r = requests.post(json_url + '/posts', headers=headers, json=post)
            if r.status_code == 201:
                keyword_model.error = 'No error'
                keyword_model.status = 'Completed'
                keyword_model.content = post_body
                keyword_model.save()
                print('completed, kw:', keyword)
            else:
                keyword_model.error = str(f'Wordpress Error and, error Status Code is : {r.status_code}')
                keyword_model.status = 'Failed'
                keyword_model.save()
                print('Faild, kw:', keyword)
            sleep(10)        
            shutil.rmtree('bulkimg')
    


def SingleKeywordsJob(url, username, app_pass, openai_api, engine, youtube_api, cat_name, post_status):
    pending_keywords = SingleKeywordModel.objects.filter(status='Pending')
    
    openai_key = openai_api.strip()
    website_url = url.strip()
    Username = username.strip()
    App_pass = app_pass.strip()
    status = post_status.strip()
    category_name = cat_name.strip()
    
    print(openai_key)
    print(website_url)
    
    # Prompt list
    outline_prompt = 'Write outline on this topic'
    outline_prompt_format= 'outline must be H2 : format, not underscore, not symbol, not hyphen, not number and no indentation, under each H2 : will have 4 H3 : not need sub heading for H3 :\n and an important command is, outlines not answer \n and another important command is, do not give me me "Introduction" and "Conclusion, each heading length must be less than 7 words"'
    paragraph_prompt = 'Write article paragraph section from this heading, interesting, and organized way like human writing but not unnessary words not long lenght'
    paragraph_prompt_instruction = 'Each output sentence will be short, meaningful and easy to read, that can understand elementary school student'
    
    # Wordpress posting code-----------------
    json_url = website_url + 'wp-json/wp/v2'
    token = base64.standard_b64encode((Username + ':' + App_pass).encode('utf-8'))  # we have to encode the usr and pw
    headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
    
    def image_operation_bing(command):
        print('Image operation ..............')
        try:
            os.mkdir('bulkimg')
        except FileExistsError:
            pass
        try:
            downloader.download(command, limit=1, output_dir='bulkimg', filter='.jpg' )
            try:
                im = Image.open('bulkimg/' +command +'/Image_1.jpg')
            except:
                try:
                    im = Image.open('bulkimg/' +command +'/Image_1.png')
                except:
                    im = Image.open('bulkimg/' +command +'/Image_1.JPEG')

            # Define the desired size
            desired_size = (670, 330)
            # Calculate the cropping area based on the desired size
            width, height = im.size
            left = (width - desired_size[0]) / 2
            upper = (height - desired_size[1]) / 2
            right = (width + desired_size[0]) / 2
            lower = (height + desired_size[1]) / 2

            # Crop the image
            cropped_image = im.crop((left, upper, right, lower)) # type: ignore
            cropped_image.save('bulkimg/' +command +'.jpg')
        except:
            pass

    
    def body_img(command, bulkmodel):
        bulkmodel.error = 'Body Img...'
        bulkmodel.save()
        image_operation_bing(command)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            print(' Body IMG : --------- ',image)
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            print('Body Image:\n.......\n.........\n.........\n', image_wp, '...........\n.........\n.....\n')
            return image_wp
        except:
            return ''
     
    def feature_image(command, bulkmodel):
        bulkmodel.error = 'Feature Img...'
        bulkmodel.save()
        image_operation_bing(command)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            print(' Body IMG : --------- ',image)
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            f_img = [post_id, image_wp]
            return f_img
        except:
            f_img = [0, '']
            return f_img     
     
     
        
    def text_format(text):
        print('Text formating .................')
        if len(text) > 0:
            rc1 = choice([3, 4])
            rc2 = choice([10, 11])
            rc3 = choice([16, 17])
            p_format = text.replace('?', '?---').replace('.', '.---').replace('!', '!---').strip().split(sep='---')
            p = '<p>' + ''.join(p_format[:rc1]) + '</p>' + '<p>' + ''.join(p_format[rc1:7]) + '</p>' + '<p>' + ''.join(p_format[7:rc2]) + '</p>' + '<p>' + ''.join(p_format[rc2:13]) + '</p>' + '<p>' + ''.join(p_format[13:rc3]) + '</p>' + '<p>' + ''.join(p_format[rc3:20]) + '</p>' + '<p>' + ''.join(p_format[20:]) + '</p>'
            text = p.replace('  ', ' ').replace('<p></p>', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p> ','<p>').replace('\n','').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace('9.', '').replace('10.', '').replace('<p>  ','<p>').replace('<p> ','<p>').replace('.','. ').replace('.  ','. ').replace('!!','')
            return text
        else:
            return 'Text dose not Generated from OpenAI'  

    def keyword_format(text):
        print('Text formating .................')
        if len(text) > 0:
            rc1 = choice([3, 4])
            rc2 = choice([10, 11])
            rc3 = choice([16, 17])
            p_format = text.replace('?', '?---').replace('.', '.---').replace('!', '!---').strip().split(sep='---')
            p = '<p>' + ''.join(p_format[:rc1]) + '</p>' + '<p>' + ''.join(p_format[rc1:7]) + '</p>' + '<p>' + ''.join(p_format[7:rc2]) + '</p>' + '<p>' + ''.join(p_format[rc2:13]) + '</p>' + '<p>' + ''.join(p_format[13:rc3]) + '</p>' + '<p>' + ''.join(p_format[rc3:20]) + '</p>' + '<p>' + ''.join(p_format[20:]) + '</p>'
            text = p.replace('  ', ' ').replace('<p></p>', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p> ','<p>').replace('\n','').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace('9.', '').replace('10.', '').replace('<p>  ','<p>').replace('<p> ','<p>').replace('.','. ').replace('.  ','. ').replace('!!','')
            return text
        else:
            return 'Text dose not Generated from OpenAI'  


    openai.api_key = openai_key
    def text_render(prompt, bulkmodel, temp=0.7):
        try:
            res = openai.Completion.create(model=engine.strip(),prompt=prompt,temperature=temp,max_tokens=2000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
            text = res['choices'][0]['text'].strip() # type: ignore
            bulkmodel.error = 'Text Render...'
            bulkmodel.save()  
            print('Text render .................')
            return text
        except:
            sleep(30)
            try:
                res = openai.Completion.create(model=engine.strip(),prompt=prompt,temperature=1.5,max_tokens=2000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
                text = res['choices'][0]['text'].strip() # type: ignore
                bulkmodel.error = 'Text Render...'
                bulkmodel.save()  
                print('Text render .................')
                return text
            except:
                sleep(60)
                try:
                    res = openai.Completion.create(model=engine.strip(),prompt=prompt,temperature=1.5,max_tokens=2000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
                    text = res['choices'][0]['text'].strip() # type: ignore
                    bulkmodel.error = 'Text Render...'
                    bulkmodel.save()  
                    print('Text render .................')
                    return text
                except Exception as oops:
                    print('Text render fail .................')
                    bulkmodel.error = 'OpenAI error and error Message is : ' + str(oops)
                    bulkmodel.status = 'Failed'
                    bulkmodel.save()
                    return 'openaierror'
    
    
    def formated_outline(keyword, outline, bulkmodel):
        bulkmodel.error = 'Outline Formating...'
        bulkmodel.save()  
        if len(outline) < 1:
          while True:
            outline = text_render(f'{outline_prompt} """{keyword}""" \n{outline_prompt_format}\n H1: {keyword}', bulkmodel)
            if 'h2' in outline or 'H2' in outline or outline == 'openaierror':
                break
        outlines = list()
        print(outline)
        for line in outline.splitlines():
            if len(line) > 1:
                if 'h3 ' in line.lower():
                    line_format = line.replace('H3','').replace('h3','').replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h3>'+line_format.strip().capitalize()+'</h3>')      
                if 'h4 ' in line.lower():
                    line_format = line.replace('H4','').replace('h4','').replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h4>'+line_format.strip().capitalize()+'</h4>')                                        
                else:
                    line_format = line.replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h2>'+line_format.strip().capitalize()+'</h2>')
        return outlines
        
    def faq(keyword, bulkmodel):
        print('FAQ .................')
        bulkmodel.error = 'FAQ...'
        bulkmodel.save()  
        try:
            questions = people_also_ask.get_related_questions(keyword, 5)
        except:
            prompt = f'Topic:{keyword}\nWrite 5 related questions on this topic\n1.'
            outline = text_render(prompt, bulkmodel)
            questions = outline.splitlines()
        faq_body = ''
        schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type": "FAQPage","mainEntity":['
        for q in questions:
            q_filter = re.sub(r'[0-9]. ','', q)
            q_h3 = '<strong>'+q_filter.title()+'</strong>'
            q_body_raw = text_render(f'Write a short answer to this question within four sentence {q_filter}', bulkmodel)
            q_body = '<!-- wp:paragraph --><p>'+q_body_raw+'</p><!-- /wp:paragraph -->'
            faq_body += q_h3 + q_body
            question = '{"@type": "Question","name": "'+q_filter.replace('"','').title()+'",'
            ans = '"acceptedAnswer": {"@type": "Answer","text": "'+q_body_raw.replace('"','')+'"}},'
            schema += question + ans
        schema += ']}</script>' 
        schema_final = schema.replace(',]}</script>',']}</script>') 
        faq_final = faq_body + schema_final
        return faq_final       
    
    def content_body(keyword,outline, bulkmodel):
        bulkmodel.error = 'Content Body...'
        bulkmodel.save()    
        print('Content body .................')
        outlines = formated_outline(keyword, outline, bulkmodel)
        print(outlines)
        prompt_remember = ''
        content_body_data = ''
        for heading in outlines:
            prompt_remember = heading
            if 'h3' in heading.lower():
                clean_heading = heading.replace('H3', '').replace('h3', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').strip()
                print(f'Para Section H2 : {heading} .................')
                body_img_src = body_img(clean_heading + ' '+keyword, bulkmodel)  
                section = text_format(text_render(f'{paragraph_prompt} \n Prompt Rember : {prompt_remember}\n, article title is : {keyword}, heading is : {clean_heading} \n{paragraph_prompt_instruction}\n', bulkmodel))
                prompt_remember = section
                content_body_data += heading + body_img_src + section
            else:
                print(F'Para Section H3 : {heading}.................')
                clean_heading = heading.replace('H4', '').replace('h4', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').replace('H4','').replace('h4','').strip()
                section = text_format(text_render(f'{paragraph_prompt} \n Prompt Rember : {prompt_remember}\n, article title is : {keyword}, heading is : {clean_heading} \n{paragraph_prompt_instruction}\n', bulkmodel))
                prompt_remember = section
                content_body_data += heading + section
        print('Content body done .................')
        return content_body_data   
    
    
    def create_category(cat_name, bulkmodel):
        bulkmodel.error = 'Ctegory...'
        bulkmodel.save()    
        print('Category .................') 
        id = 0
        if len(cat_name) > 0:
            data = {"name":cat_name}
            try:
                cat = requests.post(json_url + '/categories', headers=headers, json=data)
                id = str(json.loads(cat.content.decode('utf-8'))['id'])
            except KeyError:
                cat = requests.get(json_url + '/categories', headers=headers)
                cat_id = json.loads(cat.content.decode('utf-8'))
                for cat in cat_id:
                    if cat_name.lower() == cat['name'].lower():
                        id = str(cat['id'])
        return id  
    
    def youtubevid(self, bulkmodel):
        bulkmodel.error = 'Youtube...'
        bulkmodel.save()   
        print('Youtube API .................')
        if len(youtube_api) > 0:
            youtube = build('youtube', 'v3', developerKey=youtube_api.strip())
            try:
                request = youtube.search().list(q=self, part='snippet', type='video', maxResults=1)
                res = request.execute()
                id = res['items'][0]['id']['videoId']
                youtube_url = '<!-- wp:html --><figure  style="text-align: center"><iframe width="640" height="360" src="https://www.youtube.com/embed/' + id + '?rel=0&amp;enablejsapi=1"></iframe></figure><!-- /wp:html --><!-- wp:separator {"align":"center"} --><hr class="wp-block-separator aligncenter"/><!-- /wp:separator -->'
            except:
                youtube_url = ' *** Youtube API Has Been Finished *** '
            return youtube_url
        else:
            return ''
      
    
    for keyword_model in pending_keywords:
        keyword = keyword_model.name
        print('kw: ',keyword)
        introduction = keyword_format(text_render(f'Write a article introduction on this keyword intro start with technical terms, not like """are you""" and keyword must be include in output do not give me direct solution in intro section, intro last sentence must be interesting to read the full article, keyword: {keyword}\nand length approx 100 words\n', keyword_model, 0.5))
        if keyword_model.status != 'Failed':
            excerpt = text_render(f'Write a short summary,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 25 words\n',keyword_model, 0.5)
            conclusion_para = text_format(text_render(f'keyword: {keyword}\nWrite an web article bottom summary\n and length approx 60 words\n', keyword_model, 0.5))
            
            h2_title = text_render(f'Write an h2 heading on this keyword within 55 characters before starting the main article and the keyword must be directly included in the title \n keyword : {keyword}\n', keyword_model, 0.3).replace('"','').title()
            summary = text_render(f'Write a short briefing before starting the main article after intro,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 70 words\n',keyword_model, 0.5)
           
            feature_img_raw = feature_image(keyword, keyword_model)
            image_id = feature_img_raw[0]
            img_source = feature_img_raw[1]
            
            post_body = introduction + '<h2>'+h2_title.replace('#','')+'</h2>' + img_source + summary + content_body(keyword, keyword_model.outline, keyword_model) + youtubevid(keyword, keyword_model) + '<h4>Conclusion</h4>' + conclusion_para + "<h4>FAQs</h4>" + faq(keyword, keyword_model)

            category_id = create_category(category_name, keyword_model)
            title = text_render(f'Write an SEO title on this keyword within 55 characters and the keyword must be directly included in the title \n keyword : {keyword}\n', keyword_model, 0.3).replace('"','').title()
            slug = keyword.replace(' ', '-')

            # Post Data
            if category_id == 0:
                post = {'title': title,'slug': slug,'status': status,'content': post_body,'format': 'standard','excerpt': excerpt,'featured_media': int(image_id)}
            else:
                post = {'title': title,'slug': slug,'status': status,'content': post_body,'categories': [category_id],'format': 'standard','excerpt': excerpt,'featured_media': int(image_id)}
                
            
            # Posting Request
            r = requests.post(json_url + '/posts', headers=headers, json=post)
            if r.status_code == 201:
                keyword_model.error = 'No error'
                keyword_model.status = 'Completed'
                keyword_model.content = post_body
                keyword_model.save()
                print('completed, kw:', keyword)
            
            else:
                keyword_model.error = str(f'Error Status : {r.status_code}')
                keyword_model.status = 'Failed'
                keyword_model.save()
                print('Faild, kw:', keyword)
            sleep(10)        
            shutil.rmtree('bulkimg')
            
            