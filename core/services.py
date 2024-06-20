from .models import InferenceServiceMapping
import requests

class InferenceServiceManager:

    def __init__(self):
        self.inference_services = dict()


    def get_available_inference_services_metadata(self):
        
        inference_services = InferenceServiceMapping.objects.all()
        self.inference_services = dict()
        for service in inference_services:
            try:
                response = requests.get(service.information_url)
                self.inference_services[service.service_name] = response.json()
            except Exception as e:
                print(f'==========Cannot establish connection with {service.service_name} Inference Service.')
                print(e)

        return self.inference_services


    def get_inference_service_metadata(self, inference_service_name):
        if inference_service_name in self.inference_services:
            return self.inference_services[inference_service_name]
        
        inference_service_exists = InferenceServiceMapping.objects.filter(service_name=inference_service_name).exists()

        if not inference_service_exists:
            raise Exception('Inference service does not exist or is unavailable at the moment')
        

        inference_service = InferenceServiceMapping.objects.get(service_name=inference_service_name)

        response = requests.get(inference_service.information_url)
        
        metadata = response.json()
        self.inference_services[inference_service_name] = metadata

        return metadata
    

    def get_inference_service_by_name(self, service_name):

        return InferenceServiceMapping.objects.get(service_name=service_name)
    

    def check_inference_service_availability(self, inference_service_name):
        if inference_service_name in self.inference_services:
            return True
        
        return InferenceServiceMapping.objects.filter(service_name=inference_service_name).exists()



inferenceServiceManager = InferenceServiceManager()