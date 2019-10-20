from django.urls import path
from .views import *

app_name = 'home'
urlpatterns = [
    path('', PostList.as_view(), name = 'post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',get_post_detail,name = 'post_detail'),
    path('<int:post_id>/share/',post_share, name = 'post_share'),
]
