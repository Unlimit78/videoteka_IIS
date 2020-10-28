from django.urls import path,include

from .views import VideoListView,UserLogin,UserLogout,NewVideo,CartView,process_payment,payment_done,payment_canceled

urlpatterns = [
    path('',VideoListView.as_view(),name='index'),
    path('accounts/login/',UserLogin.as_view(),name='login'),
    path('accounts/logout/',UserLogout.as_view(),name='logout'),
    path('new',NewVideo.as_view(),name='new'),
    path('cart',CartView.as_view(),name='cart'),
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]
