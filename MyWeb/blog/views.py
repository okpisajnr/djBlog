#from django.contrib.auth.mixins import LoginRequiredMixin 
from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import NewCommentForm
 
class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ['author','title', 'text']
    #login_url = 'login'

class BlogUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ['title', 'text']
    #login_url = 'login'



class BlogListView(ListView):
    model = Post
    template_name = "index.html"
    

class BlogDetailView( DetailView):
    model = Post
    template_name = "post_details.html"
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post=self.get_object()).order_by('-pub_date')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)
        return data
    
    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
                                  your_name=self.request.user,
                                  post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class BlogDeleteView(DeleteView): # new
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('index')
    #login_url = 'login'

