from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from flask_socketio import emit
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from corsheaders.defaults import default_headers

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        message = data.get('message')
        if message:
            emit('message', {'message': message}, namespace='/chat')
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)

class ChatView(APIView):
    parser_classes = (JSONParser,)
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        message = data.get('message')
        if message:
            emit('message', {'message': message}, namespace='/chat')
            return Response({'message': 'Message sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)