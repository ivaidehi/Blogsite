from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    path('check_username/', views.check_username, name='check_username'),
    path('debug-image/', views.debug_profile_image, name='debug_image'),
    path('role-dashboard/', views.role_based_dashboard_view, name='role_based_dashboard'),
    path('add-blog/', views.add_blog_view, name='add_blog'),
    path('drafts/', views.drafts_view, name='drafts'),
    path('get-blogs/', views.get_blogs_by_category, name='get_blogs_by_category'),
]

