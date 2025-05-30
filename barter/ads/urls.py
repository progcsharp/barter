from django.urls import path
from .views import ad_list, login_view, register_view, logout_view, user_ad_list, ad_detail, ad_create, \
    user_proposal_list, ad_edit, ad_delete, proposal_accepted, proposal_rejected, proposal_create

urlpatterns = [
    path('', ad_list, name='index'),
    path('my-ads/', user_ad_list, name='my-ads'),
    path('proposals/', user_proposal_list, name='proposals'),
    path('proposal-create/<int:ad_receiver_id>', proposal_create, name='proposal-create'),
    path('proposal/accepted/<int:proposal_id>', proposal_accepted, name="proposal-accepted"),
    path('proposal/rejected/<int:proposal_id>', proposal_rejected, name="proposal-rejected"),
    path('ad/<int:ad_id>', ad_detail, name='ad-detail'),
    path('ad-create/', ad_create, name='ad-create'),
    path('ad-edit/<int:ad_id>', ad_edit, name='ad-edit'),
    path('ad-delete/<int:ad_id>', ad_delete, name='ad-delete'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]