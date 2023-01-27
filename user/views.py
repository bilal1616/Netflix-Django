from django.shortcuts import render, redirect
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_str, force_bytes
from django.http import HttpResponse
# Create your views here.
def userLogin(request):
    if request.method == 'POST':
        kullanici = request.POST['kullaniciadi']
        sifre = request.POST['sifre']

        user = authenticate(request, username = kullanici, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız.')
            return redirect('profiles')
        else:
            messages.warning(request, 'Kullanıcı adı veya şifre hatalı.')
            return redirect('login')

    return render(request, 'login.html')
def userRegister(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        tel = request.POST['tel']
        tc = request.POST['tc']
        resim = request.FILES['resim']
        tarih = request.POST['date']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.warning(request, 'Bu kullanıcı adı zaten kullanılıyor.')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.warning(request, 'Bu e-posta adresi zaten kullanılıyor.')
                return redirect('register')
            elif User.objects.filter(username__icontains = password1):
                messages.warning(request, 'Şifre ile kullanıcı adı çok benzer.')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, email = email, password = password1)
                Profil.objects.create(
                    user = user,
                    name = username,
                    email = email,
                    tel = tel,
                    tc = tc,
                    image = resim,
                    date = tarih,
                )
                
                subject = 'Neos Netflix'
                message = 'Bu netflix projesini 12 haziran grubuyla beraber yaptık.'
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                current_site = get_current_site(request)
                mail_subject = 'Linke tıklayarak mailinizi doğrulayın.'
                message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                to_email = user.email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                user.is_active = False
                user.save()
                messages.success(request, 'Mailinzi doğrulayın.')
                return redirect('login')
    return render(request, 'register.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        messages.success(request, 'Mailiniz başarıyla doğrulandı.')
        return redirect('profil')
    else:
        return HttpResponse('Activation link is invalid!')
def userLogout(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('login')

def userProfil(request):
    profile = request.user.profil
    context = {
        'profile': profile,
    }
    return render(request, 'hesap.html', context)

def userDelete(request):
    userProfil = request.user.profil
    user = request.user
    userProfil.delete()
    user.delete()
    messages.success(request, 'Kullanıcı başarıyla silindi.')
    return redirect('login')

def profilCreate(request):
    form = ProfilForm()
    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit = False)
            form.owner = request.user.profil
            form.save()
            messages.success(request, 'Profil başarıyla oluşturuldu.')
            return redirect('profiles')
    context = {
        'form': form,
    }
    return render(request, 'profil-create.html', context)
