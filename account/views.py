from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SignUpForm, LoginForm, ProfileForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from question.models import Question, Answer, Comment
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate, logout
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from PIL import Image
import os


class SignUpView(View):
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, "account/signup.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                form.add_error("confirm_password", "Parolalar uyuşmuyor")
                return render(request, "account/signup.html", {"form": form})
            user.set_password(form.cleaned_data["password"])
            user.is_active = True
            user.save()
            '''
             current_site = get_current_site(request)
            message = render_to_string("account/activate_email.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            mail_subject = "Quora hesabınızı etkinleştirin"
            to_email = form.cleaned_data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            #email.send()
            '''

            profile = Profile(user=user)
            profile.save()

            return redirect('account:login')
            #return HttpResponse("Lütfen hesabınızı e-postayla etkinleştirin")
        else:
            return render(request, "account/signup.html", {"form": form})


class LoginView(View):
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, "account/login.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    form.add_error("username", "Lütfen parolanızı doğrulayınız")
                    return render(request, "account/login.html", {"form": form})
            else:
                form.add_error("password", "Geçersiz kullanıcı adı veya parola")
                return render(request, "account/login.html", {"form": form})
        else:
            return render(request, "account/login.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('E-posta onayınız için teşekkür ederiz. Artık hesabınıza giriş yapabilirsiniz.')
    else:
        return HttpResponse('Etkinleştirme bağlantısı geçersiz!')


def logout_view(request):
    logout(request)
    return redirect("/")


def profile_view_2(request, username):
    return profile_view(request, username, 1)


def profile_view(request, username, page):
    profile = Profile.objects.get(user=User.objects.get(username=username))
    questions = Question.objects.filter(profile=profile).order_by('-created_at').all()
    paginator = Paginator(questions, 10)
    questions = paginator.page(page)
    return render(request, "account/profile.html", {
        "profile": profile, "questions": questions
    })


def answers_view_2(request, username):
    return answers_view(request, username, 1)


def answers_view(request, username, page):
    profile = Profile.objects.get(user=User.objects.get(username=username))
    answers = Answer.objects.filter(profile=profile).order_by('-created_at').all()
    paginator = Paginator(answers, 10)
    answers = paginator.page(page)
    return render(request, "account/answers.html", {
        "profile": profile, "answers": answers
    })

def comments_view_2(request, username):
    return comments_view(request, username, 1)


def comments_view(request, username, page):
    profile = Profile.objects.get(user=User.objects.get(username=username))
    commnets = Comment.objects.filter(profile=profile).order_by('-created_at').all()
    paginator = Paginator(commnets, 10)
    commnets = paginator.page(page)
    return render(request, "account/commnets.html", {
        "profile": profile, "commnets": commnets
    })



class EditView(View):
    form_class = ProfileForm

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = self.form_class(None,
                               profession=profile.profession,
                               education=profile.education,
                               employment=profile.employment
                            )
        return render(request, "account/edit.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.education = form.cleaned_data['education']
            profile.profession = form.cleaned_data['profession']
            profile.employment = form.cleaned_data['employment']
            avatar = request.FILES.get('avatar')
            if avatar is not None:
                fs = FileSystemStorage()
                source_file = fs.save('cache/avatar.jpg', avatar)
                img = Image.open('media/' + source_file)
                width, height = img.size
                if width >= height:
                    upper_x = int((width / 2) - (height / 2))
                    upper_y = 0
                    lower_x = int((width / 2) + (height / 2))
                    lower_y = height
                else:
                    upper_x = 0
                    upper_y = int((height / 2) - (width / 2))
                    lower_x = width
                    lower_y = int((height / 2) + (width / 2))
                box = (upper_x, upper_y, lower_x, lower_y)
                img = img.crop(box)
                img.save('media/'+source_file)
                profile.avatar = fs.save('avatar/avatar.jpg', open('media/'+source_file, 'rb'))
                os.remove('media/'+source_file)
            profile.save()
            return redirect("account:profile", username=request.user.username)
        else:
            return render(request, "account/edit.html", {"form": form})

