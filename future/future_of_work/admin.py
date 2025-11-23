from django.contrib import admin
from .models import Badge, UserProfile, Notification, Lesson, LessonProgress, Future_Of_Work

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pod', 'goal', 'level', 'xp')
    list_filter = ('pod', 'goal', 'level')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('badges',)  # makes many-to-many badges easier to manage


admin.site.register(Badge)
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(Lesson)
admin.site.register(LessonProgress)
admin.site.register(Future_Of_Work)