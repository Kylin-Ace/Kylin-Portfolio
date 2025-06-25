from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import URLValidator, FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import Truncator

# Utility function for slug generation
def generate_unique_slug(model_class, field_value, slug_field_name="slug", max_length=255):
    """
    Generate a unique slug for a given model class and field value.
    """
    slug = orig = slugify(field_value)[:max_length]
    for x in range(1, 100):
        if not model_class.objects.filter(**{slug_field_name: slug}).exists():
            return slug
        slug = f"{orig}-{x}"
    raise ValueError("Unable to generate a unique slug.")

class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    description = models.TextField()
    image = models.ImageField(
        upload_to='projects/%Y/%m/%d/',
        default='defaults/project.png',
        null=False,
        blank=True,
        help_text="Upload a project image"
    )
    is_featured = models.BooleanField(default=False)
    github_url = models.URLField(
        blank=True,
        validators=[URLValidator(schemes=['http', 'https', 'git'])],
        help_text="URL to GitHub repository"
    )
    live_url = models.URLField(
        blank=True,
        validators=[URLValidator(schemes=['http', 'https'])],
        help_text="URL to live project"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_featured']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Project, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('myapp:project_detail', kwargs={'slug': self.slug})  

    def __str__(self):
        return self.title
class BlogPost(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True)  # Make it optional
    image = models.ImageField(upload_to='blog/%Y/%m/%d/', help_text="Featured image for the blog post")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at']
        get_latest_by = 'published_at'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('myapp:blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class About(models.Model):
    name = models.CharField(max_length=200, help_text="Your full name")
    title = models.CharField(max_length=200, help_text="Your professional title")
    bio = models.TextField(help_text="Tell us about yourself")
    short_bio = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short version for previews"
    )
    image = models.ImageField(
        upload_to='about/',
        help_text="Profile picture (recommended size: 800x800px)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'

    def clean(self):
        if About.objects.exists() and not self.pk:
            raise ValidationError('Only one About instance is allowed.')

    def save(self, *args, **kwargs):
        if not self.pk and About.objects.exists():
            About.objects.all().delete()

        # Optimize image if one is being saved
        if self.image:
            img = Image.open(self.image)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize image
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)
            
            # Save the optimized image
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Update the ImageField
            self.image = ContentFile(output.read(), name=self.image.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    slug = models.SlugField(unique=True)