from rest_framework.response import Response
from rest_framework.views import APIView



class MenuView(APIView):

    def get(self, request, *args, **kwargs):
        menu = [
            { 'id': 1, 
              'name': 'Users', 
              'title': 'Users', 
              'icon': 'flaticon-interface-7', 
              'page': '/user'
            }
        ]
        data = {'results_list': menu}
        return Response(data)