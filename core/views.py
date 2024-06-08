from django.http import HttpResponse
import json, pathlib
from . import common
from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import InferenceSerializer
# Create your views here.

MODULE_DIR = pathlib.Path(__file__).parent
sample_image_path = MODULE_DIR / 'assets' / 'image.png'

def info(request):
    return HttpResponse(json.dumps(common.get_available_inference_services()), content_type='application/json')
    

class InferenceView(APIView):


    def post(self, request):
        serializer = InferenceSerializer(data=request.data)
        if serializer.is_valid():
            image_data = None
            with sample_image_path.open('rb') as f:
                image_data = f.read()
            
            return HttpResponse(image_data, content_type='image/png')
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    