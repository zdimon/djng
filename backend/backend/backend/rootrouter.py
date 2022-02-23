from rest_framework import routers
from collections import OrderedDict

class RootRouter(routers.DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)


        api_root_dict['register-man'] = 'register-man'
        api_root_dict['user-online'] = 'user-online'
        api_root_dict['user-logout'] = 'user-logout'
        api_root_dict['celery-task'] = 'celery-task'

        api_root_dict['room-list'] = 'room-list'
        api_root_dict['room-select'] = 'room-select'
        api_root_dict['room-add'] = 'room-add'
        api_root_dict['room-send-message'] = 'room-send-message'
        api_root_dict['room-stop'] = 'room-stop'
        api_root_dict['room-get-video-list'] = 'room-get-video-list'
        api_root_dict['room-get-photo-list'] = 'room-get-photo-list'



        api_root_dict['user-online-list'] = 'user-online-list'
        api_root_dict['update-socket-id'] = 'update-socket-id'
        api_root_dict['message-list'] = 'message-list'


        api_root_dict['webrtc-offer'] = 'webrtc-offer'
        api_root_dict['webrtc-camera-on'] = 'webrtc-camera-on'
        api_root_dict['webrtc-camera-off'] = 'webrtc-camera-off'
        api_root_dict['webrtc-camera-show'] = 'webrtc-camera-show'
        api_root_dict['webrtc-camera-hide'] = 'webrtc-camera-hide'

        api_root_dict['feed-of-user'] = 'feed-of-user'
        api_root_dict['feed-subscribe'] = 'feed-subscribe'
        api_root_dict['feed-subscriber-list'] = 'feed-subscriber-list'


        api_root_dict['get-translation'] = 'get-translation'


        api_root_dict['account-add-credits'] = 'account-add-credits'
        api_root_dict['account-set-language'] = 'account-set-language'
        api_root_dict['account-register-agency'] = 'account-register-agency'
        api_root_dict['account-register-woman'] = 'account-register-woman'
        api_root_dict['account-register-man'] = 'account-register-man'
        api_root_dict['account-change-password'] = 'account-change-password'
        api_root_dict['account-reset-password'] = 'account-reset-password-request'
        api_root_dict['account-reset-password-validate'] = 'account-reset-password-validate'
        api_root_dict['account-reset-password-confirm'] = 'account-reset-password-confirm'
        api_root_dict['account-favorites'] = 'account-favorites'
        api_root_dict['account-detail'] = 'account-detail'


        # online
        api_root_dict['user-online-count'] = 'user-online-count'

        #####  Media
        api_root_dict['media-photo-list'] = 'media-photo-list'
        api_root_dict['media-change-role'] = 'media-change-role'

        api_root_dict['photo-list'] = 'photo-list'
        api_root_dict['photo-delete'] = 'photo-delete'
        api_root_dict['photo-crop'] = 'photo-crop'

        api_root_dict['props-list'] = 'props-list'

        api_root_dict['gallery-list'] = 'gallery-list'
        api_root_dict['gallery-detail'] = 'gallery-detail'

        api_root_dict['settings-plan'] = 'settings-plan'
        api_root_dict['settings-add-credits'] = 'settings-add-credits'
        api_root_dict['settings-smiles'] = 'settings-smiles'
        api_root_dict['settings-stickers'] = 'settings-stickers'

        api_root_dict['payment-list'] = 'payment-list'

        return self.APIRootView.as_view(api_root_dict=api_root_dict)
