from django.urls import path, include

from .views.auth import *
from rest_framework import routers
from .views import *

from account.views.credits import AddCretitsView
from account.views.registration import RegisterAgencyView, RegisterMan, RegisterWoman, CheckValidEmail
from account.views.locale import SetLanguageView, GeoLocationView

from account.views.password import ResetPasswordConfirm, ResetPasswordRequestToken, SaveNewPasswordView

from account.views.favorites import FavoritesView
from account.views.photo import MyPhotoView
from account.views.video import MyVideoView
from account.views.profile import ProfileDetailView, ProfileCountryView

from account.views.admin.login import AdminLoginView
from account.views.admin.permissions import AdminPermissionsView
from account.views.admin.user import AdminUserView
from account.views.admin.roles import AdminRolesView
from account.views.profile import UserProfileViewSet, ProfileSaveBasicInfoView, ProfileSaveDocsView, ProfileSaveDetailView
from account.views.countries import CountriesListView

urlpatterns = [
    path('profile', UserProfileViewSet.as_view({'post': 'edit'}), name="account-edit-credits"),

    path('check_valid_email', CheckValidEmail.as_view(), name='check-valid-email'),
    path('add', AddCretitsView.as_view(), name="account-add-credits"),
    path('register/man', RegisterMan.as_view(), name="account-register-man"),
    path('register/woman', RegisterWoman.as_view(), name="account-register-woman"),
    path('register/agency', RegisterAgencyView.as_view(), name="account-register-agency"),
    path('setlanguage/<str:language>', SetLanguageView.as_view(), name="account-set-language"),
    path('reset_password', ResetPasswordRequestToken.as_view(), name="account-reset-password-request"),
    path('reset_password/confirm', ResetPasswordConfirm.as_view(), name="account-reset-password-confirm"),
    path('save_password', SaveNewPasswordView.as_view(), name="account-save-password"),
    path('favorites', FavoritesView.as_view(), name="account-faforites"),
    # path('detail/<int:id>', ProfileDetailView.as_view(), name="account-detail"),
    path('myphoto', MyPhotoView.as_view(), name="account-myphoto"),
    path('myvideo', MyVideoView.as_view(), name="account-myphoto"),

    path('adminLogin', AdminLoginView.as_view(), name="account-admin-login"),
    path('adminPermissions', AdminPermissionsView.as_view(), name="account-admin-permissions"),
    path('adminRoles', AdminRolesView.as_view(), name="account-admin-roles"),
    path('adminUser', AdminUserView.as_view(), name="account-admin-user"),
    path('countries/', ProfileCountryView.as_view(), name="profiles-countries"),

    path('detail', ProfileDetailView.as_view(), name="account-detail"),
    path('countries', CountriesListView.as_view(), name="account-countries-list"),

    path('save/info', ProfileSaveBasicInfoView.as_view(), name="account-saving-info-list"),
    path('save/detail', ProfileSaveDetailView.as_view(), name="account-saving-detail"),
    path('save/docs', ProfileSaveDocsView.as_view(), name="account-saving-docs-list"),

    path('geolocation', GeoLocationView.as_view(), name="get-geolocation"),

]
