from django.contrib import admin

from .models import Language, Topic, SituationalVideo, Exercise, LanguageTopic, LanguageSubtopic, ExerciseQuestion, Resource, ResourceItem, ResourceItemPicture, Dialect

admin.site.register(Language)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_filter = ('level',)

@admin.register(LanguageTopic)
class LanguageTopicAdmin(admin.ModelAdmin):
	list_filter = ('language',)

@admin.register(ExerciseQuestion)
class ExerciseQuestionAdmin(admin.ModelAdmin):
	list_filter = ('exercise',)

@admin.register(Dialect)
class DialectAdmin(admin.ModelAdmin):
	list_filter = ('language_id',)

@admin.register(LanguageSubtopic)
class LanguageSubtopicAdmin(admin.ModelAdmin):
	list_filter = ('language_topic',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
	list_filter = ('dialect_id',)

admin.site.register(Exercise)
admin.site.register(SituationalVideo)

admin.site.register(ResourceItem)
admin.site.register(ResourceItemPicture)