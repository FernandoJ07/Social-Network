import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from .models import *


def index(request):

    posts = Post.objects.all().order_by('-date')

    paginator = Paginator(posts, 10)


    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    

    return render(request, "network/index.html", {
        'page_obj': pageObj,
    })

def savePost(request):
    
    if request.user.is_authenticated:

        if request.method == 'POST':
            user = request.user
            content = request.POST['content']

            post = Post.objects.create(poster = user, content =content)
            post.save()
            messages.success(request, 'Successfully posted')
            return redirect('index')
    else:
        messages.info(request, 'You must Log In to post')
        return redirect('index')

def userProfile(request, username):
    
    #Get user and your own posts
    user = User.objects.get(username = username)
    posts = Post.objects.filter(poster = user.id).order_by('-date')

    paginator = Paginator(posts, 4)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    #Get user followed
    userFollowing = Follow.objects.get(user = user.id )
    followings = userFollowing.followed.count()

    if request.user.is_authenticated:
        userFollowed = Follow.objects.get(user = request.user)
        if user in userFollowed.followed.all():
            followed = True
        else: 
            followed = False

    else:
        return redirect('login')
        
    #Get user followers
    numbFollowers = 0

    for i in Follow.objects.all():
        followers = i.followed.all()
        for j in followers:
            if user.username == j.username:
                numbFollowers +=1


    return render(request, 'network/profile.html', {
        "user": user,
        'page_obj': pageObj,
        'following': followings,
        'followed': followed,
        'followers': numbFollowers
        })

def follow(request, username):
    userFollower = Follow.objects.get(user = request.user)
    userFollowed = User.objects.get(username = username)

    userFollower.followed.add(userFollowed)
    return redirect('profile', username)

def unFollow(request, username):
    userFollower = Follow.objects.get(user = request.user)
    userFollowed = User.objects.get(username = username)

    userFollower.followed.remove(userFollowed)
    return redirect('profile', username)

@login_required
def followingPosts(request):
    userFollowing = Follow.objects.get(user = request.user.id )
    followings = userFollowing.followed.all()

    users = []
    for user in followings:
        users.append(user)

    postsList = []
    for user in users:
        post = Post.objects.filter(poster = user.id).order_by('-date')
        postsList.append(post)

    paginator = Paginator(postsList, 10)

    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    
    return render(request, 'network/followingPosts.html', {
        'page_obj': pageObj
    })

def editPost(request, post_id):

    post = Post.objects.get(id= post_id)
    data = json.loads(request.body)
    post.content = data['form']
    post.save()
    return JsonResponse({"content": data['form']})

@login_required
def postLiked(request, post_id):

    post = Post.objects.get(id = post_id)
    data = json.loads(request.body)

    if data.get('like'):
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    post.save()
    return JsonResponse({'like': post.likes.count()})
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            follow = Follow.objects.create(user = user)
            follow.save()
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
