"""Selection_Trails URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('adm_view_verify_academy/', views.adm_view_verify_academy),
    path('adm_view_verify_academy_post/', views.adm_view_verify_academy_post),

    path('adm_approve_academy/<id>', views.adm_approve_academy),
    path('adm_reject_academy/<id>', views.adm_reject_academy),

    path('adm_add_game/',views.adm_add_game),
    path('adm_add_game_post/',views.adm_add_game_post),

    path('adm_view_game/',views.adm_view_game),

    path('adm_delete_game_post/<tid>',views.adm_delete_game_post),


    path('adm_edit_game/<tid>', views.adm_edit_game),
    path('adm_edit_game_post/', views.adm_edit_game_post),

    path('login/', views.login),
    path('login_post/', views.login_post),

    path('adm_home/',views.adm_home),

    path('adm_sent_reply/<id>', views.adm_sent_reply),
    path('adm_sent_reply_post/',views.adm_sent_reply_post),



    path('adm_view_approved_academy/', views.adm_view_approved_academy),
    path('adm_view_approved_academy_post/', views.adm_view_approved_academy_post),

    path('adm_view_rejected_academy/', views.adm_view_rejected_academy),
    path('adm_view_rejected_academy_post/', views.adm_view_rejected_academy_post),



    path('adm_view_coach_approve_reject/', views.adm_view_coach_approve_reject),
    path('adm_approve_coaches/<id>',views.adm_approve_coaches),
    path('adm_reject_coaches/<id>',views.adm_reject_coaches),

    path('adm_view_approved_coaches/', views.adm_view_approved_coaches),
    path('adm_view_approved_coaches_post/', views.adm_view_approved_coaches_post),

    path('adm_view_rejected_coaches/', views.adm_view_rejected_coaches),
    path('adm_view_rejected_coaches_post/', views.adm_view_rejected_coaches_post),



    path('adm_view_trails/', views.adm_view_trails),
    path('adm_view_trails_post/', views.adm_view_trails_post),

    path('adm_view_complaints_sent_reply/', views.adm_view_complaints_sent_reply),
    path('adm_view_complaints_sent_reply_post/', views.adm_view_complaints_sent_reply_post),

    path('adm_change_password/', views.adm_change_password),
    path('adm_change_password_post/', views.adm_change_password_post),

    path('adm_view_reviews_about_academy/<id>', views.adm_view_reviews_about_academy),
    path('adm_view_reviews_about_academy_post/', views.adm_view_reviews_about_academy_post),
    path('adm_view_reviews_about_coach/<id>', views.adm_view_reviews_about_coach),
    path('adm_view_reviews_about_coach_post/', views.adm_view_reviews_about_coach_post),

    #============Academy===============


    path('acd_signup/', views.acd_signup),
    path('acd_signup_post/', views.acd_signup_post),
    path('acd_home/', views.acd_home),
    path('acd_call_for_trials/', views.acd_call_for_trials),
    path('acd_call_for_trials_post/', views.acd_call_for_trials_post),

    path('acd_change_password/', views.acd_change_password),
    path('acd_change_password_post/', views.acd_change_password_post),

    path('acd_edit_profile/<id>', views.acd_edit_profile),
    path('acd_edit_profile_post/', views.acd_edit_profile_post),

    path('acd_edit_trials/<tid>', views.acd_edit_trials),
    path('acd_edit_trials_post/', views.acd_edit_trials_post),

    path('acd_delete_trials_post/<tid>',views.acd_delete_trials_post),

    path('acd_message_with_players/',views.acd_message_with_players),
    path('acd_message_with_players_post/',views.acd_message_with_players_post),
    path('acd_send_complaint/', views.acd_send_complaint),
    path('acd_send_complaint_post/', views.acd_send_complaint_post),
    path('acd_view_reply/', views.acd_view_reply),
    path('acd_view_reply_post/', views.acd_view_reply_post),

    path('acd_view_player_for_trials/', views.acd_view_player_for_trials),
    path('acd_view_player_for_trials_post/', views.acd_view_player_for_trials_post),

    path('acd_approve_player/<id>', views.acd_approve_player),
    path('acd_reject_player/<id>', views.acd_reject_player),

    path('acd_rejected_player_for_trials/', views.acd_rejected_player_for_trials),
    path('acd_rejected_player_for_trials_post/', views.acd_rejected_player_for_trials_post),

    path('acd_approved_player_for_trials/', views.acd_approved_player_for_trials),
    path('acd_approved_player_for_trials_post/', views.acd_approved_player_for_trials_post),

    path('acd_attend_players/<id>', views.acd_attend_players),
    path('acd_view_attended_players/', views.acd_view_attended_players),
    path('acd_view_attended_players_post/', views.acd_view_attended_players_post),

    path('acd_shortlist_players/<id>', views.acd_shortlist_players),
    path('acd_view_shortlist_players/', views.acd_view_shortlist_players),
    path('acd_view_shortlist_players_post/', views.acd_view_shortlist_players_post),


    path('acd_view_profile/', views.acd_view_profile),

    path('acd_view_reviews/', views.acd_view_reviews),
    path('acd_view_reviews_post/', views.acd_view_reviews_post),

    path('acd_view_trials/', views.acd_view_trials),
    path('acd_view_trials_post/', views.acd_view_trials_post),

    path('chat/<id>', views.chat),
    path('chat_view/', views.chat_view),
    path('chat_send/<msg>', views.chat_send),



# -------------------FLUTTER---------------------------------------



    path('ply_change_password/',views.ply_change_password),

    path('ply_login/', views.ply_login),

    path('ply_signup/', views.ply_signup),

    path('ply_view_profile/', views.ply_view_profile),

    path('ply_edit_profile/', views.ply_edit_profile),

    path('ply_viewchat/', views.ply_viewchat),

    path('ply_sendchat/', views.ply_sendchat),

    path('ply_view_chat_coach/', views.ply_view_chat_coach),

    path('ply_sendchat_acd/', views.ply_sendchat_acd),

    path('ply_viewchat_acd/', views.ply_viewchat_acd),

    path('ply_view_chat_acd/', views.ply_view_chat_acd),

    path('ply_view_coach_and_follow/', views.ply_view_coach_and_follow),

    path('ply_view_followed_coach/', views.ply_view_followed_coach),

    path('ply_view_trial/', views.ply_view_trial),

    path('ply_apply_trial/', views.ply_apply_trial),

    path('ply_view_applied_trials/', views.ply_view_applied_trials),

    path('ply_view_certificate_of_coach/', views.ply_view_certificate_of_coach),


    # -------------------FLUTTER---------------------------------------


    path('coc_signup/', views.coc_signup),

    path('coc_view_profile/', views.coc_view_profile),

    path('coc_edit_profile/', views.coc_edit_profile),

    path('coc_sendchat/', views.coc_sendchat),

    path('coc_viewchat/', views.coc_viewchat),

    path('coc_view_chat_player/', views.coc_view_chat_player),

    path('coc_add_experience/', views.coc_add_experience),

    path('coc_view_experience/', views.coc_view_experience),

    path('coc_edit_experience/', views.coc_edit_experience),

    path('coc_edit_experience_get/', views.coc_edit_experience_get),

    path('coc_view_reply/', views.coc_view_reply),

    path('coc_send_complaint/', views.coc_send_complaint),

    path('coc_add_tips/', views.coc_add_tips),

    path('coc_view_tips/', views.coc_view_tips),



]