from rest_framework.test import APITestCase
from rest_framework import status

class InformationEndpointTest(APITestCase):
     def test_information_endpoint_available(self):
        response = self.client.get('/api/inference/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InferenceEndpointTest(APITestCase):

    def test_information_endpoint_available(self):
        response = self.client.get('/api/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



