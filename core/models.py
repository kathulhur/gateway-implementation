from django.db import models
import uuid

class InferenceServiceMapping(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    service_name = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.service_name} -> {self.ip_address}:{self.port}"
    
    @property
    def information_url(self):
        return f'http://{self.ip_address}:{self.port}/info/'
    

    @property
    def inference_url(self):
        return f'http://{self.ip_address}:{self.port}/inference/'