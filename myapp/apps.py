from django.apps import AppConfig

class MyappConfig(AppConfig):
    # Recommended to use BigAutoField as default for Django 3.2+
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name of the app (must match the directory name)
    name = 'myapp'
    
    # Human-readable name for admin interface
    verbose_name = 'My Custom App'
    
    def ready(self):
        """
        Override this method to perform initialization tasks when Django starts.
        Useful for signals, checks, or other startup routines.
        """
  