from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
#
# posts=[
#     {
#         'AUTHOR': "CoreysMS",
#         'title': "Blog Post",
#         'content': "Hello",
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'AUTHOR': "EF",
#         'title': "Blog PostNew",
#         'content': "Salam",
#         'date_posted': 'June 27, 2018'
#     }
# ]
titleName = "About"

def home(request):
    titleName = "Home"
    context={
        'posts': Post.objects.all(), #get from db instead of dummmy data
        'title': titleName
    }
    return render(request, 'blog/home.html', context)
    # return HttpResponse('<h1>Hello World</h1>')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/><model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/><model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) #kwargs query paramater helt to get from url
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    context = {
        'title': titleName
    }
    return render(request, 'blog/about.html', context)
