from django.contrib import admin
from socializer.models import Comment
from socializer.models import Recommendation
from socializer.models import Flag
from socializer.models import Nudge


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'timestamp',)


class RecommendationAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'timestamp',)


class FlagAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'timestamp',)


class NudgeAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'timestamp',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Flag, FlagAdmin)
admin.site.register(Nudge, NudgeAdmin)
