from rest_framework import serializers
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
from . import common
from typing import Union, List

class InferenceSerializer(serializers.Serializer):
    inference_service = serializers.CharField()

    input_files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )

    model_artifacts = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )

    def validate_inference_service(self, value):

        service_name_exists = common.check_inference_service_existence(value)

        if service_name_exists:
            return value
        
        raise serializers.ValidationError(f'The inference service with the tag {value} does not exist or is unavailable.')
    

    def validate_input_files(self, value):
        metadata = common.get_inference_service_metadata(value)

        if len(value) != len(metadata['input_files']):
            raise serializers.ValidationError(f'There must be {len(metadata["input_files"])} input files attached')
        return value

    def validate_model_artifacts(self, value: List[Union[TemporaryUploadedFile, InMemoryUploadedFile]]):
        metadata = common.get_inference_service_metadata(value)

        if len(value) != len(metadata['model_artifacts']):
            raise serializers.ValidationError(f'There must be {len(metadata["model_artifacts"])} model artifacts attached')


        for i in range(len(value)):
            file = value[i]
            if isinstance(file, TemporaryUploadedFile):
                file_extension = '.' + file.name.split('.')[-1]
                if file_extension not in metadata['model_artifacts'][i]:
                    raise serializers.ValidationError(f'The file extension of a model artifact is invalid')
                
            elif isinstance(file, InMemoryUploadedFile):
                file_extension = '.' + file.name.split('.')[-1]
                if file_extension not in metadata['model_artifacts'][i]:
                    raise serializers.ValidationError(f'The file extension of a model artifact is invalid')
                

        return value
    
