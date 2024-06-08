from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

class InformationEndpointTest(APITestCase):

    def test_information_endpoint_available(self):
        response = self.client.get('/api/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        response = self.client.get('/api/inference/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_information_endpoint_returns_image(self):
        response = self.client.get('/api/inference/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get('Content-Type'), 'image/png')




