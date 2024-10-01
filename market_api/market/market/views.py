from abc import ABC, abstractmethod
from django.db import models

from rest_framework import (
    mixins,
    status,
    viewsets,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers

class APIView(ABC, viewsets.GenericViewSet):
    
    @abstractmethod
    def model_name(self) -> str:
        ...

    @property
    def plural_name(self) -> str:
        return f"{self.model_name()}s"

class CreateAPIView(ABC, mixins.CreateModelMixin):
    
    @abstractmethod
    def create(self, request: Request, *args, **kwargs) -> Response:
        ...

class RetrieveAPIView(ABC, mixins.RetrieveModelMixin):
    
    @abstractmethod
    def retrieve(self, request: Request, id: int, *args, **kwargs) -> Response:
        ...

class UpdateAPIView(ABC, mixins.UpdateModelMixin):
    
    @abstractmethod
    def update(self, request: Request, id: int, *args, **kwargs) -> Response:
        ...

class DeleteAPIView(ABC, mixins.DestroyModelMixin):
    
    @abstractmethod
    def destroy(self, request: Request, id: int, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ListAPIView(ABC, mixins.ListModelMixin):
    
    @abstractmethod
    def list(self, request: Request, *args, **kwargs) -> Response:
        ...

class CRUDAPIView(
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DeleteAPIView,
    ListAPIView,
    APIView,
):
    
    @property
    def model(self) -> models.Model:
        return self.get_model()

    @property
    def serializer(self) -> serializers.Serializer:
        return self.get_serializer()

    @abstractmethod
    def get_model(self) -> models.Model:
        ...

    @abstractmethod
    def get_serializer(self) -> serializers.Serializer:
        ...

    @abstractmethod
    def list_model(self) -> list:
        ...

    def not_found_by_id(self) -> Response:
        return Response(
            {"message": f"{self.model_name()} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    def get_object(self, id: int) -> models.Model:
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None
    
    def list(self, request: Request, *args, **kwargs) -> Response:
        instances: list[models.Model] = self.list_model()
        serializer: serializers.Serializer = self.serializer(instances, many=True)
        return Response({
            self.plural_name: serializer.data
        })

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer: serializers.Serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def retrieve(self, request: Request, id: int, *args, **kwargs) -> Response:
        model_ = self.get_object(id)
        if not model_:
            return self.not_found_by_id()
        serializer: serializers.Serializer = self.serializer(model_)
        return Response(serializer.data)
    
    def update(self, request: Request, id: int, *args, **kwargs) -> Response:
        model_ = self.get_object(id)
        if not model_:
            return self.not_found_by_id()
        serializer: serializers.Serializer = self.serializer(model_, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def destroy(self, request: Request, id: int, *args, **kwargs) -> Response:
        model_ = self.get_object(id)
        if not model_:
            return self.not_found_by_id()
        model_.delete()
        return Response(
            {"message": f"{self.model_name()} deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )