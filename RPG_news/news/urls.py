from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', cache_page(0)(PostList.as_view()), name='post_list'),
    path('<int:pk>', cache_page(0)(PostDetailView.as_view()), name='post_detail'),
    path('<int:pk>/comments', CommentList.as_view(), name='Comments'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('<int:pk>/addcomment', CommCreate.as_view(), name='addcomm'),
    path('comm/', MyCommentList.as_view(), name='comm'),
    path('comments/<int:pk>', OneComm.as_view(), name='onecomm'),
    path('comments/<int:pk>/delete', CommDel.as_view(), name='delcomm'),
    path('comments/<int:pk>/confirm', CommConfirm.as_view(), name='confirm'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
]
