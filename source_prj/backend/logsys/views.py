from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend

from logsys.models import Log
from logsys.serializers import LogSerializer
from logsys.filters import LogsFilter
from rest_framework.response import Response


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    filter_backends = DjangoFilterBackend,
    filterset_fields = ['username', 'ip_address', 'created_at__lte', 'created_at__gte', 'type']
    filter_class = LogsFilter

    def destroy(self, request, *args, **kwargs):
        delete_this = request.data['ids_for_delete']
        logs = Log.objects.filter(id__in=delete_this)
        try:
            logs._raw_delete(logs.db)
            response = {'status': 0, 'message': 'Ok'}
        except:
            response = {'status': 1, 'message': 'Error'}
        return Response(status=status.HTTP_204_NO_CONTENT, data=response)

    def create(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def bulkDelete(self, request, *args, **kwargs):
        for i in request.data['itemsIdsForDelete']:
            l = Log.objects.get(pk=i)
            l.delete()
        response = {'status': 0, 'message': 'Ok'}
        return Response(response)
