from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . forms import ArticleForm
from . models import Article

@login_required(login_url='my_login')
def writer_dashboard(request):
     return render(request, 'writer/writer-dashboard.html')
    
@login_required(login_url='my_login')
def create_article(request):
     
     form = ArticleForm()
     
     if request.method == 'POST':
          form = ArticleForm(request.POST)
          
          if form.is_valid():
               article = form.save(commit=False)
               
               article.user = request.user
               
               article.save()
               
               return HttpResponse('Article created!')
          
     context = {'CreateArticleForm' : form }
     
     return render(request, 'writer/create-article.html', context)

@login_required(login_url='my_login')
def my_articles(request):
     current_user=request.user.id 
     # retorna todos los articulos que se encuentran en el objeto modelo "Article"
     # El filtro se asegura de que solo un usuario registrado pueda ver los objetos(articulos)
     article = Article.objects.all().filter(user=current_user)
     
     context = {'AllArticles': article}
     
     return render(request, 'writer/my-articles.html', context)