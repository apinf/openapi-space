from django.http import JsonResponse

def search_apis(request):
    return JSONResponse({'apis': []})
