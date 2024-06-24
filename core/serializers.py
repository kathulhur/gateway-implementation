from rest_framework import serializers
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from . import services
from typing import Union, List

class InferenceSerializer(serializers.Serializer):
    inference_service = serializers.CharField()

    input_files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )

    model_artifacts = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        default=list
    )

    def validate_inference_service(self, value):

        inference_service_available = services.inferenceServiceManager.check_inference_service_availability(value)

        if inference_service_available:
            return value
        
        raise serializers.ValidationError(f'The inference service with the tag {value} does not exist or is unavailable.')
    
    
    def validate(self, attrs):
        inference_service_name = attrs.get('inference_service')


        metadata = services.inferenceServiceManager.get_inference_service_metadata(inference_service_name)
        input_files = attrs.get('input_files')
        model_artifacts = attrs.get('model_artifacts')

        if len(input_files) != len(metadata['input_files']):
            raise serializers.ValidationError({ 'input_files': f'There must be {len(metadata["input_files"])} input files attached' })

        if len(model_artifacts) != len(metadata['model_artifacts']):
            raise serializers.ValidationError({ 'model_artifacts': f'There must be {len(metadata["model_artifacts"])} model artifacts attached' })


        for i in range(len(model_artifacts)):
            file = model_artifacts[i]
            if isinstance(file, TemporaryUploadedFile):
                file_extension = '.' + file.name.split('.')[-1]
                if file_extension not in metadata['model_artifacts'][i]:
                    raise serializers.ValidationError({ 'input_files': f'The file extension of a model artifact is invalid' })
                
            elif isinstance(file, InMemoryUploadedFile):
                file_extension = '.' + file.name.split('.')[-1]
                if file_extension not in metadata['model_artifacts'][i]:
                    raise serializers.ValidationError({ 'input_files': f'The file extension of a model artifact is invalid' })
                

        return attrs
    
