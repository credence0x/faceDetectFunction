from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import base64

@csrf_exempt
@xframe_options_exempt
def detectView(request):

    image_file = request.FILES['image']
    read_image = image_file.read()
    image_data = base64.b64encode(read_image).decode('utf-8')
    print(image_data)
    return HttpResponse(image_data, content_type="image/*")
    
