"""
    Form for User model(add new staff user)
"""

from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active', 'password']

        error_messages = {
                             'email': {'required': "Пожалуйста введите email",
                                       'max_length':"Не более 30 символов",
                                       'unique': "Этот email уже используется введите другой"
                                      },
                             'username': {'required': "Пожалуйста введите имя",
                                          'max_length': "Не более 30 символов",
                                          'unique': "Это имя уже используется введите другое"
                                      }
                         }

    def clean(self):
        # check isset username
        if User.objects.filter(username=self.cleaned_data['username']):
            raise ValidationError('Введенное имя уже существует!Выберите другое', code='invalid')
        return self.cleaned_data

class UserFormEdit(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_superuser']