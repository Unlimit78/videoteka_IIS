from decimal import Decimal

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from paypal.standard.forms import PayPalPaymentsForm

from .models import User, VideoCasets, Genre, Types



class VideoListView(LoginRequiredMixin,ListView):
    context_object_name = "video"

    template_name = "index.html"
    def get_queryset(self):
        video = VideoCasets.objects.all()



        return video

    def post(self,request):
        user = self.request.user
        v = VideoCasets.objects.get(pk=request.POST.get('pk'))
        if v in user.cart.all():
            user.cart.remove(v)
        else:
            user.cart.add(v)
        return HttpResponseRedirect(reverse('index'))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        context['user'] = user
        context['genres'] = Genre.objects.all()
        return context


class UserLogin(LoginView):
    template_name = 'login.html'

class UserLogout(LoginRequiredMixin,LogoutView):
    template_name = 'logout.html'

class NewVideo(LoginRequiredMixin,CreateView):
    model = VideoCasets
    fields = '__all__'
    template_name = 'new_video.html'
    success_url = reverse_lazy('index')

class CartView(LoginRequiredMixin,ListView):
    context_object_name = "cart"

    template_name = "cart.html"
    def get_queryset(self):
        cart = self.request.user.cart.all()



        return cart

    def post(self,request):
        user = self.request.user
        v = VideoCasets.objects.get(pk=request.POST.get('pk'))
        if v in user.cart.all():
            user.cart.remove(v)
        else:
            user.cart.add(v)
        return HttpResponseRedirect(reverse('index'))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        context['user'] = user
        context['liked'] = user.liked.all()
        prices = [i.price for i in user.cart.all()]
        context['sum'] = sum(prices)

        return context


def process_payment(request):
    user = request.user
    prices = [i.price for i in user.cart.all()]
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % sum(prices),
        'item_name': 'Order {}'.format(user.pk),
        'invoice': str(user.pk),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})


@csrf_exempt
def payment_done(request):
    for i in request.user.cart.all():
        request.user.cart.all().remove(i)
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')


