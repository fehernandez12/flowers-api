from rest_framework import viewsets, status
from rest_framework.response import Response
from flowers.serializers import ImagePredictionSerializer

# Create your views here.
class ImageViewSet(viewsets.GenericViewSet):
    serializer_class = ImagePredictionSerializer

    def create(self, request):
        serializer = ImagePredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        prediction = serializer.save()
        return Response(prediction, status=status.HTTP_201_CREATED)