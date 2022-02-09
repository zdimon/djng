from django.contrib import admin
from image_cropping import ImageCroppingMixin
from account.admin import superadmin_site

# Register your models here.
from feed.models import UserFeed, UserFeedComment
from usermedia.models import UserMedia
from feed.models import UserFeedSubscription
# Register your models here.

class UserMediaInline(admin.StackedInline):
    model = UserMedia
    readonly_fields = ['user', 'type_media']



@admin.register(UserFeed)
class UserFeedAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ['title', 'user', 'is_approved', 'is_stories', 'city']
    list_filter = ['user']
    inlines = [ UserMediaInline , ]

# admin.site.register(UserFeed, UserFeedAdmin)

@admin.register(UserFeedComment)
class UserFeedCommentAdmin(admin.ModelAdmin):
    list_display = ['feed', 'user', 'text']
    
# admin.site.register(UserFeedComment, UserFeedCommentAdmin)

@admin.register(UserFeedSubscription)
class UserFeedSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user_subscriber', 'user_destination']