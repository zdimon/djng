"""
    Functional for working with a models Group, Permission
"""

from django.contrib.auth.models import Group, Permission


class GroupWork:

    @staticmethod
    def get_all_groups():
        return Group.objects.all()

    @staticmethod
    def add_new_group(name):
        new_group = Group(name=name)
        new_group.save()
        return new_group

    @staticmethod
    def delete_group(kwargs):
        Group.objects.get(pk=kwargs['pk']).delete()

    @staticmethod
    def get_group(name):
        return Group.objects.filter(name=name).get()

    @staticmethod
    def get_all_permissions():
        return Permission.objects.all()

    @staticmethod
    def clean_permissions_group(group_id):
       group = Group.objects.get(id=group_id)
       print(group)
       group.permissions.clear()

    @staticmethod
    def get_permission(codename):
        return Permission.objects.filter(codename=codename).get()