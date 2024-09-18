from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import available_cats, user_profile, CustomLoginView, cat_profile, put_cat_for_adoption, ask_for_adoption, search
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Home page route
    path('join_us/', views.register, name='join_us'),   # Route for registration page
    path('submit_join_us/', views.submit_join_us, name='submit_join_us'),   # Route for registration form submition
    path('login/', CustomLoginView.as_view(), name='login'),   # Route for sign in page
    path('available-cats/', available_cats, name='available_cats'),   # Route to display available cats for adoption
    path('cat/<int:cat_id>/', cat_profile, name='cat_profile'),   # Route to view a specific cat's profile by ID
    path('put_cat_for_adoption/', put_cat_for_adoption, name='put_cat_for_adoption'),   # Route to submit a cat for adoption
    path('cat/<int:cat_id>/adopt/', ask_for_adoption, name='ask_for_adoption'),   # Route to request a cat for adoption
    path('search/', search, name='search'),   # Route to handle cat search
    path('delete-cat/<int:cat_id>/', views.delete_cat, name='delete_cat'),   # Route to delete a cat by ID
    path('my-posted-cats/', views.my_posted_cats, name='my_posted_cats'),   # Route to view users posted cats
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),   # Logout route that redirects to home page
    path('profile/', user_profile, name='profile'),   # Route for viewing user's profile
    path('landing_page/', views.landing_page, name='landing_page'),   # Route for the landing page
    path('my-cat-requests/', views.my_cat_requests, name='my_cat_requests'),   # Route for viewing user's requests for adoption
    path('received-requests/', views.received_requests, name='received_requests'),   # Route for viewing user's posted cats requests
    path('update-request-status/<int:request_id>/', views.update_request_status, name='update_request_status'),   # Route to accept or decline cat request
    path('handle-adoption-request/<int:request_id>/<str:action>/', views.handle_adoption_request, name='handle_adoption_request'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # Serve media files during development
