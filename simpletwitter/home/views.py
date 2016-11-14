from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context
from django.core import serializers
from home.models import TwitUser,TwitPost,TwitFollower


@csrf_exempt
def home(request):
    template = loader.get_template('Home.html')
    # request.session[0] = 'bar'
    #return HttpResponse(text)
    #return render_to_response('Hello.html')
    # Load the template myblog/templates/index.html
    # request.session[0] = 'bar'
    #template = loader.get_template('Hello.html')

    # Context is a normal Python dictionary whose keys can be accessed in the template index.html
    #context = Context({
     #   'TwitUserId':-1,
     #   'username': 'GUEST'
    #})
    #return HttpResponse(template.render(context))
    if request.session.has_key('username'):
        u=loginFunc(request.session['username'])
        if u.exists():
            usr=TwitUser.objects.get(username = request.session['username'])
            # Context is a normal Python dictionary whose keys can be accessed in the template index.html
            context = Context({
                'TwitUserId':usr.id,
                'username': usr.username
            })
            #return HttpResponse("html")
            return HttpResponse(template.render(context))
    else:
        context = Context({
            'TwitUserId':-1,
            'username': 'GUEST'
        })
        #return HttpResponse("html")
        return HttpResponse(template.render(context))


@csrf_exempt
def view(request):
    #del request.session['username']
    template = loader.get_template('View.html')
    if request.session.has_key('username'):
        u=loginFunc(request.session['username'])
        if u.exists():
            usr=TwitUser.objects.get(username = request.session['username'])
            # Context is a normal Python dictionary whose keys can be accessed in the template index.html
            #context = Context({
             #   'TwitUserId':usr.id,
             #   'username': usr.username
            #})
            #followedUser=TwitFollower.objects.filter(TwitUser_Id=1).only('FollowerId').all()

            #posts = TwitPost.objects.raw('''select *
             #                           from TwitPost
            #                           where TwitUser_id in (
            #                              select Distinct FollowerId from TwitFollower where TwitUser_id =1
             #                       ) ''')

            posts=TwitPost.objects.raw('''select *
from TwitPost p
  INNER JOIN TwitUser u
  on p.TwitUser_id=u.id
where TwitUser_id in (
  select Distinct FollowerId from TwitFollower where TwitUser_id =%s)''',[usr.id]);
            context = Context({
                'posts': posts,
                'id':usr.id
            })
            return HttpResponse(template.render(context))
    else:
        return HttpResponse("Not a valid user.Go to register to register first   <button  onclick=\"window.location='/register'\">Click here</button>")


@csrf_exempt
def register(request):
    if request.method == 'GET':
        template = loader.get_template('Register.html')
        context = Context({
            'post': ''
        })
        return HttpResponse(template.render(context))
    else:
        #email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        alreadyFollowing=TwitFollower.objects.raw('select * from TwitUser where username=%s ',[username])
        if len(list(alreadyFollowing))>0:
            return HttpResponse('Already have same username.Try with different username')
        else:
            user=TwitUser(username=username,password=password,email=email)
            user.save()

            post=TwitFollower(FollowerId=user.id,TwitUser=user)
            post.save();
            #password = request.POST.get('password')
            #return HttpResponseRedirect('/hello/')
            template = loader.get_template('SuccessfullyRegistered.html')
            context = Context({
                'username': user.username,
                'email':user.email
            })
            return HttpResponse(template.render(context))

#login complete
@csrf_exempt
def login(request):
    if request.method == 'GET':
        template = loader.get_template('Login.html')
        context = Context({
            'post': 'heoo'
        })
        return HttpResponse(template.render(context))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        u=TwitUser.objects.filter(username=username,password=password)
        if u.exists():
            usr=TwitUser.objects.get(username = username)
            request.session['username']=usr.username
            return HttpResponse("login successfully <script>window.location='/home'</script>")
        else:
            return HttpResponse("Not a valid user.Go to register to register first   <button  onclick=\"window.location='/register'\">Click here</button>")
@csrf_exempt
def twit(request):
    if 'username' not in request.session:
        return HttpResponseRedirect('/home')
    if request.method == 'GET':
        template = loader.get_template('Twit.html')
        context = Context({
            'username': request.session['username']
        })
        return HttpResponse(template.render(context))
    else:
        title = request.POST.get('title')
        description = request.POST.get('description')
        username = request.session['username'];
        usr=TwitUser.objects.get(username = username)

        t=TwitPost(Title=title,Description=description,TwitUser=usr)
        t.save()
        return HttpResponse("Submitted successfully .To view <button  onclick=\"window.location='/view'\">Click here</button>")

@csrf_exempt
def follow(request):
    if 'username' not in request.session:
        return HttpResponseRedirect('/home')
    if request.method == 'GET':
        username = request.session['username'];
        template = loader.get_template('Follow.html')
        users=TwitUser.objects.raw("select * from TwitUser where username<>%s",[username])
        context = Context({
            'users': users
        })
        return HttpResponse(template.render(context))
    else:
        followid=request.POST.get('userid')
        username = request.session['username'];
        user=TwitUser.objects.get(username=username)
        alreadyFollowing=TwitFollower.objects.raw('select * from TwitFollower where TwitUser_id=%s and FollowerId=%s',[user.id,followid])
        if len(list(alreadyFollowing))>0:
            return HttpResponse('following')
        else:
            f=TwitFollower(FollowerId=followid,TwitUser=user)
            f.save()
            return HttpResponse('ok')

def logout(request):
    try:
        del request.session['username']
    except Exception as e:
         return HttpResponseRedirect('/home')
    return HttpResponseRedirect('/home')

def loginFunc(uname):
    twituser=TwitUser.objects.filter(username=uname)
    return twituser;





