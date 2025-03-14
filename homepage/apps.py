from django.apps import AppConfig


class HomepageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"
    verbose_name = "Main Website (CMS)"

    def ready(self):
        import homepage.signals
