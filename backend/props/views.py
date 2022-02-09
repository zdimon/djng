from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import Props, Value
from backend.settings import DOMAIN

# class PropsListView(APIView):
#     """
#        Props list
#     """
#     permission_classes = (AllowAny,)
#     def get(self, request, gender, format=None):
#         data = {'one': [], 'many': []}
#         if(gender=='female'):
#             props = Props.objects.filter(for_woman=True, type='one')
#         else:
#             props = Props.objects.filter(for_man=True, type='one')
#         for p in props:
#             values = []
#             for v in Value.objects.filter(prop=p):
#                 values.append({'value': v.id, 'title': v.name, 'icon': DOMAIN+v.icon.url})
#             data['one'].append({'type': p.type, 'alias': p.alias, 'title': p.name, 'icon': DOMAIN+p.icon.url, 'category': p.category, 'values': values})

#         if(gender=='female'):
#             props = Props.objects.filter(for_woman=True, type='many')
#         else:
#             props = Props.objects.filter(for_man=True, type='many')
#         for p in props:
#             values = []
#             for v in Value.objects.filter(prop=p):
#                 values.append({'value': v.id, 'title': v.name})
#             data['many'].append({'alias': p.alias, 'title': p.name, 'values': values})
            
#         return Response(data)


class PropsListView(APIView):
    """
       Props list
    """
    permission_classes = (AllowAny,)
    def get(self, request, gender, format=None):
        data = []
        if(gender=='female'):
            props = Props.objects.filter(for_woman=True)
        else:
            props = Props.objects.filter(for_man=True)
        for p in props:
            values = []
            for v in Value.objects.filter(prop=p):
                values.append({'id': v.id, 'value': v.id, 'title': v.name, 'icon': DOMAIN+v.icon.url})
            data.append({'id': p.id, 'category': p.category, 'type': p.type, 'alias': p.alias, 'title': p.name, 'values': values, 'icon': DOMAIN+p.icon.url})
            
        return Response(data)

class PropsSaveView(APIView):
    """
       Props save
    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        data = { 'status': 0, "message": 'OK' }
        return Response(data)