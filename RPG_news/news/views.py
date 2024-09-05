from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter, CommFilter
from .forms import PostForm, CommForm, CommConfirmForm
from .models import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.http import Http404
from django.urls import reverse_lazy
from .mixin import *

class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/details.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = Comment()
        return context



class PostCreate( PermissionRequiredMixin, CreateView ):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'Post_edit.html'
    raise_exception = True

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username': self.request.user.username})

    def form_valid(self, fors):
        post = fors.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(fors)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'Post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'Post_delete.html'
    #success_url = reverse_lazy('post_list')
    group_required = 'Автор'

    def get_success_url(self):
        return reverse('post_list')


class CommentList(ListView):
    model = Comment
    template_name = 'CommentList.html'
    context_object_name = 'CommentList'


    def get_queryset(self):
        queryset = Comment.objects.filter(message=self.kwargs['pk']).order_by('-dateComm')
        return queryset

class MyCommentList(ListView):
    model = Comment
    template_name = 'MyCommentList.html'
    context_object_name = 'MyCommentList'
    ordering = '-dateComm'

    def get_queryset(self):
        queryset = Comment.objects.filter(message__author__id=self.request.user.id)
        self.filterset = CommFilter(self.request.GET, queryset, request=self.request.user.id)
        if not self.request.GET:
            return Comment.objects.none()
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['get'] = self.request.GET
        return context


class CommCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommForm
    raise_exception = True
    template_name = 'CommCreate.html'

    def form_valid(self, form, *args, **kwargs):
        self.post = form.save(commit=False)
        self.post.author = self.request.user
        self.post.save()
        return super().form_valid(form)

@login_required
def profile(request, pk=None):
    if pk:
        post_owner = get_object_or_404(User, pk=pk)
        user_posts = Post.objects.filter(author_id=request.user).order_by('-dateMsg')

    else:
        post_owner = request.user
        user_posts = Post.objects.filter(author_id=request.user).order_by('-dateMsg')
    return render(request, 'profile_page.html', {'post_owner': post_owner, 'user_posts': user_posts})




class OneComm(DetailView):
    model = Comment
    context_object_name = 'OneComm'
    template_name = 'OneComm.html'

class CommDel(PermissionRequiredMixin, DeleteView):
    permission_required = 'app.delete_comment'
    model = Comment
    template_name = 'CommDel.html'
    success_url = 'http://127.0.0.1:8000/comm'
    context_object_name = 'CommDel'


class CommConfirm(PermissionRequiredMixin, UpdateView):
    permission_required = 'app.change_comment'
    model = Comment
    template_name = 'CommConfirm.html'
    form_class = CommConfirmForm
    success_url = 'http://127.0.0.1:8000/comm'

class UserProfileView(TemplateView):
    template_name = 'news/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = get_object_or_404(User, username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        context['user_profile'] = user
        context['title'] = f'Профиль пользователя {user}'
        context['user_posts'] = Post.objects.filter(author=self.request.user)
        return context


class EditPostByAuthorView(PostUpdate, PermissionSameAuthorMixin, UpdateView):
    extra_context = {'title': 'Изменить пост'}
