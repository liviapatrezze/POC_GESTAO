from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hello.models import Greeting


class HelloView(APIView):
    def get(self, request: Request) -> Response:
        greeting = Greeting.objects.order_by("id").first()
        if greeting is None:
            return Response({"mensagem": ""}, status=404)
        return Response({"mensagem": greeting.mensagem})
