from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


def process(request):
    if request.method == 'POST':
        image = request.FILES['image']
        fs = FileSystemStorage()
        saved_name = fs.save(image.name, image)
        image_url = fs.url(saved_name)
        response = [
            {"type": "text", "content": "Success!"},
            {"type": "text", "content": "cropLeft: " + request.POST['cropLeft']},
            {"type": "text", "content": "cropTop: " + request.POST['cropTop']},
            {"type": "text", "content": "cropRight: " + request.POST['cropRight']},
            {"type": "text", "content": "cropBottom: " + request.POST['cropBottom']},
            {"type": "image", "content": image_url},
        ]
        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({'error': 'Please request post'})
