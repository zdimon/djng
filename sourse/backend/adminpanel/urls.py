from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from .mainviews.group_work_view import (GroupWorkView, GroupDelete, AddNewGroup, GroupEdit)
from .mainviews.staff_work import (StaffWorkView, FormAddNewStaff, CreateStaff, EditStaff, DeleteStaff)
from .mainviews.feed_work import (GetManFeedForModerate, GetWomanFeedForModerate, ViewFeed)
from .mainviews.user_work import ViewUserProfile
from .mainviews.feedappruve import AppruveFeed
from .mainviews.mainview import MainView

"""
   Urls for group staff
"""
group_patterns = [
    path('view/', GroupWorkView.as_view(), name='groupview'),
    path('delete/<int:pk>/', GroupDelete.as_view(), name='groupdelete'),
    path('add/', AddNewGroup.as_view(), name='ajax_group_new'),
    path('edit/<int:pk>/', GroupEdit.as_view(), name='groupedit')
]

"""
   Urls for users staff
"""
users_patterns = [
    path('view/', StaffWorkView.as_view(), name='staffview'),
    path('delete/<int:pk>/', DeleteStaff.as_view(), name='staffdelete'),
    path('addform/', FormAddNewStaff.as_view(), name='addform'),
    path('create/', CreateStaff.as_view(), name='createstaff'),
    path('edit/<int:pk>/', EditStaff.as_view(), name='editstaff')
]

"""
    Urls for feed moderate
"""
feedmode_patterns = [
    path('approvedfeed/<int:pk>/<str:gender>/', AppruveFeed.as_view(), name='approvedfeed')
]

"""
    Urls for Users 
"""
user_profile_patterns = [
    path('profile/<int:pk>/', ViewUserProfile.as_view(), name='viewusrprofile')
]

"""
    Urls for Feeds 
"""
feeds_profile_patterns = [
    re_path(r'^getman/(?:page/(?P<page>\d+)/)?$', GetManFeedForModerate.as_view(), name='getmenfeed'),
    re_path(r'^getwoman/(?:page/(?P<page>\d+)/)?$', GetWomanFeedForModerate.as_view(), name='getwomanfeed'),
    path('view/<int:pk>/', ViewFeed.as_view(), name='viewfeed')
]

"""
    Main urls 
"""
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='loginadmin'),
    path('logoutadmin/', auth_views.LogoutView.as_view(), name='logoutadmin'),
    path('', MainView.as_view(), name='homeadmin'),
    path('group/', include(group_patterns)),
    path('staff/', include(users_patterns)),
    path('feed/', include(feeds_profile_patterns)),
    path('users/', include(user_profile_patterns)),
    path('feedmode/', include((feedmode_patterns)))
]
