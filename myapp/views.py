from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Project, BlogPost, About
from .forms import ContactForm

def home(request):
    """Show featured work, falling back to the most recent projects."""
    featured_projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:3]
    if not featured_projects.exists():
        featured_projects = Project.objects.order_by('-created_at')[:3]

    return render(request, 'myapp/home.html', {'featured_projects': featured_projects})

def projects(request):
    projects = Project.objects.order_by('-is_featured', '-created_at')
    return render(request, 'myapp/projects.html', {'projects': projects})

def project_detail(request, slug):
    """Detail view for a single project"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(slug=slug).order_by('-is_featured', '-created_at')[:3]
    return render(request, 'myapp/project_detail.html', {
        'project': project,
        'related_projects': related_projects
    })

def blog(request):
    """List published posts, with optional search and pagination."""
    query = request.GET.get('q', '').strip()[:100]
    posts = BlogPost.objects.filter(status=BlogPost.PUBLISHED).order_by('-published_at')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    page = Paginator(posts, 6).get_page(request.GET.get('page'))
    return render(request, 'myapp/blog.html', {'posts': page, 'query': query})

def blog_detail(request, slug):
    """Show a published blog post."""
    post = get_object_or_404(BlogPost, slug=slug, status=BlogPost.PUBLISHED)
    return render(request, 'myapp/blog_detail.html', {'post': post})

def about(request):
    """About page view with fallback for missing content."""
    about_me = About.objects.first()
    return render(request, 'myapp/about.html', {
        'about_me': about_me,
    })

def contact(request):
    """Save contact messages for follow-up from the admin."""
    form = ContactForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out. Your message has been received.")
            return redirect('myapp:contact')
        messages.error(request, "Please correct the errors below and try again.")
    return render(request, 'myapp/contact.html', {'form': form})