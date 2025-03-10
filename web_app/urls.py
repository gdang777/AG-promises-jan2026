from django.urls import path
from . import views
urlpatterns=[
    path('',views.Index.as_view(),name='index'),
    # path('/<str:name>',views.Index.as_view(),name='index'),
]