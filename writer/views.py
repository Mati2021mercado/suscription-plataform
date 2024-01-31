from django.shortcuts import render, redirect
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
               
               return redirect('my-articles')
          
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


#Tenemos nuestra vista de artículo de actualización aquí configurada,
#Estamos pasando, estamos usando la clave principal como placeholder

@login_required(login_url='my_login')
def update_article(request, pk):
     
     # Obtener el objeto Article con el ID igual al valor de pk
     # Cada objeto Article será un modelo que represente un artículo en la base de datos,
     # y su ID será igual a la PK (Primary Key) que se pasa como parámetro en la URL dinámica
     
     #user=request.user verifica que el mismo usuario que creo el post sea el que lo va a editar, para que si alguien que no es el usuario lo intente editar, no pueda. ¿como? me aseguro de que el usuario que está conectado actualmente sea igual al usuario que publicó ese artículo en particular.
     
     try:
          article = Article.objects.get(id=pk, user=request.user)
     except:
          return redirect('my-articles')
     # asegurarnos de completar previamente un formulario con los datos de esa instancia particular que estamos solicitando a través de nuestra URL dinámica haciendo nuestra solicitud de Publicación asegurando que ese artículo en particular se actualice
     
     # se está inicializando el formulario con los datos del artículo existente que se obtuvo de la base de datos utilizando Article.objects.get(id=pk). 
     # Esto significa que el formulario se rellenará automáticamente con los datos del artículo que se está actualizando.
     form = ArticleForm(instance=article)
     
     if request.method == 'POST':
          form = ArticleForm(request.POST, instance=article)
          
          if form.is_valid():
                #mandamos los datos a la base de datos
               form.save()
               
               return redirect('my-articles')
     
     context = {'UpdateArticleForm': form}
     
     return render(request, 'writer/update-article.html', context)


@login_required(login_url='my_login')
def delete_article(request, pk):
     
     try:
          article = Article.objects.get(id=pk, user=request.user)
     except:
          return redirect('my-articles')
          
     if request.method == 'POST':
          article.delete()
          
          return redirect('my-articles')
     
     return render(request, 'writer/delete-article.html')