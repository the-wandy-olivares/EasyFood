from django.http import JsonResponse
from django.contrib.auth.models import User

def Verify_Username_Ajax(request):
    username = request.GET.get('username', '').strip()
    if username:
        user_exists = User.objects.filter(username__iexact=username).exists()
        return JsonResponse({'exists': user_exists})
    return JsonResponse({'error': 'No username provided'}, status=400)