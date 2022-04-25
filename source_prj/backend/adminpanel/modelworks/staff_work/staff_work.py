"""
    Functional for working with a model Users for staff users
"""

from django.contrib.auth.models import User

class StaffWork:

    @staticmethod
    def get_all_staff():
        super_users = User.objects.filter(is_superuser=True).only('id', 'first_name', "last_name")
        staff_users = User.objects.filter(is_staff=True).exclude(is_superuser=True).only('id', 'first_name', "last_name")
        return {'supers': super_users, 'staffs': staff_users}

    @staticmethod
    def delete_staff(kwargs):
        User.objects.get(pk=kwargs['pk']).delete()

    @staticmethod
    def get_single_user(kwargs):
        return User.objects.get(pk=kwargs['pk'])

    @staticmethod
    def clean_group_user(user_id):
        user = User.objects.get(id=user_id)
        user.groups.clear()