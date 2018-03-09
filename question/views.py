import os

from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from .forms import AskForm, AnswerForm, CommentForm
from .models import Topic, Question, Answer, Follow, Comment
from account.models import Profile
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Q

def index_dim(request):
    return index(request, 1)


def index(request, page):
    if not request.user.is_authenticated:
        return redirect('account:signup')
    profile = Profile.objects.get(user=request.user)
    following = Follow.objects.filter(profile=profile).all()
    followed_topics = []
    for topic in following:
        followed_topics.append(topic.topic)
    queries = [Q(topic=topic) for topic in followed_topics]
    if queries:
        query = queries.pop()
        for item in queries:
            query |= item
        questions = Question.objects.filter(query).order_by('-created_at').all()
    else:
        questions = []
    paginator = Paginator(questions, 10)
    questions = paginator.page(page)
    print(questions)
    return render(request, "question/index.html", {
        "questions": questions, "following": followed_topics
    })

class AskView(View):
    form_class = AskForm

    def get(self, request):
        form = self.form_class(None)
        topics = Topic.objects.all()
        return render(request, "question/ask.html",{"form": form, "topics": topics})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_question = Question()
            new_question.content = form.cleaned_data['content']
            picture = request.FILES.get('picture')
            if picture:
                fs = FileSystemStorage()
                new_question.picture = fs.save('questions/question.jpg', picture)
            new_question.profile = Profile.objects.get(user=request.user)
            new_question.topic = Topic.objects.get(id=int(request.POST.get('topic')))
            new_question.save()
            return redirect("/")
        else:
            topics = Topic.objects.all()
            return render(request, "question/ask.html", {"form": form, "topics": topics})

class QuestionEditView(UpdateView):
    form_class = AskForm

    def get(self, request,id):
        if not request.user.is_authenticated:
            return redirect('/')
        question = get_object_or_404(Question,id=id)
        form = self.form_class(None, content=question.content)

        return render(request, "question/edit_question.html", {"form": form})

    def post(self, request,id):

        form = self.form_class(request.POST)
        if form.is_valid():
            question = get_object_or_404(Question,id=id)
            question.content = form.cleaned_data['content']

            question.profile = Profile.objects.get(user=request.user)
            question.save()
            return redirect('question:question', id=id)
        else:
            return render(request, "question/edit_question.html", { "form": form })
class AnswerEditView(UpdateView):
    form_class = AnswerForm

    def get(self, request,id):
        if not request.user.is_authenticated:
            return redirect('/')
        answer = get_object_or_404(Answer,id=id)
        form = self.form_class(None, content=answer.content)

        return render(request, "question/edit_answer.html", {"form": form})

    def post(self, request,id):

        form = self.form_class(request.POST)
        if form.is_valid():
            answer = get_object_or_404(Answer, id=id)
            answer.content = form.cleaned_data['content']

            answer.profile = Profile.objects.get(user=request.user)
            answer.save()
            return redirect('question:answer1', id=id)

        else:
            return render(request, "question/edit_answer.html", { "form": form })
class CommentEditView(UpdateView):
    form_class = CommentForm

    def get(self, request,id):
        if not request.user.is_authenticated:
            return redirect('/')
        comment = get_object_or_404(Comment,id=id)
        form = self.form_class(None, content=comment.content)

        return render(request, "question/edit_comment.html", {"form": form})

    def post(self, request,id):

        form = self.form_class(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=id)
            comment.content = form.cleaned_data['content']

            comment.profile = Profile.objects.get(user=request.user)
            comment.save()
            return redirect('/')

        else:
            return render(request, "question/edit_comment.html", { "form": form })


def topics_view(request, page):
    topics = Topic.objects.all()
    paginator = Paginator(topics, 18)
    topics = paginator.page(page)
    return render(request, "question/topics.html", {
        "topics": topics
    })

def question_view(request, id):
    question = get_object_or_404(Question, id=id)
    question.views += 1
    question.save()
    answers = Answer.objects.filter(question=question)
    return render(request, "question/question.html", {
        "question": question, "answers": answers
    })
def q_like_view(request, id):
    question = get_object_or_404(Question, id=id)
    question.q_like += 1
    question.save()
    answers = Answer.objects.filter(question=question)
    return render(request, "question/question.html", {
        "question": question, "answers": answers
    })

def q_dislike_view(request, id):
    question = get_object_or_404(Question, id=id)
    question.q_dislike += 1
    question.save()
    answers = Answer.objects.filter(question=question)
    return render(request, "question/question.html", {
        "question": question, "answers": answers
    })


def answer_view(request, id):
    answer = get_object_or_404(Answer, id=id)
    comments = Comment.objects.filter(answer=answer)
    return render(request, "question/answer-comment.html", {
        "answer": answer, "comments": comments
    })

def answer2_view(request, id):
    answer = get_object_or_404(Answer, id=id)
    comment2s = Comment.objects.filter(answer=answer)
    return render(request, "question/answer-comment.html", {
        "answer": answer, "comment2s": comment2s
    })
class AnswerView(View):
    form_class = AnswerForm

    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect('/')
        question = Question.objects.get(id=id)
        question.views += 1
        question.save()
        form = self.form_class(None)
        return render(request, "question/answer.html", {"question": question, "form": form})

    def post(self, request, id):
        question = Question.objects.get(id=id)

        form = self.form_class(request.POST)
        if form.is_valid():
            answer = Answer(profile=Profile.objects.get(user=request.user))
            answer.content = form.cleaned_data['content']
            source_file = request.FILES.get('picture')
            if source_file:
                fs = FileSystemStorage()
                answer.picture = fs.save('answers/answer.jpg', source_file)
            answer.question = question
            answer.save()
            return redirect('question:question', id=id)
        else:
            return render(request, "question/answer.html", {
                "form": form, "question": question
            })




def a_like_view(request, id):
        answer = get_object_or_404(Answer, id=id)
        answer.a_like += 1
        answer.save()
        comments = Comment.objects.filter(answer=answer)
        return render(request, "question/answer-comment.html", {
            "answer": answer, "comments": comments
        })


def a_dislike_view(request, id):
    answer = get_object_or_404(Answer, id=id)
    answer.a_dislike += 1
    answer.save()
    comments = Comment.objects.filter(answer=answer)
    return render(request, "question/answer-comment.html", {
        "answer": answer, "comments": comments
    })


class CommentView(View):
    form_class = CommentForm

    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect('/')

        answer = get_object_or_404(Answer, id= id)
        form = self.form_class(None)
        return render(request, "question/comment.html", {"answer": answer, "form": form})

    def post(self, request, id):
        answer = get_object_or_404(Answer, id=id)

        form = self.form_class(request.POST)
        if form.is_valid():
            comment = Comment(profile=Profile.objects.get(user=request.user))
            comment.content = form.cleaned_data['content']
            source_file = request.FILES.get('picture')
            if source_file:
                fs = FileSystemStorage()
                comment.picture = fs.save('answers/answer.jpg', source_file)
            comment.answer = answer
            comment.save()
            return redirect('question:answer1', id=id)
        else:
            return render(request, "question/comment.html", {
                "form": form, "answer": answer
            })

class Comment2View(View):
    form_class = CommentForm

    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect('/')

        comment = get_object_or_404(Comment, id= id)
        form = self.form_class(None)
        return render(request, "question/comment.html", {"comment": comment, "form": form})

    def post(self, request, id):
        comment = get_object_or_404(Comment, id=id)

        form = self.form_class(request.POST)
        if form.is_valid():
            comment2 = Comment(profile=Profile.objects.get(user=request.user))
            comment2.content = form.cleaned_data['content']
            source_file = request.FILES.get('picture')
            if source_file:
                fs = FileSystemStorage()
                comment2.picture = fs.save('answers/answer.jpg', source_file)
            comment2.comment = comment
            comment2.save()
            return redirect('question:answer1', id=id)
        else:
            return render(request, "question/comment.html", {
                "form": form, "comment": comment
            })


def topic_no_page(request, id):
    return topic_view(request, id, 1)

def topic_view(request, id, page):
    topic = Topic.objects.get(id=id)
    questions = Question.objects.filter(topic=topic).order_by('-created_at').all()
    profile = Profile.objects.get(user=request.user)
    if Follow.objects.filter(profile=profile, topic=topic).exists():
        following = "Unfollow"
    else:
        following = "Follow"
    count = questions.count()
    paginator = Paginator(questions, 10)
    questions = paginator.page(page)
    return render(request, "question/topic.html", {
        "topic": topic, "questions": questions, "following": following,
        "count": count
    })


def follow_view(request):
    id = request.POST.get('id')
    topic = Topic.objects.get(id=int(id))
    profile = Profile.objects.get(user=request.user)
    if Follow.objects.filter(profile=profile, topic=topic).exists():
        Follow.objects.get(profile=profile, topic=topic).delete()
        return HttpResponse("Follow")
    else:
        follow = Follow(topic=topic, profile=profile)
        follow.save()
        return HttpResponse("Unfollow")


def question_delete_view(request,id,page):
    question = get_object_or_404(Question, id=id)
    question.delete()
    if not request.user.is_authenticated:
        return redirect('account:signup')
    profile = Profile.objects.get(user=request.user)
    following = Follow.objects.filter(profile=profile).all()
    followed_topics = []
    for topic in following:
        followed_topics.append(topic.topic)
    queries = [Q(topic=topic) for topic in followed_topics]
    if queries:
        query = queries.pop()
        for item in queries:
            query |= item
        questions = Question.objects.filter(query).order_by('-created_at').all()
    else:
        questions = []
    paginator = Paginator(questions, 10)
    questions = paginator.page(page)
    print(questions)
    return render(request, "question/index.html", {
        "questions": questions, "following": followed_topics
    })

def answer_delete_view(request,id,page):
    answer = get_object_or_404(Answer, id=id)
    answer.delete()
    if not request.user.is_authenticated:
        return redirect('account:signup')
    profile = Profile.objects.get(user=request.user)
    following = Follow.objects.filter(profile=profile).all()
    followed_topics = []
    for topic in following:
        followed_topics.append(topic.topic)
    queries = [Q(topic=topic) for topic in followed_topics]
    if queries:
        query = queries.pop()
        for item in queries:
            query |= item
        questions = Question.objects.filter(query).order_by('-created_at').all()
    else:
        questions = []
    paginator = Paginator(questions, 10)
    questions = paginator.page(page)
    print(questions)
    return render(request, "question/index.html", {
        "questions": questions, "following": followed_topics
    })
def comment_delete_view(request,id,page):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    if not request.user.is_authenticated:
        return redirect('account:signup')
    profile = Profile.objects.get(user=request.user)
    following = Follow.objects.filter(profile=profile).all()
    followed_topics = []
    for topic in following:
        followed_topics.append(topic.topic)
    queries = [Q(topic=topic) for topic in followed_topics]
    if queries:
        query = queries.pop()
        for item in queries:
            query |= item
        questions = Question.objects.filter(query).order_by('-created_at').all()
    else:
        questions = []
    paginator = Paginator(questions, 10)
    questions = paginator.page(page)
    print(questions)
    return render(request, "question/index.html", {
        "questions": questions, "following": followed_topics
    })