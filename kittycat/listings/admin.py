from django.contrib import admin
from .models import Cat, UserProfile, AdoptionRequest, ProfileSettings, SearchHistory

# Register the Cat model in the Django admin
@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('cat_id', 'name', 'age', 'breed', 'castrated')

# Register the UserProfile model in the Django admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'contact_info')

# Register the AdoptionRequest model in the Django admin
@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'cat', 'request_date', 'status')
    list_filter = ('status',)

# Register the ProfileSettings model in the Django admin
@admin.register(ProfileSettings)
class ProfileSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_preferences', 'privacy_settings')

# Register the SearchHistory model in the Django admin
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'cat', 'date_added')
    list_filter = ('user', 'cat')
