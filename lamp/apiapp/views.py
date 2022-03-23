import uuid
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from mainapp.models import Board, Task, Column
from apiapp.serializers import BoardSerializer


# task/<int:taskId>/changeColumn/
class ChangeColumnView(APIView):

	def post(self, request, taskId):
		task = get_object_or_404(Task, id=taskId)
		task.column = get_object_or_404(Column, id=request.POST["column"])
		task.save()

		return Response({"code": 200}, status=status.HTTP_200_OK)

# <str:user>/boards/
class UserBoardsView(APIView):
	serializer_class = BoardSerializer

	def post(self, request, user):
		if request.user.username != user:
			return Response({"code": 403}, status=status.HTTP_403_FORBIDDEN)

		# creating new board
		print(request.data)
		name = request.data['name']
		type_ = request.data['type']

		user_ = User.objects.get(username=user)
		b = Board.objects.create(
			name=name, type=type_,
			author=user_, token=str(uuid.uuid4())
		)
		return Response(BoardSerializer(b).data, status=status.HTTP_200_OK)

