from django.contrib import admin

# Register your models here.
from .models import Problem, Topic

class ProblemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'problem_text', 'topic', 'position']}),
        ('Answer', {'fields': ['wiki_answer'], 'classes': ['collapse']}),
        ('Date', {'fields': ['pub_date'], 'classes': ['collapse']})
    ]

    list_display = ('title', 'pub_date', 'was_published_recently')

class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'screenname']})
    ]

admin.site.register(Topic, TopicAdmin)

admin.site.register(Problem, ProblemAdmin)

# fields = ['pub_date', 'question_text', 'topic', 'position', 'wiki_answer']