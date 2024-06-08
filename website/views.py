from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import template
import json, random, string, time, requests, re, copy
#from website import decode_jwt
from email_validator import validate_email, EmailNotValidError
from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
from django.http import HttpResponse
from django.http import JsonResponse
from cognitojwt import jwt_sync
import base64



def getTokens(code):
    TOKEN_ENDPOINT = settings.TOKEN_ENDPOINT
    
    CLIENT_ID = settings.CLIENT_ID
    CLIENT_SECRET = settings.CLIENT_SECRET
    REGION = settings.COGNITO_REGION_NAME
    USERPOOL_ID = settings.USER_POOL_ID

    token_1 = code[1: ]
    token_2 = token_1[:-1]
    print(token_2)
    claims = jwt_sync.decode(token_2, REGION, USERPOOL_ID)
    print(claims)

    if not claims:
        return False
    
    user = {
        'id_token': token_2,
        'name': claims['cognito:username'],
        'email': claims['email']
    }
    return user

def getSession(request):
    try:
        response = request.COOKIES["sessiontoken"]
        return response
    except:
        return None

def home(request):
    # this is auth
    if 'userlogged' in request.session:
        try:
            token = request.session['id_token']
            print('this is the home token!!!!!!!!!!!!!!!',token)
            token = request.session['id_token']
            print(token)
            messages.success(request, "Logged In")
            print('yes')
        except:
            pass

    else:
        print('no')
    #status_1 = request.session['userlogged']
    #print(status_1)

    return render(request, 'home.html')

def test(request):
    return render(request, 'test.html')


@csrf_exempt
def home1(request):  

    current ={}
    
    if request.method == 'POST':
        try:
            request_getdata = request.POST.get('getdata', None)
            #print(request_getdata)
            userData = getTokens(request_getdata)
            #print(userData)
            current['name'] = userData['name']
            current['status'] = 1

            response = render(request, 'home1.html', current)
            request.session['userlogged'] = True
            request.session['id_token'] = userData['id_token']
            request.session['name'] = userData['name']
            request.session['email'] = userData['email']
            response.set_cookie('sessiontoken', userData['id_token'], max_age=60*60*24, httponly=True)

            status = request.COOKIES.get('status')
            print('home1',status)

            messages.success(request, "Logged In")
            return response 
            #return redirect('test.html') 
        except:
            token = getSession(request)
            print(token)
            if token is not None:
                userData = jwt_sync.decode(token, REGION, USERPOOL_ID)
                current['name'] = userData['name']
                current['status'] = 1
                response =  render(request, 'home1.html', current)
                return response 
            else:
                messages.success(request, "Login First..")
                return render(request, 'home1.html', {'status':0})
    return render(request, 'home1.html')

def logout_user(request):
    try:
        session_keys = list(request.session.keys())
        for key in session_keys:
            del request.session[key]
        #del request.session['userlogged']
        
        messages.success(request, "Logged Out....")
        return redirect('home')
    except:
        return redirect('home')

@csrf_exempt
def upload_image(request):
    if 'userlogged' in request.session:
        if request.method == 'POST':
            try:
                image_file = request.FILES['image_file']
                image_name = request.FILES['image_file'].name
                print(image_name)
            except KeyError:
                return JsonResponse({'error': 'No image file provided'}, status=400)
            
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            #print(image_base64)

            # Get the current user from the request
            upload_image_url = "https://pu75uefuh1.execute-api.us-east-1.amazonaws.com/prod/image_upload_test"
            username = request.session['name']
            image = image_base64
            name = image_name
            id_token =  request.session['id_token']
            auth = 'Bearer '+ id_token
            #print(auth)
            headers = {
                "Authorization": auth,
                "Content-Type": "application/json"
                }
            
            pyload = {
                "user_name": username,
                "image_name": name,
                "image_file": image
            }

            response = requests.post(upload_image_url, headers=headers, json=pyload)
            ans = response.json()
            print(ans)
            print('yes')

            return JsonResponse({'message': 'Image uploaded successfully'})
        elif request.method == 'GET':
            # Render the upload form
            return render(request, 'upload_image.html')
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    else:
        messages.success(request, "Login First..")
        return redirect('home')

@csrf_exempt
def tag_search(request):
    if 'userlogged' in request.session:
        if request.method == "GET":
            raw_tags = request.GET.get('tags','')
            print('ths',raw_tags)

            tag_search_url = "https://pu75uefuh1.execute-api.us-east-1.amazonaws.com/prod/tagSearch"
            username = request.session['name']
            id_token =  request.session['id_token']

            tag = raw_tags

            auth = 'Bearer '+ id_token

            headers = {
                "Authorization": auth,
                "Content-Type": "application/json"
                }
            
            payload = {
                "username": username,
                "tags": tag 
            }
            #print(pyload)

            response = requests.post(tag_search_url , headers=headers, json=payload)
            ans = response.json()
            print(type(ans['body']), ans['body'])
            
            return render(request, 'tag_search.html', {'tage_search_result': ans['body']})

    else:
        messages.success(request, "Login First..")
        return redirect('home')

   

@csrf_exempt
def thumbnail_full(request):
    if 'userlogged' in request.session:
        if request.method == 'GET':
            thumbnail = request.GET.get('thumbnail','')
            print('123',thumbnail)
            thumbnail_search_url = "https://pu75uefuh1.execute-api.us-east-1.amazonaws.com/prod/thumbFull"
            username = request.session['name']
            id_token =  request.session['id_token']

            link = [thumbnail]

            auth = 'Bearer '+ id_token

            headers = {
                "Authorization": auth,
                "Content-Type": "application/json"
                }
            
            payload = {
                "username": username,
                "links": link
            }
            #print(pyload)
            # https://5225-a3-images-demo.s3.amazonaws.com/images_resized/google_107178411549322360755/04587514249111efa68d5ea72ce43cd2-thumb.jpg
            response = requests.get(thumbnail_search_url, headers=headers, json=payload)
            ans = response.json()
            print('this is the full url',ans['body'])
            
            return render(request, 'thumbnail_full.html', {'full_size_image':ans['body']})
    else:
        messages.success(request, "Login First..")
        return redirect('home')
    


@csrf_exempt
def image_similar(request):
    if 'userlogged' in request.session:
        if request.method == 'POST':
            try:
                image_file = request.FILES['image-file-similar']
                print('hahaqweqweq',image_file)
            except KeyError:
                return JsonResponse({'error': 'No image file provided'}, status=400)
            
            # Read the file and encode it in base64
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            #print(image_base64)

            upload_simliar_image_url = "https://pu75uefuh1.execute-api.us-east-1.amazonaws.com/prod/image_on_image"
            username = request.session['name']
            image = image_base64

            id_token =  request.session['id_token']
            auth = 'Bearer '+ id_token
            #print(auth)
            headers = {
                "Authorization": auth,
                "Content-Type": "application/json"
                }

            # Prepare the nested JSON as a string within the 'body' key

            payload = {
                "body": image,
                "username": username
            }

            # Send the request to the API Gateway
            response = requests.post(upload_simliar_image_url, json=payload, headers=headers)
            ans = response.json()
            print(ans['image_urls'])
            print('yes')

            # return HttpResponse({'message': 'Image uploaded successfully'})
            #messages.success(request, "Image uploaded successfully")
            return render(request, 'image_similar.html', {'same_page_url':str(ans['image_urls'])})
            #return HttpResponse(template.render(ans['image_urls'], request))
            #return TemplateResponse(request, 'image_similar.html', {'same_page_url':str(ans['image_urls'])})
        elif request.method == 'GET':
            #image_file = request.FILES['image-file-similar']
            #print('haha',image_file)
            # Render the upload form
            return render(request, 'image_similar.html')
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    else:
        messages.success(request, "Login First..")
        return redirect('home')

@csrf_exempt
def tag_manipulation(request):
    if 'userlogged' in request.session:
        if request.method == 'GET':
            try:
                # Extract data directly from FormData
                urls = request.GET.get('urls')
                tags = request.GET.get('tags')
                operation = request.GET.get('operation')
                print('urls', urls)
                print('tags', tags)
                print('operation', operation)
                if urls != None:
                    urls_list = re.split(r'[,\s]\s*',urls)
                    print('urls_list',urls_list)
                    #url_json = json.dump(urls_list)

                    tags_list = re.split(r'[,\s]\s*',tags)
                    print('tags_list',tags_list)
                    #tag_json = json.dump(tags_list)

                    operation_type = None
                    if operation == 'add':
                        operation_type = 1 
                    else:
                        operation_type = 0
                else:
                    return render(request, 'tag_manipulation.html')

            except TypeError as e:
                return JsonResponse({'error': 'Error processing input data'}, status=400)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON in form data'}, status=400)

            api_url = "https://pu75uefuh1.execute-api.us-east-1.amazonaws.com/prod/tagManipulate"

            username = request.session['name']

            id_token =  request.session['id_token']
            auth = 'Bearer '+ id_token
            #print(auth)
            headers = {
                "Authorization": auth,
                "Content-Type": "application/json"
                }

            payload = {
                "url": urls_list,
                "tags": tags_list,
                "type": operation_type,
                "username": username
            }
            print('qwe',payload['url'])
            response = requests.post(api_url, json=payload, headers=headers)
            ans = response.json()
            print(ans['statusCode'], ans)
            print('yes',response.status_code)
            
            if response.status_code == 200:
                print('yes')
                if ans['statusCode'] == 201:
                    messages.success(request, f"{ans['body']}")
                    print('this should show the info')
                    return render(request, 'tag_manipulation.html')
                else:
                    return render(request, 'tag_manipulation.html')
            else:
                return JsonResponse({'error': 'Failed to communicate with API', 'status_code': response.status_code}, status=502)
    else:
        messages.success(request, "Login First..")
        return redirect('home')

@csrf_exempt
def delete_image(request):
    if 'userlogged' in request.session:
        if request.method == 'GET':
            try:
                # Extract data directly from FormData
                urls = request.GET.get('deleteUrl','')
                print('urls',urls)
                if urls != None:
                    urls_list = re.split(r'[,\s]\s*',urls)
                    print('urls_list',urls_list)
                    #url_json = json.dump(urls_list)
                else:
                    return render(request, 'delete_image.html')

            except TypeError as e:
                return JsonResponse({'error': 'Error processing input data'}, status=400)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON in form data'}, status=400)
            if urls != None:
                delete_url = "https://pu75uefuh1.execute-api.us-east-1.amazonaws.com/prod/deleteImage"

                username = request.session['name']

                id_token =  request.session['id_token']
                
                auth = 'Bearer '+ id_token

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": auth
                    }

                payload = {
                    "url": urls_list,
                    "username": username
                }
                
                aresponse = requests.post(delete_url, headers=headers, json=payload)
                ans = aresponse.json()
                print(ans)
                print('reason',aresponse)
                
                if aresponse.status_code == 200:
                    if ans['statusCode'] == 201:
                        messages.success(request, "Image Delete")
                        return render(request, 'delete_image.html')
                    else:
                        #messages.success(request, f"Error Delete: {ans['body']}")
                        return render(request, 'delete_image.html')
                else:
                    return JsonResponse({'error': 'Failed to communicate with API', 'status_code': ans['statusCode']}, status=502)        
        else:
            messages.success(request, "Login First..")
            return redirect('home')

@csrf_exempt
def subscribe(request):
    if 'userlogged' in request.session:
        if request.method == 'GET':
            try:
                # Extract data directly from FormData
                tag_topic = request.GET.get('sub_form_id','')
                tags_topic_list = re.split(r'[,\s]\s*',tag_topic)
                print('tag_topic ',tags_topic_list, type(tags_topic_list))
               
                tag_topic_url = "https://pu75uefuh1.execute-api.us-east-1.amazonaws.com/prod/tag/subscribe"

                username = request.session['name']
                id_token =  request.session['id_token']
                email = request.session['email']

                auth = 'Bearer '+ id_token
                #print(auth)

                headers={
                    "Content-Type": "application/json",
                    "Authorization": auth
                    }

                payload = {
                    "tag": tag_topic,
                    "email": email,
                    "username": username
                }
                response = requests.post(tag_topic_url, headers=headers, json=payload)
                
                ans = response.json()
                print(len(ans))
                print(response)
                if response.status_code == 200:
                    if len(ans) > 57:
                        messages.success(request, f"{ans}")
                        return render(request, 'subscribe.html')
                    else:
                        return render(request, 'subscribe.html')
                else:
                    return JsonResponse({'error': 'Failed to communicate with API', 'status_code': response.status_code}, status=502)
                    
            
            except TypeError as e:
                return JsonResponse({'error': 'Error processing input data'}, status=400)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON in form data'}, status=400)
    else:
        messages.success(request, "Login First..")
        return redirect('home')


      