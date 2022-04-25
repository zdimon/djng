from rest_framework.views import APIView
from rest_framework.response import Response
from django_countries.data import COUNTRIES

class CountriesListView(APIView):
    """
      Countries list
    """
    def get(self, request, format=None):
        out = []
        for k in COUNTRIES:
            out.append({"name": COUNTRIES[k], "value": k})
        return Response(out)