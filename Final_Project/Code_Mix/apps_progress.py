from django.apps import AppConfig

class CodeMixProgressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Code_Mix'
    
    def ready(self):
        import Code_Mix.admin_progress
