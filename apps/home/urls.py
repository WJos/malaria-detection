# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'patients'

urlpatterns = [

    # The home page
    #path('', views.index, name='home'),

    #path('patients/', views.patients, name="patients"),

    path('', views.patients, name="patients"),

    path('patients/<int:id>/', views.diagnostics, name='diagnostics'),

    path('patients/diagnostics/<int:id>/', views.resultats, name='resultats'),

    path('patients/diagnostics/getimage/image_id=<int:id>', views.getImage, name = "getimage"),

    path('patients/imageview/', views.imageView, name = "imageview"),

    #r'^update/(\d+)/$'

    #path(r'^patients/', app_name='patients', namespace='patients'),

    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
