from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import CustomUser,Questions,Scores,Leaderboard
from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm,loginForm,questionForm,ChangePassForm
import json
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import random
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.views.decorators.http import require_http_methods
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login, logout
from quizapp.authenticate import Auth
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def start(request):
    return redirect('home/')

def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect('home/')

def home(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_admin:
            return render(request, 'home/admin-home.html', {'user': user})
        else:
            return redirect('profile')
    else:
        return render(request, 'home/web-home.html')

def play_quiz(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_admin == False:
            return render(request, 'quizzes/play-quiz.html', {'user': user})
    else:
        return render(request, 'home/web-home.html')

def category_ranks(category,user):
    scores = list(Scores.objects.filter(category=category).order_by('-score','user_name'))
    rank = None
    for index,entry in enumerate(scores):
        if entry.user_name == user:
            rank = index+1
            break
    if rank is None:
        rank = 'Not Ranked'

    return rank

@login_required
def profile(request):
    user = request.user
    if user.is_admin:
        return render(request, 'home/admin-home.html', {'user': user})
    else:
        overall_scores = list(Leaderboard.objects.all().order_by('-score','user_name'))
        overall_rank = None
        for index, entry in enumerate(overall_scores):
            if entry.user_name == user:
                overall_rank = index + 1
                break
        if overall_rank is None:
            overall_rank = 'Not Ranked'

        sports_rank = category_ranks(category="SPORTS",user=user)
        geography_rank = category_ranks(category="GEOGRAPHY",user=user)
        history_rank = category_ranks(category="HISTROY",user=user)
        movies_rank = category_ranks(category="MOVIES",user=user)
        music_rank = category_ranks(category="MUSIC",user=user)
        literature_rank = category_ranks(category="LITERATURE",user=user)
        context={
            'user': user,
            'sports_rank':sports_rank,
            'geography_rank':geography_rank,
            'history_rank':history_rank,
            'movies_rank':movies_rank,
            'music_rank':music_rank,
            'literature_rank':literature_rank,
            'overall_rank':overall_rank
        }
        return render(request, 'home/user-profile.html', context)

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    else:
        if request.method == "POST":
            form = loginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['user_name']
                password = form.cleaned_data['password']
                user = Auth.authenticate(request, username=username, password=password)
                
                if user is not None:
                    backend_path = settings.AUTHENTICATION_BACKENDS[1]
                    user.backend = backend_path
                    login(request, user)
                    return redirect("profile")
                else:
                    messages.warning(request, 'Invalid username or password.')
        else:
            form = loginForm()
        return render(request, 'login/login.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['user_name']
            upass = form.cleaned_data['password']
            cpass = form.cleaned_data['confirm_password']
            email_address = form.cleaned_data['email']


            try:
                print(1)
                already_user = CustomUser.objects.get(user_name=uname)
                messages.error(request, "Username Already Taken.")
                return render(request, 'login/signup.html', {'form': form})
            except CustomUser.DoesNotExist:
                pass


            try:
                print(2)
                
                already_email = CustomUser.objects.get(email=email_address)
                print(already_email)
                messages.error(request, "Email already in use.")
                print("Email already in use.")
                return render(request, 'login/signup.html', {'form': form})
            except (ObjectDoesNotExist, ValidationError):
                pass


            try:
                validate_email(email_address)
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
                return render(request, 'login/signup.html', {'form': form})
            

            try:
                validate_password(upass)
                if upass != cpass:
                    print('password verificatio failed')
                    messages.error(request, "Your password and confirm password field does not match.")
                    return render(request, 'login/signup.html', {'form': form})
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
                return render(request, 'login/signup.html', {'form': form})
            
            user = form.save(commit=False)
            user.is_active = False
            user.password = make_password(upass)
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('login/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return HttpResponse('Please confirm your email address to complete the registration.')
             
                    
                
            
    else:
        form = SignupForm()

    return render(request, 'login/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = int(force_str(urlsafe_base64_decode(uidb64)))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login_url = reverse('login')
        return HttpResponse(f'Thank you for your email confirmation. Now you can <a href="{login_url}" style="text-decoration: none;">Login</a> your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def launch_quiz(request):
    if request.method == "POST":
        quiz_type = request.POST.get('quiz').upper()
        questions = list(Questions.objects.filter(category=quiz_type,published=True))
        questions = random.sample(questions, 10)
        questions_serialized = json.dumps([{
            "question": q.question,
            "opt_a": q.opt_a,
            "opt_b": q.opt_b,
            "opt_c": q.opt_c,
            "opt_d": q.opt_d,
            "answer": q.answer,
            "category": q.category
        } for q in questions])

        context = {
            "quiz": quiz_type,
            "questions": questions_serialized,
        }
        return render(request, 'quizzes/quiz.html', context)

    return render(request, 'quizzes/quiz.html')

def update_leaderboard(user_id):
    user = CustomUser.objects.get(pk=user_id)
    scores = Scores.objects.filter(user_name=user_id)
    total_score=0
    i=0
    for score in scores:
        total_score += score.score
        i+=1
    avg_score=total_score/i
    try:
        curr_user = Leaderboard.objects.get(user_name=user)
        curr_user.score=avg_score
        curr_user.save()

    except Leaderboard.DoesNotExist:
        curr_user = Leaderboard(user_name=user,score=avg_score)
        curr_user.save()
        
    

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def submit_quiz(request):
    if request.method == "POST":
        curr_score = int(request.POST.get('score'))
        quiz_category = request.POST.get('category')

        if request.user.is_authenticated:
            user = request.user
            try:
                print('trying....')
                
                print(user)
                old_score = Scores.objects.get(category=quiz_category,user_name=user.id)
                new_score= math.ceil((old_score.score + curr_score)/2)
                old_score.score = new_score
                old_score.save()
                
            except Scores.DoesNotExist:
                score = Scores(user_name=user, score=curr_score, category=quiz_category)
                score.save()

            update_leaderboard(user.id)
            return JsonResponse({'status': 1})  
            
        else:
            return JsonResponse({'status': 0, 'error': 'User not authenticated'})

def rankings(request):
    if request.method == "POST":
        user = request.user
        quiz_type = request.POST.get('quiz').upper()
        scores = Scores.objects.filter(category=quiz_type).order_by('-score','user_name')
        context ={
            'scores':scores,
            'category':quiz_type,
            'user_id': user.id,
        }
        return render(request,'quizzes/rankings.html',context)

def leaderboard(request):
    scores = Leaderboard.objects.all().order_by('-score','user_name')
    
    if request.user.is_authenticated:
        user = request.user
        
        context = {
            'scores':scores,
            'user_id':user.id,
            'nav':1,
        }

    else:
        context={
            'scores':scores,
            'nav':2,
        }
    return render(request,'quizzes/leaderboard.html',context)

def publish(request):
    if request.method == "POST":
        qid = request.POST.get('questionId')
        question = Questions.objects.get(pk=qid)
        question.published = True
        question.save()
        return JsonResponse({'status':1})

@login_required
def add_questions(request):
    if request.method == "POST":
        form = questionForm(request.POST)
        if form.is_valid():
            
            try :
                question = request.POST.get('question')
                que = Questions.objects.get(question=question)
                messages.warning(request,'Question already added.')
            except Questions.DoesNotExist:
                form.save()
                messages.success(request, 'Question submitted successfully.')
                form = questionForm()
                return render(request, 'home/admin-questions.html', {'form': form})

    else:
        form = questionForm()

    return render(request, 'home/admin-questions.html', {'form': form})

def questions_list(request):
    if request.method == "POST":
        status = request.POST.get('status').lower()
        if status == 'published':
            status = 'Published'
            questions = Questions.objects.filter(published=True)
            
            
        elif status == 'not_published':
            status = 'Not Published'
            questions = Questions.objects.filter(published=False)
            
        else :
            return redirect('questions-list')
        

    else:
        questions = Questions.objects.all()
        status = 'All'

    page_num = request.GET.get('page', 1)
    paginator = Paginator(questions, 15)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context={
        'questions':page_obj,
        'status':status
    }
    return render(request,'home/questions-list.html',context)

def modify_questions(request):
    if request.method =="POST":
        qid = request.POST.get('questionId')
        que = request.POST.get('question')
        optA = request.POST.get('opt_a')
        optB = request.POST.get('opt_b')
        optC = request.POST.get('opt_c')
        optD = request.POST.get('opt_d')
        category = request.POST.get('category').upper()
        answer = request.POST.get('answer').upper()
        try: 
            question = Questions.objects.get(pk=qid)
            question.question = que
            question.opt_a = optA
            question.opt_b = optB
            question.opt_c = optC
            question.opt_d = optD
            question.answer = answer
            question.category = category
            question.save()
            print('question updated')
            return JsonResponse({'status':1})
        except Questions.DoesNotExist:
            return JsonResponse({'status':0})
        


def forget_pass(request):
    if request.method == 'POST':
        email = request.POST.get('user')
        user = CustomUser.objects.filter(email=email).first()
        if user is not None:
            otp = random.randint(100000,999999)
            user.otp = otp
            user.save()
            send_mail(
                "OTP for reseting your password ",
                f"Your OTP is {otp}",
                "khushdhameliya007@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return JsonResponse({'status':1})
        else :
            return JsonResponse({'status':0})
    else:
        return render(request,'login/forget-pass.html')

@csrf_protect
def confirm_otp(request):
    if request.method == "POST":
        otp =  request.POST.get('otp')
        uname = request.POST.get('user')
        user =  CustomUser.objects.get(email=uname)
        if str(user.otp) == otp:
            user.otp = None
            user.save()
            return JsonResponse({'status':1})
        else:
            return JsonResponse({'status':0})

@login_required
def change_pass(request):
    if request.user.is_authenticated:
        user = request.user
    else: 
        redirect('login')
    
    if request.method == 'POST':
        form = ChangePassForm(request.POST)
        
        
        if form.is_valid():
            curr_pass=form.cleaned_data['current_password']
            new_pass=form.cleaned_data['new_password']
            con_pass=form.cleaned_data['confirm_password']
            if check_password(curr_pass,user.password):
                if curr_pass == new_pass:
                    messages.warning(request,'Your new password is same as current password.')
                else:
                    try:
                        validate_password(new_pass)
                        if new_pass == con_pass:
                            user.password = make_password(new_pass)
                            user.save()
                            messages.success(request,'You password is changed successfully.')
                            return redirect('login')
                            
                        else :
                            messages.warning(request,'Your new password does not matches confirm password field.')
                            form=ChangePassForm()
                    except ValidationError as e:
                        for error in e:
                            messages.warning(request, error)

            else:
                messages.warning(request,'You have enterred incorrect current password.')
                form=ChangePassForm()
    else:
        form=ChangePassForm()
    context = {'form':form,'user':user}
    return render(request,'login/change-pass.html',context)


@csrf_protect
def new_pass(request):
    if request.method == 'POST':
        new_pass = request.POST.get('npass')
        
        uname = request.POST.get('user')
        user = CustomUser.objects.get(email=uname)
        try:
            validate_password(new_pass)
            
            user.password = make_password(new_pass)
            user.save()
            print("done")
            return JsonResponse({'status':1})
        
                
        except ValidationError as e:
            return JsonResponse({'status':0})
    else:
        return JsonResponse({'status':0})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# FLOW = flow_from_clientsecrets(
#     settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
#     scope='https://www.googleapis.com/auth/gmail.readonly',
#     redirect_uri='http://127.0.0.1:8000/oauth2callback',
#     prompt='consent')