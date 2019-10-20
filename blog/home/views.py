from django.shortcuts import render ,get_object_or_404
from .models import *
from django.core.paginator import Paginator , 	PageNotAnInteger , EmptyPage
from django.core.mail import send_mail
from django.views.generic import ListView
from .forms import *


def post_list_without_pagination(request):
    posts = Post.published.all()
    print(posts)
    return render(request,'home/post/list.html',{'posts':posts})

def get_post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,
                                slug=post,status='published',
                                publish__year=year,publish__month=month,publish__day = day)
    comments = post.comments.filter(active = True)
    new_comment	=	None
    if request.method == "POST":
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit = False)
            comment.user = request.user
            comment.post = post
            comment.save()
            new_comment = True
            commentForm = CommentForm()
    else:
        commentForm = CommentForm()
    return render(request,'home/post/detail.html',{'post':post,'new_comment':new_comment,'comment_form':commentForm,'comments':comments})

def post_list(request):
    objects_list = Post.published.all()
    paginator = Paginator(objects_list,2)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except 	PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'home/post/list.html',{'page':page , 'posts':posts})

class PostList(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'home/post/list.html'



def post_share(request,post_id):
    post = get_object_or_404(Post,id = post_id , status = 'published')
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "{} ({}) wants from you to read {}.".format(data['name'],data['email'],post.title)
            message = "Read '{}' at\n\n{}'s comments: {}.".format(post.title ,post_url,data['name'],data['comment'])
            send_mail(subject,message,'admin@abkasm.com',[data['to'],])
            sent = True

    else:
        form = EmailPostForm()

    return render(request,'home/post/share.html',{'post':post , 'form':form , 'sent':sent})
