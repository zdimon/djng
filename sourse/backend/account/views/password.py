import random
from rest_framework.authtoken.models import Token
from account.utils import send_email
from django.utils.translation import ugettext_lazy as _
from account.signals import reset_password_token_created, pre_password_reset, post_password_reset
from django.core.exceptions import ValidationError
from rest_framework import generics
from account.serializers import PasswordTokenSerializer
from django.conf import settings
from account.serializers import EmailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from account.models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, get_password_reset_lookup_field
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')



class ResetPasswordConfirm(generics.GenericAPIView):
    throttle_classes = {}
    permission_classes = {}
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status', 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        '''
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            reset_password_token.delete()
            return Response({'status': 1, 'message': _('Your token has expired!')}, status=status.HTTP_404_NOT_FOUND)
        '''
        if reset_password_token.user.eligible_for_reset():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
            '''
            try:
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                )
            except ValidationError as e:
                raise exceptions.ValidationError({
                    'password': e.messages
                })
            '''

            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'status': 0, 'message': _('Your password has been changed.')})


class ResetPasswordRequestToken(generics.GenericAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)

        clear_expired(now_minus_expiry_time)

        users = User.objects.filter(**{'{}__iexact'.format(get_password_reset_lookup_field()): email})

        active_user_found = False

        for user in users:
            if user.eligible_for_reset():
                active_user_found = True

        if not active_user_found and not getattr(settings, 'DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE', False):
            raise exceptions.ValidationError({
                'email': [_(
                    'There is no active user associated with this e-mail address or the password can not be changed')],
            })

        for user in users:
            if user.eligible_for_reset():
                token = None

                if user.password_reset_tokens.all().count() > 0:
                    token = user.password_reset_tokens.all()[0]
                else:
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
                        ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, '')
                    )

                reset_password_token_created.send(sender=self.__class__, instance=self, reset_password_token=token)

        return Response({'status': 'OK'})





class SaveNewPasswordView(APIView):
   
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        new = request.data['new']
        request.user.userprofile.set_password(new)
        request.user.userprofile.save()
        return Response({'status': 0, 'message': _('Your password has been changed.')})
