from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UsernameForm, PasswordForm ,CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
# your_app_name/views.py
import os
# for encrypt
from .encryption_module import encryptor ,decryptor

# views.py
def encrypt(request):
    if request.method == 'POST':
        # Assuming you have a form with 'file', 'passw1', and 'passw2' fields for user input
        uploaded_file = request.FILES.get('file')
        passw1 = request.POST.get('passw1')
        passw2 = request.POST.get('passw2')

        # Validate passwords
        if passw1 != passw2:
            return HttpResponse("Passwords do not match.")

        if uploaded_file:
            # Save the uploaded file to a temporary location
            temp_file_path = "temp_file_to_encrypt"
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            # Encrypt the file
            original_name = uploaded_file.name
            encrypted_file_path = encryptor(temp_file_path, passw1)

            # Serve the encrypted file for download
            with open(encrypted_file_path, 'rb') as encrypted_file:
                response = HttpResponse(encrypted_file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename={"encrypted_"+original_name}'
                return response

        else:
            return HttpResponse("No file uploaded.")
    else:
        return render(request, 'encrypt.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'common/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username_form = UsernameForm(request.POST, prefix='username')
        password_form = PasswordForm(request, request.POST, prefix='password')

        if username_form.is_valid() and password_form.is_valid():
            username = username_form.cleaned_data.get('username')
            password = password_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        username_form = UsernameForm(prefix='username')
        password_form = PasswordForm(prefix='password')

    return render(request, 'common/login.html', {'username_form': username_form, 'password_form': password_form})

def logout_1(request):
    logout(request)
    return redirect('login')

# Create your views here.
def home(request):
    return render(request,'home.html')

# views.py
def decrypt(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        passw1 = request.POST.get('passw1')

        if uploaded_file:
            temp_file_path = "temp_file_to_decrypt"
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            try:
                decrypted_file_path = decryptor(temp_file_path, passw1)
                with open(decrypted_file_path, 'rb') as decrypted_file:
                    response = HttpResponse(decrypted_file.read(), content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename={"decrypted_"+uploaded_file.name}'
                    return response
            except Exception as e:
                return HttpResponse(f"Decryption failed: {str(e)}")
        else:
            return HttpResponse("No file uploaded.")
    else:
        return render(request, 'decrypt.html')
