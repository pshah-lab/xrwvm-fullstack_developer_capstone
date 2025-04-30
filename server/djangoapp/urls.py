from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from . import views
import os

app_name = 'djangoapp'

urlpatterns = [
    # path for registration
    path('register', views.registration, name='register'),

    # path for login
    path('login', views.login_user, name='login'),

    # path for logout
    path('logout', views.logout_user, name='logout'),

    # path for getting cars
    path('get_cars', views.get_cars, name='getcars'),

    # path for getting dealerships (all or by state)
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_details'),

    # path for adding a review view
    path('add_review', views.add_review, name='add_review'),

    # Serve manifest.json and favicon
    re_path(r'^manifest\.json$', serve, {
        'path': 'manifest.json',
        'document_root': os.path.join(settings.BASE_DIR, 'frontend/build')
    }),

    re_path(r'^favicon\.ico$', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(settings.BASE_DIR, 'frontend/build')
    }),

    # Serve React index.html for all other unmatched routes
    re_path(r'^.*$', views.index, name='index'),  # Serve index.html from React build folder
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)