from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, Comment, Contact,Profile
from .forms import ArticleForm, CommentForm, ContactForm,ProfileForm
from django.contrib.auth.models import User  # ← تأكدي إنه موجود بالأعلى
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Profile
from django.db.models import Q  # ← لإجراء عمليات البحث المتقدمة
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from .forms import UserRegisterForm



def home(request):
    articles = Article.objects.all()
    return render(request, 'blog/home.html', {'articles': articles})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        Contact.objects.create(name=name, email=email, message=message)
        
        # إرسال إيميل
        send_mail(
            subject=f"رسالة من {name}",
            message=message,
            from_email=email,
            recipient_list=['your_email@example.com'],
        )
        
        return redirect('contact_success')  # أو أي صفحة تأكيد
        
    return render(request, 'blog/contact.html')


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'blog/add_article.html', {'form': form})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.name = request.user.username
                comment.save()
                return redirect('article_detail', pk=pk)
        else:
            return redirect('login')  # لو مش مسجل دخول يرجع للوغين

    else:
        form = CommentForm()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author:
        return HttpResponseForbidden("غير مصرح لك تعديل هذا المقال.")

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/edit_article.html', {'form': form})


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author:
        return HttpResponseForbidden("غير مصرح لك حذف هذا المقال.")

    if request.method == 'POST':
        article.delete()
        return redirect('home')
    return render(request, 'blog/delete_confirm.html', {'article': article})

def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.name != request.user.username:  # الشرط صار على الاسم بدل user
        return HttpResponseForbidden("لا يمكنك تعديل هذا التعليق")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=comment.article.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/edit_comment.html', {'form': form})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.name != request.user.username:  # الشرط على الاسم
        return HttpResponseForbidden("لا يمكنك حذف هذا التعليق")
    article_pk = comment.article.pk
    comment.delete()
    return redirect('article_detail', pk=article_pk)


from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

def category_articles(request, category):
    articles = Article.objects.filter(category=category)
    return render(request, 'blog/category_articles.html', {'articles': articles, 'category': category})

# عرض البروفايل
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile  # تأكدي من وجود علاقة بين User و Profile

    # لو البروفايل مش موجود، ممكن تعملي توجيه لصفحة خطأ أو إنشاء بروفايل جديد
    if not profile:
        return redirect('home')  # أو أي صفحة تانية

    articles = Article.objects.filter(author=user)
    return render(request, 'blog/profile.html', {'user': user, 'profile': profile, 'articles': articles})
    
# تعديل البروفايل
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    if request.user != user:
        return redirect('home')  # ما تسمحي لحدا يعدل غير بروفايله

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blog/edit_profile.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # ✅ تفعيل المستخدم فورًا
            user.save()
            login(request, user)  # ✅ تسجيل دخول مباشر
            return redirect('home')  # غيريها للصفحة اللي بدك ياها
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def search_view(request):
    query = request.GET.get('q')
    article_results = []
    comment_results = []
    author_results = []

    if query:
        article_results = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(category__icontains=query)
        )
        comment_results = Comment.objects.filter(
            Q(name__icontains=query) | Q(body__icontains=query)
        )
        author_results = User.objects.filter(
            Q(username__icontains=query)
        )

    context = {
        'query': query,
        'article_results': article_results,
        'comment_results': comment_results,
        'author_results': author_results,
    }
    return render(request, 'blog/search_results.html', context)
