from rest_framework.serializers import ModelSerializer
from mainapp.models import Board


class BoardSerializer(ModelSerializer):
	class Meta:
		model = Board
		fields = "__all__"
