from django.urls import path, include
from .views import UserFeedDetailView, UserFeedSaveView, FeedOfUserView, FeedCommentsInfoView
from .views import FeedSubscribeView, UserFeedSubscriberListView, FeedUnsubscribeView, UserFeedCommentView, FeedAddNewView
from feed.views import FeedRemoveView, FeedCommentAddView
from .views import ThrowError


urlpatterns = [

    path('detail/<int:pk>', UserFeedDetailView.as_view(), name='feed-detail'),
    path('user/<int:pk>', FeedOfUserView.as_view(), name='feed-of-user'),
    path('save/', UserFeedSaveView.as_view(), name='feed-save'),
    path('subscribe/<int:id>', FeedSubscribeView.as_view(), name='feed-subscribe'),
    path('unsubscribe/<int:id>', FeedUnsubscribeView.as_view(), name='feed-unsubscribe'),
    path('subscribers/', UserFeedSubscriberListView.as_view(), name='feed-subscriber-list'),
    # path('add/comment', UserFeedCommentView.as_view(), name='feed-add-comment-list'),
    path('add/new', FeedAddNewView.as_view(), name='feed-add-new-list'),
    path('remove/<int:post_id>', FeedRemoveView.as_view(), name='feed-remove-post'),

    path('add/comment', FeedCommentAddView.as_view(), name='feed-remove-post'),
    path('get-comments/<int:id>', FeedCommentsInfoView.as_view(), name='get-feed-comments'),

    path('error/', ThrowError.as_view())

]
