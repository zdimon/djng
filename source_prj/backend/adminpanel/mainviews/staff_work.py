"""
   Functional for working with staff users
"""
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from .mainview import BaseAdminView
from adminpanel.modelworks.staff_work.staff_work import StaffWork
from adminpanel.modelworks.group_work.group_work import GroupWork
from adminpanel.forms.user_form import UserForm, UserFormEdit

"""
    Main page for staffs
"""
class StaffWorkView(BaseAdminView, ListView):
    template_name = 'staff/staffwork.html'
    context_object_name = 'users'

    def get_queryset(self):
        return StaffWork.get_all_staff()

    def get_context_data(self, **kwargs):
        context = super(StaffWorkView, self).get_context_data(**kwargs)
        context['tab_staff'] = True
        return context


"""
    Show form for add new staff
"""
class FormAddNewStaff(BaseAdminView, TemplateView):
    template_name = "staff/add_form_staff.html"

    def get_context_data(self, **kwargs):
        context = super(FormAddNewStaff, self).get_context_data(**kwargs)
        context['tab_staff'] = True
        context['groupss'] = GroupWork.get_all_groups()
        return context


"""
    Create new staff
"""
class CreateStaff(BaseAdminView, CreateView):
    form_class = UserForm
    template_name = "staff/add_form_staff.html"
    success_url = '/adminpanel/staff/view'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.set_password(instance.password)
        instance.save()
        """
            Save groups
        """
        dict_query = dict(self.request.POST)
        if dict_query.get('groups', False):
            for group in dict_query['groups']:
                my_group = GroupWork.get_group(group)
                my_group.user_set.add(instance)
        return super(CreateStaff, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['data'] = self.request.POST
        context['groupss'] = GroupWork.get_all_groups()
        context['tab_staff'] = True
        print(context)

        return self.render_to_response(context)


"""
    Edit staff
"""
class EditStaff(BaseAdminView, UpdateView):
    form_class = UserFormEdit
    template_name = "staff/edit_staff.html"
    success_url = '/adminpanel/staff/view'
    model = User
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super(EditStaff, self).get_context_data(**kwargs)
        context['groupss'] = GroupWork.get_all_groups()
        context['tab_staff'] = True

        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        """
            Save groups
        """
        #get object to save(user data)
        self.object = self.get_object()
        dict_query = dict(self.request.POST)
        if dict_query.get('groups', False):
            StaffWork.clean_group_user(self.object.id)
            for group in dict_query['groups']:
                #get group and add to user
                my_group = GroupWork.get_group(group)
                my_group.user_set.add(instance)
        else:
            StaffWork.clean_group_user(self.object.id)
        return super(EditStaff, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['data'] = self.request.POST
        context['groupss'] = GroupWork.get_all_groups()
        context['tab_staff'] = True
        print(context)

        return self.render_to_response(context)


"""
    Delete staff
"""
class DeleteStaff(BaseAdminView, DeleteView):

    def get(self, request, *args, **kwargs):
        StaffWork.delete_staff(kwargs)
        redirect_url = 'staffview'
        return redirect(redirect_url)