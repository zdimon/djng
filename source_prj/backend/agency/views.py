from django.http import HttpResponseRedirect


# def to_agency_page(request):
#     print(request.user.groups.all().values_list('name', flat=True))
#     if request.user.is_authenticated and 'agency-director' in request.user.groups.all().values_list('name', flat=True):
#         print(1)
#         return HttpResponseRedirect('/agency/')
#     else:
#         return HttpResponseRedirect('/admin/')
