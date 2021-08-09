from django.shortcuts import render
from django.http import JsonResponse
from .models import Old_image
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
import base64,os,requests
from pathlib import Path
from yoloface import yoloface
from face_detector.settings import BASE_DIR,MEDIA_ROOT

@csrf_exempt
def detectView(request):
	if request.method =="POST":
		user_id = request.POST['user_id']
		token = request.POST['token']
		url = 'http://localhost:3001/apis/token/verify/{}/{}'.format(user_id,token)
		response_data = requests.get(url).json()

		if not response_data["authenticated"]:
			# return HttpResponse(status=401) #unauthorized
			res = {
			"success":False,
			"message":"Unauthorized"
			}
			return JsonResponse(res)
		try:
			image_file = request.FILES['image']
		

			old_image = Old_image.objects.create(image=image_file)
		    
			old_absolute_file_path = os.path.join(MEDIA_ROOT, old_image.image.name)
		    
			model_cfg = os.path.join(BASE_DIR, "yoloface","cfg","yolov3-face.cfg")
			model_weights = os.path.join(BASE_DIR, "yoloface","model-weights","yolov3-wider_16000.weights")
			output_dir = os.path.join(BASE_DIR, "yoloface","outputs")


			new_image_path,number_of_faces = yoloface.run_yoloface(image_path=old_absolute_file_path,
											    	model_cfg=model_cfg,
											    	model_weights=model_weights,
											    	output_dir=output_dir)
			new_image_path = str(new_image_path)
			old_image.new_image_file_name = new_image_path
			old_image.save()
			new_image = open(new_image_path, "rb")
			new_image_utf8 = base64.b64encode(new_image.read()).decode('utf-8')
			res = {
			"success":True,
			"number_of_faces":number_of_faces,
			"image" : new_image_utf8
			}
			return JsonResponse(res)
		except KeyError:
			res = {
			"success":False,
			"message":"No image was sent"
			}
			return JsonResponse(res)

	else:
		return render(request,"index.html")

