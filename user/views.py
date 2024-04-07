from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from phone_store_for_GITHUB import settings
from product import models
from user import forms
from user.forms import ProfileForm


class LoginUser(LoginView):
    form_class = forms.UserForm
    template_name = 'user/login_user.html'
    extra_context = {'title': 'Login'}

    def get_success_url(self):
        # TO DO
        # next_url = self.request.POST.get('next')
        # if next_url:
        #     print(next_url)
        #     return next_url
        # else:
        return reverse_lazy('products')


# def register(request):
#     if request.method == 'POST':
#         form = forms.UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             return render(request, 'user/register_done.html', {'form': form})
#     else:
#         form = forms.UserRegistrationForm()
#         return render(request, 'user/register.html', context={'form': form})


class UserRegister(CreateView):
    form_class = forms.UserRegistrationForm
    extra_context = {'title': 'Register'}
    template_name = 'user/registration_user.html'
    success_url = reverse_lazy('user:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'user/profile_user.html'
    model = get_user_model()
    form_class = forms.ProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = models.Basket.objects.filter(user=self.request.user)
        context['title'] = 'Profile'
        context['default_photo'] = settings.DEFAULT_USER_PHOTO
        return context

    def get_success_url(self):
        return reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'user/password_change.html'
    extra_context = {'title': 'Password Reset'}
    form = forms.ChangePasswordForm
    success_url = reverse_lazy('user:profile')


def add_to_basket(request, product_id):
    product = models.PhoneProduct.objects.get(pk=product_id)

    if models.Basket.objects.filter(user=request.user, product=product).exists():
        basket = models.Basket.objects.get(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
    else:
        basket = models.Basket.objects.create(user=request.user, product=product)
    return redirect('products')


def delete_from_basket(request, product_id):
    product = models.PhoneProduct.objects.get(pk=product_id)

    basket = models.Basket.objects.get(product=product, user=request.user)
    if 'delete_single' in request.POST:
        if basket.quantity > 1:
            basket.quantity -= 1
            basket.save()
        else:
            basket.delete()
    else:
        basket.delete()
    return redirect('user:profile')
