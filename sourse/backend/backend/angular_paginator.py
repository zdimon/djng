from rest_framework.response import Response
from collections import OrderedDict
from rest_framework import pagination

class AngularPagination(pagination.LimitOffsetPagination):

    def get_paginated_response(self, data):
        #print(data)
        out_dict = {}
        obj_list = []
        for i in data:
            out_dict[i['id']] = i
        out_list = []
        for i in data:
            out_list.append(i['id'])  
            obj_list.append(i)          
        return Response(OrderedDict([
            ('totalCount', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', out_dict),
            ('results_list', obj_list),
            ('ids', out_list),
            ('status', 0)
        ]))

