from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save()); return redirect('/')
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Post, Comment

@login_required
def feed(request):
    if request.method == 'POST' and request.POST.get('text', '').strip():
        Post.objects.create(author=request.user, text=request.POST['text'].strip()); return redirect('feed')
    ids = list(request.user.profile.following.values_list('id', flat=True)) + [request.user.id]
    scope = request.GET.get('all')
    posts = Post.objects.all() if scope else Post.objects.filter(author_id__in=ids)
    return render(request, 'social/feed.html', {'posts': posts.select_related('author').prefetch_related('comments__author', 'likes'), 'all': scope})

@login_required
def like(request, pk):
    p = get_object_or_404(Post, pk=pk)
    p.likes.remove(request.user) if request.user in p.likes.all() else p.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def comment(request, pk):
    if request.method == 'POST' and request.POST.get('text', '').strip():
        Comment.objects.create(post=get_object_or_404(Post, pk=pk), author=request.user, text=request.POST['text'].strip())
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def profile(request, username):
    u = get_object_or_404(User, username=username)
    return render(request, 'social/profile.html', {'u': u, 'posts': u.posts.all(),
        'is_following': u in request.user.profile.following.all()})

@login_required
def follow(request, username):
    u = get_object_or_404(User, username=username)
    if u != request.user:
        f = request.user.profile.following
        f.remove(u) if u in f.all() else f.add(u)
    return redirect('profile', username=username)

@login_required
def edit_bio(request):
    if request.method == 'POST':
        request.user.profile.bio = request.POST.get('bio', '')[:200]; request.user.profile.save()
    return redirect('profile', username=request.user.username)

@login_required
def people(request):
    return render(request, 'social/people.html', {'users': User.objects.exclude(pk=request.user.pk)})
