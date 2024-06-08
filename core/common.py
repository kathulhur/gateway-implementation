
from .models import InferenceServiceMapping
import requests


def check_inference_service_existence(service_name):
    """
        Checks whether the inference service exists
    """
    if InferenceServiceMapping.objects.filter(service_name=service_name).exists():
        return True

    return False


def get_available_inference_services():
    """
        Fetch the metadata of all the inference services in the database
    """
    inference_services = InferenceServiceMapping.objects.all()
    inference_services_metadata = dict()
    for service in inference_services:

        response = requests.get(service.information_url)
        metadata = response.json()

        inference_services_metadata[service.name] = metadata

    return {
        'available_inference_services': inference_services_metadata
    }



def get_inference_service_metadata(service_name):
    """
        Fetch the inference service metadata given the service name
    """
    inference_service_exists = check_inference_service_existence(service_name)

    if not inference_service_exists:
        raise Exception(f'The inference service with the tag {service_name} does not exist or is unavailable.')
    
    inference_service = InferenceServiceMapping.objects.get(service_name)
    response = requests.get(inference_service.information_url)

    return response.json()


    
    