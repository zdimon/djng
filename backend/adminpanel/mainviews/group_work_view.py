"""
   Functional for working with staff groups
"""
from django.contrib.auth.models import Group
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect
from django.http import JsonResponse
from .mainview import BaseAdminView
from adminpanel.modelworks.group_work.group_work import GroupWork

"""
    Main page for groups
"""
class GroupWorkView(BaseAdminView, ListView):
    template_name = 'groups/viewgroup.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return GroupWork.get_all_groups()

    def get_context_data(self, **kwargs):
        context = super(GroupWorkView, self).get_context_data(**kwargs)
        context['tab_staff'] = True
        return context


"""
    Add new group(used AJAX request)
"""
class AddNewGroup(BaseAdminView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            new_group = GroupWork.add_new_group(self.request.GET['name'])
            if new_group:
                return JsonResponse({"status": True, 'id': new_group.id})
            else:
                return JsonResponse({"status": False})


"""
    Delete group (used AJAX request)
"""
class GroupDelete(BaseAdminView):

    def get(self, request, *args, **kwargs):
        GroupWork.delete_group(kwargs)
        redirect_url = 'groupview'
        return redirect(redirect_url)


"""
    Edit group
"""
class GroupEdit(BaseAdminView, UpdateView):
    template_name = "groups/permissions.html"
    success_url = '/adminpanel/group/view'
    model = Group
    fields = ['id', 'name']
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(GroupEdit, self).get_context_data(**kwargs)
        context['tab_staff'] = True
        context['permissions'] = GroupWork.get_all_permissions()
        return context

    def post(self, request, *args, **kwargs):
        """
            Save permissions for group
        """
        self.object = self.get_object()
        dict_query = dict(self.request.POST)
        if dict_query.get('permissions', False):
            GroupWork.clean_permissions_group(self.object.id)
            for permission in dict_query['permissions']:
                #get permission and add to group
                my_permission = GroupWork.get_permission(permission)
                my_permission.group_set.add(self.object)
        else:
            GroupWork.clean_permissions_group(self.object.id)
        redirect_url = 'groupview'
        return redirect(redirect_url)