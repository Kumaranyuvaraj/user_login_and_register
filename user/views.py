
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .models import CustomUser    
from .forms import CodeForm
from .utils import send_sms



@login_required
def home_view(request):
    return render(request,'user/main.html',{})
##################################################################
####################index#######################################
def index(request):
    return render(request, 'user/index.html',{'title':'index'})

########################################################################
########### register here #####################################

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
            username = request.POST.get('username')
            #########################mail####################################
            htmly = get_template('user/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'hello', 'from@example.com', 'to@emaple.com'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("error in sending mail")
            ##################################################################
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form,'title':'reqister here'})

###################################################################################
################login forms###################################################

def Login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username =request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            request.session['pk']=user.pk
            return redirect('verify-view')
 
        else:
            messages.info(request, f'account does not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form,'title':'log in'})
    

def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = CustomUser.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.username}:{user.code}"
        
        if not request.POST:
            print(code_user)
            send_sms(code_user,user.phone_number)
        
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()
                login(request,user)
                return redirect('home-view')
            else:
                return redirect('login-view')
    
    return render(request,'user/verify.html',{'form':form})

