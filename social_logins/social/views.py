from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.conf import settings
import requests
from .facebook import GraphAPI, get_access_token_from_code

# Create your views here.


def  index(request):
    return HttpResponse("<h1>your project runs successfully</h1>")


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(username=email, password=password)
        print (admin)
        if admin is not None:
            login(request, admin)
            return HttpResponseRedirect('/home/')
        return render(request, 'login.html', {'errors': True})
    return render(request, 'login.html')


def home_display(request):
    return render(request, "home.html")


def google_login(request):
    print ("request get")
    print (request.GET)
    if 'code' in request.GET:
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri':  settings.GOOGLE_REDIRECT_URL,
            'client_id': settings.GOOGLE_APP_ID,
            'client_secret': settings.GOOGLE_SECRET_KEY
        }

        info = requests.post(
            "https://accounts.google.com/o/oauth2/token", data=params)

        info = info.json()
        print ('info')
        print (info)
        if 'access_token' in info.keys():
            params = {'access_token': info['access_token']}
            kw = dict(params=params, headers={}, timeout=60)
            response = requests.request('GET', 'https://www.googleapis.com/oauth2/v1/userinfo', **kw)
            user_document = response.json()
            print ('response')
            print (user_document)

            email_matches = User.objects.filter(email=user_document['email'])
            link = "https://plus.google.com/" + user_document['id']

            if email_matches:
                user = email_matches[0]
            else:
                print ("user create")
                user = User.objects.create(email=user_document['email'], username=user_document['email'])
            user = authenticate(username=user_document['email'])

            login(request, user)
            return render(request, 'home.html', {'user_document': user_document})
        else:
            return HttpResponseRedirect('/login/')
    else:
        rty = "https://accounts.google.com/o/oauth2/auth?client_id=" + \
               settings.GOOGLE_APP_ID + "&response_type=code"
        rty += "&scope=https://www.googleapis.com/auth/userinfo.profile" + \
            " https://www.googleapis.com/auth/userinfo.email&redirect_uri=" + settings.GOOGLE_REDIRECT_URL
        print (rty)
        return HttpResponseRedirect(rty)


def facebook_login(request):
    if 'code' in request.GET:
        accesstoken = get_access_token_from_code(request.GET['code'], settings.FACEBOOK_REDIRECT_URL, settings.FB_APP_ID, settings.FB_SECRET)
        if 'error' in accesstoken.keys():
            message_type = 'Sorry,'
            message = 'Your session has been expired'
            reason = "Please kindly try again login to update your profile"
            email = settings.DEFAULT_FROM_EMAIL
            return render(request, '404.html', {'message_type': message_type, 'message': message, 'reason': reason})
        graph = GraphAPI(accesstoken['access_token'])
        accesstoken = graph.extend_access_token(settings.FB_APP_ID, settings.FB_SECRET)['accesstoken']
        profile = graph.get_object("me", fields="id,name,email,birthday,hometown,location,link,locale,gender")
        print (profile)
        email = profile['email'] if 'email' in profile.keys() else ''
        hometown = profile['hometown']['name'] if 'hometown' in profile.keys() else ''
        location = profile['location']['name'] if 'location' in profile.keys() else ''
        profile_pic = "https://graph.facebook.com/" + profile['id'] + "/picture?type=large"
        if 'email' in profile.keys():
            user = User.objects.filter(email=profile['email'])
            if user:
                user = user[0]
            else:
                user = User.objects.create(
                    username=profile['email'],
                    email=profile['email'],
                    )

            user = authenticate(username=profile['email'])
            print (user)
        else:
            message_type = 'Sorry,'
            message = 'We didnt find your email id through facebook'
            reason = "Please verify your email id in facebook and try again"
            return render(request, '404.html', {'message_type': message_type, 'message': message, 'reason': reason})

        login(request, user)
        return render(request, 'home.html', {'profile': profile, 'email': email, 'hometown': hometown, 'location': location, 'profile_pic': profile_pic})

        return HttpResponseRedirect('/home/')
    elif 'error' in request.GET:
        # TODO : log the error and transfer to error page
        print (request.GET)
    else:
        # publish_stream, friends_groups
        # the above are depricated as part of graphapi 2.3 we need to update our code to fix it
        rty = "https://graph.facebook.com/oauth/authorize?client_id=" + settings.FB_APP_ID + "&redirect_uri=" + settings.FACEBOOK_REDIRECT_URL + "&scope=user_about_me, user_location, user_website, email"
        return HttpResponseRedirect(rty)

def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login/")