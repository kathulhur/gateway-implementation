from django.http import HttpResponse
import json, pathlib, requests
from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import InferenceSerializer
from . import services
from typing import Union
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
# Create your views here.

MODULE_DIR = pathlib.Path(__file__).parent
sample_image_path = MODULE_DIR / 'assets' / 'image.png'

def info(request):
    return HttpResponse(json.dumps(services.inferenceServiceManager.get_available_inference_services_metadata()), content_type='application/json')
    

class InferenceView(APIView):
    def post(self, request):
        serializer = InferenceSerializer(data=request.data)
        if serializer.is_valid():
            inference_service_name = serializer.validated_data['inference_service']
            input_files: Union[InMemoryUploadedFile, TemporaryUploadedFile]  = serializer.validated_data['input_files']
            model_artifacts: Union[InMemoryUploadedFile, TemporaryUploadedFile] = serializer.validated_data['model_artifacts']

            inference_service = services.inferenceServiceManager.get_inference_service_by_name(inference_service_name)

            input_files_attachment = []
            for file in input_files:
                if isinstance(file, InMemoryUploadedFile):
                    input_files_attachment.append(('input_files', file.file))
                elif isinstance(file, TemporaryUploadedFile):
                    input_files_attachment.append(('input_files', file.file))
            
            model_artifacts_attachment = []
            for file in model_artifacts:
                if isinstance(file, InMemoryUploadedFile):
                    model_artifacts_attachment.append(('model_artifacts', file.file))
                    
                elif isinstance(file, TemporaryUploadedFile):
                    model_artifacts_attachment.append(('model_artifacts', file.file))
            
            response = requests.post(inference_service.inference_url, files=input_files_attachment + model_artifacts_attachment)
            
            
            return HttpResponse(response.content, content_type=response.headers.get('Content-Type'), status=response.status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    