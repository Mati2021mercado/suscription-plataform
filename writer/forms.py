from . models import Article
from account.models import CustomUser
from django.forms import ModelForm

class ArticleForm(ModelForm):
    
    class Meta:
        model=Article
        fields= ['title', 'content', 'is_premium']
        
        

class UpdateUserForm(ModelForm):
    
    password = None
    
    class Meta:
        
        model=CustomUser
        fields= ['email','first_name','last_name', 'api_key']
        exclude= ['password1','password2']