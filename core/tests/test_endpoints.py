from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
import pathlib
from core.models import InferenceServiceMapping


MODULE_DIR = pathlib.Path(__file__).parent

image_file_path = MODULE_DIR / 'assets' / 'image.png'
yolov8_file_path = MODULE_DIR / 'assets' / 'yolov8n.pt'


class InformationEndpointTest(APITestCase):

    def test_information_endpoint_available(self):
        response = self.client.get('/api/info/')
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_information_endpoint_returns_json(self):
        response = self.client.get('/api/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get('Content-Type'), 'application/json')


    @patch('core.services.inferenceServiceManager')
    def test_information_endpoint_contains_the_expected_data(self, mockedInferenceServiceManager):
        mockedInferenceServiceManager.get_available_inference_services_metadata.return_value = {
            'available_inference_services': {
                'YOLOv8': {
                    'input_files': [],
                    'model_artifacts': []
                },
                'YOLOv9': {
                    'input_files': [],
                    'model_artifacts': []
                },
            }
        }

        
        response = self.client.get('/api/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get('Content-Type'), 'application/json')

        data = response.json()

        self.assertIn('available_inference_services', data)
        self.assertIn('YOLOv8', data['available_inference_services'])
        self.assertIn('YOLOv9', data['available_inference_services'])

        for metadata in data['available_inference_services'].values():
            self.assertIn('input_files', metadata)
            self.assertIn('model_artifacts', metadata)
        
        

class InferenceEndpointTest(APITestCase):

    def test_information_endpoint_available(self):
        response = self.client.post('/api/inference/')
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_inference_endpoint_without_input_results_to_bad_request(self):
        response = self.client.post('/api/inference/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('inference_service', response.data)
        self.assertIn('input_files', response.data)
        self.assertIn('model_artifacts', response.data)

    @patch('requests.post')
    @patch('core.services.inferenceServiceManager')
    def test_inference_endpoint_with_valid_input(self, mockedInferenceServiceManager, mockedPost):


        mockedInferenceServiceManager.check_inference_service_availability.return_value = True
        mockedInferenceServiceManager.get_inference_service_metadata.return_value = {
            'input_files': [ ['image'] ],
            'model_artifacts': [ ['.pt'] ]
        }
        mockedInferenceServiceManager.get_inference_service_by_name.return_value = InferenceServiceMapping.objects.create(service_name='YOLOv8', ip_address='127.0.0.1', port=8000)


        mockedPost.return_value.status_code = 200
        mockedPost.return_value.headers = {'Content-Type': 'image/png'}

        with yolov8_file_path.open('rb') as f:
            mockedPost.return_value.content = f.read()
            
        image = None
        with image_file_path.open('rb') as f:
            image = SimpleUploadedFile('image.png', f.read(), 'image/png')

        model_artifact = None
        with yolov8_file_path.open('rb') as f:
            model_artifact = SimpleUploadedFile('yolov8n.pt', f.read(), 'application/octet-stream')

            
        response = self.client.post('/api/inference/', {
            'inference_service': 'YOLOv8',
            'input_files': [image],
            'model_artifacts': [model_artifact],
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get('Content-Type'), 'image/png')
        mockedPost.assert_called_once()
        mockedInferenceServiceManager.check_inference_service_availability.assert_called_once()
        mockedInferenceServiceManager.get_inference_service_metadata.assert_called_once()
        mockedInferenceServiceManager.get_inference_service_by_name.assert_called_once()


    @patch('core.services.inferenceServiceManager')
    def test_inference_endpoint_excess_input(self, mockedInferenceServiceManager):
        mockedInferenceServiceManager.get_inference_service_metadata.return_value = {
            'input_files': [ ['image'] ],
            'model_artifacts': [ ['.pt'] ]
        }

        image = None
        with image_file_path.open('rb') as f:
            image = SimpleUploadedFile('image.png', f.read(), 'image/png')

        image_2 = None
        with image_file_path.open('rb') as f:
            image_2 = SimpleUploadedFile('image.png', f.read(), 'image/png')

        model_artifact = None
        with yolov8_file_path.open('rb') as f:
            model_artifact = SimpleUploadedFile('yolov8n.pt', f.read(), 'application/octet-stream')

            
        response = self.client.post('/api/inference/', {
            'inference_service': 'YOLOv8',
            'input_files': [image, image_2],
            'model_artifacts': [model_artifact],
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('input_files', response.data)


    






