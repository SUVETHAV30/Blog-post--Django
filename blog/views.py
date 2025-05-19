from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import Blog, Comment, Reaction, Category
from .forms import CommentForm

# Create your views here.

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        selected_category = self.request.GET.get('category')
        if selected_category:
            context['selected_category'] = selected_category
            context['blogs'] = context['blogs'].filter(category__slug=selected_category)
        return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(parent=None)
        context['reaction_counts'] = self.object.reaction_counts
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

def add_reaction(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        reaction_type = request.POST.get('reaction_type')
        user_ip = request.META.get('REMOTE_ADDR')

        if reaction_type in dict(Reaction.REACTION_CHOICES):
            reaction, created = Reaction.objects.get_or_create(
                blog=blog,
                user_ip=user_ip,
                reaction_type=reaction_type
            )
            
            if not created:
                reaction.delete()
                action = 'removed'
            else:
                action = 'added'

            return JsonResponse({
                'status': 'success',
                'action': action,
                'reaction_type': reaction_type,
                'counts': blog.reaction_counts
            })
    
    return JsonResponse({'status': 'error'}, status=400)

class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'category']
    success_url = reverse_lazy('blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'category']
    success_url = reverse_lazy('blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
