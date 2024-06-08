from django.shortcuts import render
from django.http import HttpResponse
import json, pathlib
# Create your views here.

MODULE_DIR = pathlib.Path(__file__).parent
sample_image_path = MODULE_DIR / 'assets' / 'image.png'
def info(request):
    dummyInferenceServicesMetadata = {
        'available_inference_services': {
            'YOLO7': {
                'input_files': [ ['image/*'] ],
                'model_artifacts': [ ['.pt'] ],
            },
            'YOLOv8': {
                'input_files': [ ['image/*', 'video/*'] ],
                'model_artifacts': [ ['.pt'] ],
            }
        }
    }    

    return HttpResponse(json.dumps(dummyInferenceServicesMetadata), content_type='application/json')
    

def inference(request):
    image_data = None
    with sample_image_path.open('rb') as f:
        image_data = f.read()
    
    return HttpResponse(image_data, content_type='image/png')