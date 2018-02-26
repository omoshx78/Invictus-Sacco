from django.shortcuts import render
from django.shortcuts import redirect
from .models import Contact
from .models import Member_reg
from .models import reg_members
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Avg, Max, Min, Sum
from .forms import DocumentForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import auth

# Create your views here.
def index(request):
    return render(request, 'invictus/home.html')

def about(request):
    return render(request, 'invictus/about.html')

def loan_dev(request):
    return render(request, 'invictus/loan_dev.html')

def loan_biz(request):
    return render(request, 'invictus/loan_biz.html')

def salary_adv(request):
    return render(request, 'invictus/salary_adv.html')

def biz_fix(request):
    return render(request, 'invictus/biz_fix.html')

def timiza(request):
    return render(request, 'invictus/timiza.html')

def jipange(request):
    return render(request, 'invictus/jipange.html')


def open_acc(request):
    return render(request, 'invictus/open_acc.html')


def statuary(request):
    return render(request, 'invictus/statuary.html')



def investment(request):
    return render(request, 'invictus/investment.html')



def sacco_dep(request):
    return render(request, 'invictus/sacco_dep.html')

@csrf_exempt
def contact(request):
        if request.method == 'POST':
            if request.POST.get('name') and request.POST.get('email') and request.POST.get('phone')  and request.POST.get('message'):
                post=Contact()
                post.name= request.POST.get('name')
                post.email= request.POST.get('email')
                post.phone= request.POST.get('phone')
                post.message= request.POST.get('message')
                post.save()
                
                return render(request, 'invictus/contact.html')

        else:
                return render(request, 'invictus/contact.html')


@csrf_exempt
def member_regi(request):
        if request.method == 'POST':
             if request.POST.get('fullname') and request.POST.get('dob') and request.POST.get('idno') and request.POST.get('mobile') and request.POST.get('email') and request.POST.get('employer') and request.POST.get('address') and request.POST.get('county') and request.POST.get('religion') and request.POST.get('month_cont') and request.POST.get('kin_fullname') and request.POST.get('kin_ID') and request.POST.get('kin_phone') and request.POST.get('kin_relation') and request.POST.get('transaction_reference'):       	
                post=reg_members()
                post.fullname= request.POST.get('fullname')
                post.dob= request.POST.get('dob')
                post.idno= request.POST.get('idno')
                post.mobile= request.POST.get('mobile')
                post.email= request.POST.get('email')
                post.employer= request.POST.get('employer')
                post.address = request.POST.get('address')
                post.county = request.POST.get('county')
                post.religion = request.POST.get('religion')
                post.month_cont = request.POST.get('month_cont')
                post.kin_id = request.POST.get('kin_ID')
                post.kin_phone = request.POST.get('kin_phone')
                post.kin_relation = request.POST.get('kin_relation')
                post.kin_fullname = request.POST.get('kin_fullname')
                post.datestamp = datetime.datetime.now()
                post.transaction_reference = request.POST.get('transaction_reference')
                maxid = reg_members.objects.order_by('-id')[0] 
                p = maxid.id
                post.member_no = p + 10000
                

                if post.save():
                    return render(request, 'invictus/member_reg.html')               
                   
                else:
                	request.session['post.fullname'] = post.fullname
                	request.session['post.idno'] = post.idno
                	request.session['post.member_no'] = post.member_no
                	request.session['post.email'] = post.email
                	return redirect('upload')            

               


        else:
                return render(request, 'invictus/member_reg.html')


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            if form.save():
             member_no = request.session['post.member_no']
             request.session['post.member_no'] = member_no                  
             return redirect('signup')

               
    else:
        form = DocumentForm(initial = {'idno':request.session['post.idno']})
        fullname = request.session['post.fullname']
    return render(request, 'invictus/upload.html', {'form': form , 'names' : fullname })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Invictus account.'
            message = render_to_string('invictus/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm(initial = {'username':request.session['post.member_no']})
        fname = request.session['post.fullname']
        member_n = request.session['post.member_no']
    return render(request, 'invictus/signup.html', {'form': form , 'names' : fname , 'member_n' : member_n})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('index')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@csrf_exempt
def login_view(request):
	if request.method == 'POST':
	    username = request.POST.get('username', '')
	    password = request.POST.get('password', '')
	    user = auth.authenticate(username=username, password=password)
	    if user is not None and user.is_active:
	        # Correct password, and the user is marked "active"
	        auth.login(request, user)
	        # Redirect to a success page.
	        return redirect("/")
	    else:
	        # Show an error page
	        return render(request, 'invictus/login.html', {'error': 'Your username or password is invalid.' })
	else:
		return render(request, 'invictus/login.html')



def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return redirect("/")

def member_portal(request):
    return render(request, 'invictus/member_portal.html')