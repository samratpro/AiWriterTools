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
                im = Image.open('bulkimg/'+command+'/Image_1.jpg')
            except:
                try:
                    im = Image.open('bulkimg/'+command+'/Image_1.png')
                except:
                    im = Image.open('bulkimg/'+command+'/Image_1.JPEG')

            resized_im = im.resize((round(im.size[0] * 0.8), round(im.size[1] * 0.8)))
            resized_im.save('bulkimg/'+command+'.jpg')
        except:
            pass
    
    def body_img(command):
        image_operation_bing(command)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            return image_wp
        except:
            return ''

    def feature_image(command):
        image_operation_bing(command)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            img_id = json.loads(image.content.decode('utf-8'))['id']
            return img_id
        except:
            return 0  
        
    def text_format(text):
        print('Text formating .................')
        if len(text) > 0:
            rc1 = choice([2, 3])
            rc2 = choice([7, 8])
            rc3 = choice([12, 13])
            p_format = text.replace('?', '?---').replace('.', '.---').replace('!', '!---').strip().split(sep='---')
            p = '<p>' + ''.join(p_format[:rc1]) + '</p>' + '<p>' + ''.join(p_format[rc1:5]) + '</p>' + '<p>' + ''.join(p_format[5:rc2]) + '</p>' + '<p>' + ''.join(p_format[rc2:10]) + '</p>' + '<p>' + ''.join(p_format[10:rc3]) + '</p>' + '<p>' + ''.join(p_format[rc3:15]) + '</p>' + '<p>' + ''.join(p_format[15:]) + '</p>'
            text = p.replace('  ', ' ').replace('<p></p>', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p> ','<p>').replace('\n','').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace('9.', '').replace('10.', '').replace('<p>  ','<p>').replace('<p> ','<p>').replace('.','. ').replace('.  ','. ').replace('!!','')
            return text
        else:
            return 'Text dose not Generated from OpenAI'
    
    openai.api_key = openai_key
    def text_render(prompt):
        try:
            res = openai.Completion.create(model=engine.strip(),prompt=prompt,temperature=1.5,max_tokens=2000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
            text = res['choices'][0]['text'].strip() # type: ignore
            print('Text render .................')
            return text
        except Exception as oops:
            print('Text render fail .................')
            error = 'error from API Section :' + str(oops)
            return error
    
    
    def formated_outline(keyword):
        while True:
            outline = text_render(f'{outline_prompt} """{keyword}""" \n{outline_prompt_format}\n H1: {keyword}')
            if 'h2' in outline or 'H2' in outline:
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
                        outlines.append('<h4>'+' '.join(line_format.capitalize().split()[:7])+'</h4>')
        return outlines
    
    
    def content_body(keyword):
        print('Content body .................')
        outlines = formated_outline(keyword)
        print(outlines)
        prompt_remember = ''
        content_body_data = ''
        for heading in outlines:
            prompt_remember = heading
            if 'h3' in heading.lower():
                clean_heading = heading.replace('H3', '').replace('h3', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').strip()
                print(f'Para Section H2 : {heading} .................')
                section = text_format(text_render(f'{paragraph_prompt} \n Prompt Rember : {prompt_remember}\n, article title is : {keyword}, heading is : {clean_heading} \n{paragraph_prompt_instruction}\n'))
                prompt_remember = section
                content_body_data += heading + section
            else:
                print(F'Para Section H3 : {heading}.................')
                clean_heading = heading.replace('H4', '').replace('h4', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').replace('H4','').replace('h4','').strip()
                section = text_format(text_render(f'{paragraph_prompt} \n Prompt Rember : {prompt_remember}\n, article title is : {keyword}, heading is : {clean_heading} \n{paragraph_prompt_instruction}\n'))
                prompt_remember = section
                content_body_data += heading + section
        print('Content body done .................')
        return content_body_data   
    
    
    def create_category(cat_name):
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
    
    def youtubevid(self):
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

    def faq(keyword):
        print('FAQ .................')
        try:
            questions = people_also_ask.get_related_questions(keyword, choice([4,5,6]))
        except:
            prompt = f'Topic:{keyword}\nWrite 6 related questions on this topic\n1.'
            outline = text_render(prompt)
            questions = outline.splitlines()
        faq_body = ''
        schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type": "FAQPage","mainEntity":['
        for q in questions:
            q_filter = re.sub(r'[0-9]. ','', q)
            q_h3 = '<!-- wp:heading {"level":3} --><h3>'+q_filter+'</h3><!-- /wp:heading -->'
            q_body_raw = text_render(f'Write a short answer to this question with one or two sentence {q_filter}')
            q_body = '<!-- wp:paragraph --><p>'+q_body_raw+'</p><!-- /wp:paragraph -->'
            faq_body += q_h3 + q_body
            question = '{"@type": "Question","name": "'+q_filter.replace('"','')+'",'
            ans = '"acceptedAnswer": {"@type": "Answer","text": "'+q_body_raw.replace('"','')+'"}},'
            schema += question + ans
        schema += ']}</script>' 
        schema_final = schema.replace(',]}</script>',']}</script>') 
        faq_final = faq_body + schema + schema_final
        return faq_final
      
    
    for keyword_model in pending_keywords:
        keyword = keyword_model.name
        print('kw: ',keyword)
        excerpt = text_render(f'Write a short summary,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 25 words\n')
        introduction = text_format(text_render(f'Write interesting and attentionable blog Introduction,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 100 words\n'))
        conclusion_para = text_format(text_render(f'keyword: {keyword}\nWrite an web article bottom summary\n and length approx 60 words\n'))
        
        post_body = introduction + '<h2>'+keyword.title().replace('What ', '').replace('When ', '').replace('Which ', '').replace('How ', '').replace('Where ', '').replace('Why ', '').replace('Does ', '')+'</h2>' + content_body(keyword) + youtubevid(keyword) + "<h2> FAQ's </h2>" + faq(keyword) + '<H2>Conclusion</H2>' + conclusion_para

        image_id = feature_image(keyword)
        category_id = create_category(category_name)
        title = keyword.title()
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
        
        else:
            keyword_model.error = str(f'Error Status : {r.status_code}')
            keyword_model.status = 'Failed'
        sleep(10)        
        keyword_model.save()
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
                im = Image.open('bulkimg/'+command+'/Image_1.jpg')
            except:
                try:
                    im = Image.open('bulkimg/'+command+'/Image_1.png')
                except:
                    im = Image.open('bulkimg/'+command+'/Image_1.JPEG')

            resized_im = im.resize((round(im.size[0] * 0.8), round(im.size[1] * 0.8)))
            resized_im.save('bulkimg/'+command+'.jpg')
        except:
            pass
    
    def body_img(command):
        image_operation_bing(command)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            image_title = command.replace('-', ' ').split('.')[0]
            post_id = str(json.loads(image.content.decode('utf-8'))['id'])
            source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
            image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
            image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
            image3 = '<!-- /wp:image -->'
            image_wp = image1 + image2 + image3
            return image_wp
        except:
            return ''

    def feature_image(command):
        image_operation_bing(command)
        try:
            media = {'file': open('bulkimg/' + command + '.jpg', 'rb')}
            image = requests.post(json_url + '/media', headers=headers, files=media)
            img_id = json.loads(image.content.decode('utf-8'))['id']
            return img_id
        except:
            return 0  
        
    def text_format(text):
        print('Text formating .................')
        if len(text) > 0:
            rc1 = choice([2, 3])
            rc2 = choice([7, 8])
            rc3 = choice([12, 13])
            p_format = text.replace('?', '?---').replace('.', '.---').replace('!', '!---').strip().split(sep='---')
            p = '<p>' + ''.join(p_format[:rc1]) + '</p>' + '<p>' + ''.join(p_format[rc1:5]) + '</p>' + '<p>' + ''.join(p_format[5:rc2]) + '</p>' + '<p>' + ''.join(p_format[rc2:10]) + '</p>' + '<p>' + ''.join(p_format[10:rc3]) + '</p>' + '<p>' + ''.join(p_format[rc3:15]) + '</p>' + '<p>' + ''.join(p_format[15:]) + '</p>'
            text = p.replace('  ', ' ').replace('<p></p>', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p> ','<p>').replace('\n','').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace('9.', '').replace('10.', '').replace('<p>  ','<p>').replace('<p> ','<p>').replace('.','. ').replace('.  ','. ').replace('!!','')
            return text
        else:
            return 'Text dose not Generated from OpenAI'
    
    openai.api_key = openai_key
    def text_render(prompt):
        try:
            res = openai.Completion.create(model=engine.strip(),prompt=prompt,temperature=1.5,max_tokens=2000,top_p=1.0,frequency_penalty=0.0,presence_penalty=0.0,stop=['asdfasdf', 'asdasdf'])
            text = res['choices'][0]['text'].strip() # type: ignore
            print('Text render .................')
            return text
        except Exception as oops:
            print('Text render fail .................')
            error = 'error from API Section :' + str(oops)
            return error
    
    
    def formated_outline(keyword, outline):
        if len(outline) < 1:
          while True:
            outline = text_render(f'{outline_prompt} """{keyword}""" \n{outline_prompt_format}\n H1: {keyword}')
            if 'h2' in outline or 'H2' in outline:
                break
        outlines = list()
        print(outline)
        for line in outline.splitlines():
            if len(line) > 1:
                if 'h2' in line.lower():
                    line_format = line.replace('H2','').replace('h2','').replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h2>'+line_format.strip().capitalize()+'</h2>')
                if 'h3' in line.lower():
                    line_format = line.replace('H3','').replace('h3','').replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h3>'+' '.join(line_format.strip().capitalize().split()[:7])+'</h3>')                   
                else:
                    line_format = line.replace(':','').replace('-','').strip()
                    if len(line_format) > 0:
                        outlines.append('<h2>'+line_format.strip().capitalize()+'</h2>')
        return outlines
    
    
    def content_body(keyword,outline):
        print('Content body .................')
        outlines = formated_outline(keyword, outline)
        print(outlines)
        prompt_remember = ''
        content_body_data = ''
        for heading in outlines:
            prompt_remember = heading
            if 'h3' in heading.lower():
                clean_heading = heading.replace('H3', '').replace('h3', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').strip()
                print(f'Para Section H2 : {heading} .................')
                section = text_format(text_render(f'{paragraph_prompt} \n Prompt Rember : {prompt_remember}\n, article title is : {keyword}, heading is : {clean_heading} \n{paragraph_prompt_instruction}\n'))
                prompt_remember = section
                content_body_data += heading + section
            else:
                print(F'Para Section H3 : {heading}.................')
                clean_heading = heading.replace('H4', '').replace('h4', '').replace(':', '').replace('-', '').replace('/','').replace('<', '').replace('>', '').replace('H4','').replace('h4','').strip()
                section = text_format(text_render(f'{paragraph_prompt} \n Prompt Rember : {prompt_remember}\n, article title is : {keyword}, heading is : {clean_heading} \n{paragraph_prompt_instruction}\n'))
                prompt_remember = section
                content_body_data += heading + section
        print('Content body done .................')
        return content_body_data   
    
    
    def create_category(cat_name):
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
    
    def youtubevid(self):
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

    def faq(keyword):
        print('FAQ .................')
        try:
            questions = people_also_ask.get_related_questions(keyword, choice([4,5,6]))
        except:
            prompt = f'Topic:{keyword}\nWrite 6 related questions on this topic\n1.'
            outline = text_render(prompt)
            questions = outline.splitlines()
        faq_body = ''
        schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type": "FAQPage","mainEntity":['
        for q in questions:
            q_filter = re.sub(r'[0-9]. ','', q)
            q_h3 = '<!-- wp:heading {"level":3} --><h3>'+q_filter+'</h3><!-- /wp:heading -->'
            q_body_raw = text_render(f'Write a short answer to this question with one or two sentence {q_filter}')
            q_body = '<!-- wp:paragraph --><p>'+q_body_raw+'</p><!-- /wp:paragraph -->'
            faq_body += q_h3 + q_body
            question = '{"@type": "Question","name": "'+q_filter.replace('"','')+'",'
            ans = '"acceptedAnswer": {"@type": "Answer","text": "'+q_body_raw.replace('"','')+'"}},'
            schema += question + ans
        schema += ']}</script>' 
        schema_final = schema.replace(',]}</script>',']}</script>') 
        faq_final = faq_body + schema + schema_final
        return faq_final
      
    
    for keyword_model in pending_keywords:
        keyword = keyword_model.name
        print('kw: ',keyword)
        excerpt = text_render(f'Write a short summary,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 25 words\n')
        introduction = text_format(text_render(f'Write interesting and attentionable blog Introduction,\nKeyword: {keyword},\nMust be include keyword in output\nand length approx 100 words\n'))
        conclusion_para = text_format(text_render(f'keyword: {keyword}\nWrite an web article bottom summary\n and length approx 60 words\n'))
        
        post_body = introduction + '<h2>'+keyword.title().replace('What ', '').replace('When ', '').replace('Which ', '').replace('How ', '').replace('Where ', '').replace('Why ', '').replace('Does ', '')+'</h2>' + content_body(keyword, keyword_model.outline) + youtubevid(keyword) + "<h2> FAQ's </h2>" + faq(keyword) + '<H2>Conclusion</H2>' + conclusion_para

        image_id = feature_image(keyword)
        category_id = create_category(category_name)
        title = keyword.title()
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
        
        else:
            keyword_model.error = str(f'Error Status : {r.status_code}')
            keyword_model.status = 'Failed'
        sleep(10)        
        keyword_model.save()
        shutil.rmtree('bulkimg')