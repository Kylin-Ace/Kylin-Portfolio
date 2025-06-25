from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.core.cache import cache
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Project, BlogPost, About
from .forms import ContactForm

def home(request):
    """Homepage view showing featured and recent projects"""
    featured_projects = Project.objects.filter(is_featured=True).select_related().order_by('-created_at')[:3]
    if not featured_projects.exists():
        featured_projects = Project.objects.select_related().order_by('-created_at')[:3]

    recent_projects = Project.objects.select_related().order_by('-created_at')[:3]
    return render(request, 'myapp/home.html', {
        'featured_projects': featured_projects,
        'recent_projects': recent_projects
    })

def project_detail(request, slug):
    """Detail view for a single project"""
    project = get_object_or_404(
        Project.objects.select_related(),
        slug=slug
    )
    related_projects = Project.objects.exclude(slug=slug).select_related().order_by('?')[:3]
    return render(request, 'myapp/project_detail.html', {
        'project': project,
        'related_projects': related_projects
    })

def blog(request):
    """List view for published blog posts with pagination"""
    posts = BlogPost.objects.filter(status='published').order_by('-published_at')
    return render(request, 'myapp/blog.html', {'posts': posts})

def blog_detail(request, slug):
    """Detail view for a single blog post with caching"""
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'myapp/blog_detail.html', {'post': post})

def about(request):
    """About page view with fallback for missing content."""
    about_me = About.objects.first()
    return render(request, 'myapp/about.html', {
        'about_me': about_me,
    })

def contact(request):
    """Contact form view with success and error messages."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save form data if applicable
            messages.success(request, "Your message has been sent successfully!")
            return redirect('myapp:contact_success')
        else:
            messages.error(request, "There was an error submitting the form. Please try again.")
    else:
        form = ContactForm()
    
    return render(request, 'myapp/contact.html', {'form': form})

@require_POST
def toggle_theme(request):
    """Session-based theme toggle with redirect"""
    current_theme = request.session.get('theme', 'light')
    request.session['theme'] = 'dark' if current_theme == 'light' else 'light'
    return redirect(request.META.get('HTTP_REFERER', reverse('myapp:home')))

@csrf_exempt
def api_toggle_theme(request):
    """API endpoint for AJAX theme toggling."""
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        return JsonResponse({
            'status': 'success',
            'theme': theme
        })
    return JsonResponse({'status': 'error'}, status=400)