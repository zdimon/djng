class BaseLogMixin:
    '''
    Base Log mixin class
    '''

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        user = request.user
        if user.is_authenticated:
            username = user.username
        elif self.log_type == 'login' and response.status_code == 200:
            username = response.data['user']['username']

        if locals().get('username'):
            user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            self.log(username=username, ip_address=ip_address, user_agent=user_agent, log_type=self.log_type)
        return response

    def log(self, username, ip_address, user_agent, log_type):
        pass
