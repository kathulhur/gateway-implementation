from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
import pathlib


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


    @patch('core.common.get_available_inference_services')
    def test_information_endpoint_contains_the_expected_data(self, mocked_get_available_inference_services):

        mocked_get_available_inference_services.return_value = {
            'available_inference_services': {
                'YOLOv8': {
                    'input_files': [],
                    'model_artifacts': []
                }
            }
        }

        
        response = self.client.get('/api/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get('Content-Type'), 'application/json')
        mocked_get_available_inference_services.assert_called_once()

        data = response.json()

        self.assertIn('available_inference_services', data)

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

    @patch('core.common.get_inference_service_metadata')
    @patch('core.common.check_inference_service_existence')
    def test_inference_endpoint_with_valid_input(self, mocked_check_inference_service_existence, mocked_get_inference_service_metadata):

        mocked_get_inference_service_metadata.return_value = {
            'input_files': [ ['image'] ],
            'model_artifacts': [ ['.pt'] ]
        }

        mocked_check_inference_service_existence.return_value = True
        

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


    @patch('core.common.get_inference_service_metadata')
    @patch('core.common.check_inference_service_existence')
    def test_inference_endpoint_excess_input(self, mocked_check_inference_service_existence, mocked_get_inference_service_metadata):

        mocked_get_inference_service_metadata.return_value = {
            'input_files': [ ['image'] ],
            'model_artifacts': [ ['.pt'] ]
        }

        mocked_check_inference_service_existence.return_value = True
        

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


    






