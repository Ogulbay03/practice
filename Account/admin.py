from django.contrib import admin
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from Account.models import Answer, Question, Test, Response, QuizTakers


#
# class TestAdmin(admin.ModelAdmin):
# 	list_display = ['id', 'title']
# 	search_fields = ['id', 'title']
# 	list_display_links = list_display
#
#
# class AnswerAdmin(admin.ModelAdmin):
# 	list_display = ['id', 'text', 'correct']
# 	search_fields = ['id', 'text']
# 	list_display_links = list_display
#
#
# admin.site.register(Test, TestAdmin)
# admin.site.register(Question, TestAdmin)
# admin.site.register(Answer, AnswerAdmin)


class AnswerInline(NestedTabularInline):
	model = Answer
	extra = 4
	max_num = 4


class QuestionInline(NestedTabularInline):
	model = Question
	inlines = [AnswerInline, ]
	extra = 19


class QuizAdmin(NestedModelAdmin):
	inlines = [QuestionInline, ]


class ResponseInline(admin.TabularInline):
	model = Response


class QuizTakersAdmin(admin.ModelAdmin):
	inlines = [ResponseInline, ]


admin.site.register(Test, QuizAdmin)
admin.site.register(QuizTakers, QuizTakersAdmin)
admin.site.register(Response)
