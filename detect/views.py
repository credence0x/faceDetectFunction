from django.shortcuts import render
from django.http import JsonResponse
from .models import Old_image
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import base64,os
from pathlib import Path
from yoloface import yoloface
from face_detector.settings import BASE_DIR,MEDIA_ROOT

@csrf_exempt
def detectView(request):
	if request.method =="POST":
		image_file = request.FILES['image']

		if image_file:
			old_image = Old_image.objects.create(image=image_file)
		    
			old_absolute_file_path = os.path.join(MEDIA_ROOT, old_image.image.name)
		    
			model_cfg = os.path.join(BASE_DIR, "yoloface","cfg","yolov3-face.cfg")
			model_weights = os.path.join(BASE_DIR, "yoloface","model-weights","yolov3-wider_16000.weights")
			output_dir = os.path.join(BASE_DIR, "yoloface","outputs")


			new_image_path = yoloface.run_yoloface(image_path=old_absolute_file_path,
											    	model_cfg=model_cfg,
											    	model_weights=model_weights,
											    	output_dir=output_dir)
			new_image_path = str(new_image_path)
			old_image.new_image_file_name = new_image_path
			old_image.save()
			new_image = open(new_image_path, "rb")
			new_image_utf8 = base64.b64encode(new_image.read()).decode('utf-8')
			return HttpResponse(new_image_utf8, content_type="image/*")
		else:
			return HttpResponse("No image sent")

	else:
		return render(request,"index.html")

