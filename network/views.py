from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .models import User, Post, Follow, Like
from django.http import JsonResponse
import json

class New_post_form(forms.Form):
    content = forms.CharField(min_length=1, max_length=280, widget=forms.Textarea(attrs={"rows": "3"}))

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
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def index(request, page=""):
    # Get list of liked posts by logged in user
    if request.user.is_authenticated:
        user_likes_list = list(Like.objects.filter(user=request.user).values_list('post_id', flat=True))

        # Get posts authored by followed profiles for Following page
        following_users = list(request.user.follower.values_list('following_user_id', flat=True))
        following_users_posts = Post.objects.filter(user__in=following_users).order_by('-id')
    else:
        user_likes_list = ''
        following_users_posts = ''

    # Paginate all posts for All Posts page
    all_posts = Post.objects.all().order_by('-id')

    # Paginate the appropriate posts, default is All Posts
    if page == 'following':
        paginator = Paginator(following_users_posts, 10)
    else: 
        paginator = Paginator(all_posts, 10)

    # Paginate 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "form" : New_post_form(),
        "user_likes_list": user_likes_list,
    })

def profile(request, user_id):
    # Render profile with the profile's posts
    user_profile = User.objects.get(pk=user_id)
    posts_by_user = Post.objects.filter(user=user_id).order_by('-id')

    # Check if user is logged in, then check if they are following the viewed profile
    if request.user.is_authenticated:
        currently_following = Follow.objects.filter(user=request.user, following_user=user_id).exists()
    else:
        currently_following = ""

    # Paginated 10 posts per page
    paginator = Paginator(posts_by_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "form": New_post_form(),
        "user_profile": user_profile,
        "followers": len(user_profile.following.all()),
        "follows": len(user_profile.follower.all()),
        "currently_following": currently_following,
        })

def new_post(request):
    if request.method == "POST":
        form = New_post_form(request.POST, 'utf-8')
        if form.is_valid():
            new_post = Post(
                content = form.cleaned_data["content"],
                user = request.user)
            new_post.save()
            return HttpResponseRedirect(reverse("index"))

@csrf_exempt   
def edit_post(request):
    # Editing post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get content and id of post to be edited
    data = json.loads(request.body)
    post_id = data.get("post_id", "")
    post_content = data.get("content", "")

    # Check if edited post is not empty
    if post_content == "":
        return JsonResponse({"error": "post body cannot be empty"}, status=400)
    
    # Update post content
    post = Post.objects.get(pk=post_id)
    post.content = post_content
    post.save()
    return JsonResponse({"message": "Post edited succesfully."}, status=201)
    
def add_follow(request, user_id):
    Follow.objects.create(user=request.user, following_user=User.objects.get(pk=user_id))
    return HttpResponseRedirect(reverse("profile", args=(user_id,)))

def remove_follow(request, user_id):
    follow = Follow.objects.get(user=request.user, following_user=user_id)
    follow.delete()
    return HttpResponseRedirect(reverse("profile", args=(user_id,)))

@csrf_exempt
def like(request):
    # Editing post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get post
    data = json.loads(request.body)
    post_id = data.get("post_id", "")
    post = Post.objects.get(pk=post_id)

    # Create a like or remove the like if it exists already
    if Like.objects.filter(user=request.user, post=post).exists():
        like = Like.objects.filter(user=request.user, post=post)
        like.delete()
        post.likes -= 1
        post.save()
        return JsonResponse({"message": "Like removed succesfully.", "total_likes": post.likes}, status=201)
    else:    
        Like.objects.create(user=request.user, post=post)
        post.likes += 1
        post.save()
        return JsonResponse({"message": "Like added succesfully.", "total_likes": post.likes}, status=201)



