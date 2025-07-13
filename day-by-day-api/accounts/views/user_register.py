from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializer.user_register import UserRegisterSerializer

class UserRegistrationView(APIView):
    permission_classes = [] 

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
              "message": "User registrado com sucesso!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)