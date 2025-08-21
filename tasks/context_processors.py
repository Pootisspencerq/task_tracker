from .models import Theme

def active_theme(request):
    if request.user.is_authenticated:
        return {
            "active_theme": Theme.objects.filter(user=request.user, is_active=True).first(),
            "user_themes": Theme.objects.filter(user=request.user)
        }
    return {}
