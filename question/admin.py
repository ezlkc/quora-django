from django.contrib import admin
from .models import Topic, Question, Answer, Follow, Comment


admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Follow)
admin.site.register(Comment)