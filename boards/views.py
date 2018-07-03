from django.db.models import Count  
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post 
from .forms import NewTopicForm, PostForm 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime  
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 

from django.http import HttpResponse
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})     

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page',1)
    paginator = Paginator(queryset, 20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'topics.html', {'board': board, 'topics':topics})

# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save() 
#     return render(request, 'topic_posts.html', {'topic': topic})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    session_key = 'viewed_topic_{}'.format(topic.pk)  # <-- here.... create a key string
    if not request.session.get(session_key, False):    # if already in the session
        topic.views += 1
        topic.save()
        request.session[session_key] = True            
    queryset = topic.posts.order_by('created_at')
    page = request.GET.get('page',1) 
    paginator = Paginator(queryset, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'topic_posts.html', {'topic':topic, 'posts':posts})

@login_required 
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)   # to prevent duplicate DB save
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # <- here
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = datetime.datetime.now()
            topic.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@login_required 
def edit_post(request, pk, topic_pk, post_pk):  
    topic = get_object_or_404(Topic, pk=topic_pk)
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            if post.created_by == request.user: 
                post = form.save(commit=False)
                post.updated_at = datetime.datetime.now()    # timezone.now()  
                post.updated_by = request.user
                post.save()
                topic.last_updated = datetime.datetime.now()
                topic.save()
                return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'post': post, 'form': form})



   

