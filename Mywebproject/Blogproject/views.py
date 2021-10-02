from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, Http404
from .models import Post, Profile, Comment
# from .forms import CreateUserForm,PostCreateForm, UserEditForm, ProfileEditForm, PostEditForm,CommentForm
from .form import *
from django.http.response import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='login')
def post_list(request):
    posts_list = Post.objects.all().order_by('-id')
    query = request.GET.get('q')
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(author__username=query) |
            Q(body__icontains=query))
    paginator = Paginator(posts_list, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(posts, index=4)
    page_range = list(paginator.page_range)[start_index:end_index]
    return render(request, 'post_list.html', {'posts': posts, 'page_range': page_range})


def proper_pagination(posts, index):
    start_index = 0
    end_index = 7
    if posts.number > index:
        start_index = posts.number - index
        end_index = start_index + end_index
    return (start_index, end_index)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.save()
                Profile.objects.create(user=new_user)
                return redirect('login')
            else:
                return redirect('register')
        else:
            form = CreateUserForm()
            return render(request, 'register.html', {'form': form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login is Successfull')
                return redirect('post_list')
            else:
                messages.warning(request, 'Username or Password Invalid')
                return render(request, 'login_file.html')

        else:
            return render(request, 'login_file.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('login')


def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post is created successfully')
            return redirect('post_list')
    else:
        form = PostCreateForm()
        return render(request, 'post_create.html', {'form': form})


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404
    if request.method == "POST":
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, '{} Post was modified'.format(post.title))
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
        return render(request, 'post_edit.html', {'post': post, 'form': form})


def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            redirect('post_list')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'edit_file.html', context)


@login_required(login_url='login')
def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    is_favourite = False
    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if request.method == "POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'is_liked': is_liked,
        'is_favourite': is_favourite,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'post_details.html', context)


def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    context = {
        'favourite_posts': favourite_posts
    }
    return render(request, 'post_favrouit_list.html', context)


def favourite_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.success(request, '{} post was deleted successfully'.format(post.title))
    return redirect('post_list')


