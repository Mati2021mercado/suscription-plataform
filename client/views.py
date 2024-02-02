from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from writer.models import Article
from . models import Subscription
from account.models import CustomUser





@login_required(login_url='my_login')
def client_dashboard(request):
    
    try:
        subsDetails = Subscription.objects.get(user=request.user)
        subscription_plan = subsDetails.subscription_plan
        context = {'SubPlan':subscription_plan}
        return render(request, 'client/client-dashboard.html', context)
        
    except:
        subscription_plan = "None"
        context = {'SubPlan': subscription_plan}
        return render(request, 'client/client-dashboard.html', context)
    



#######
#######
#######



@login_required(login_url='my_login')
def browse_articles(request):
    
    #que el usuario conectado que va a ver los articulos sea uno que este subscripto
    try:
        subDetails = Subscription.objects.get(user=request.user, is_active=True)
        
    except:
        return render(request, 'client/subscription-locked.html')
    
    current_subscription_plan = subDetails.subscription_plan
    
    if current_subscription_plan == 'Standard':
        articles = Article.objects.all().filter(is_premium=False)
        
    elif current_subscription_plan == 'Premium':
        articles = Article.objects.all()
        
    context = {'AllClientsArticles':articles}
    return render(request, 'client/browse-articles.html', context)




##########
##########
##########




@login_required(login_url='my_login')
def subscription_locked(request):
    
    return render(request,'client/subscription-locked.html')


###############
###############
###############




@login_required(login_url='my_login')
def subscription_plans(request):
    
    return render(request,'client/subscription-plans.html')



###############
###############
###############


@login_required(login_url='my_login')
def account_management_client(request):
    return render(request,'client/account-management-client.html')


###############
###############
###############


@login_required(login_url='my_login')
def create_subscription(request, subID, plan):
    
    #compara el email en nuestra base de datos con el email del usuario actualmente conectado y agarra ese particular usuario conectado y le asigna variables...
    custom_user = CustomUser.objects.get(email = request.user)
    
    firstName = custom_user.first_name
    lastName = custom_user.last_name
    fullName = firstName + " " + lastName
    
    selected_sub_plan = plan
    
    if selected_sub_plan == "Standard":
        
        sub_cost = "0.10"
    
    elif selected_sub_plan == "Premium":
        
        sub_cost = "0.15"
        
    #Se crea la subscripcion
    subscription = Subscription.objects.create(
        subscriber_name = fullName,
        subscription_plan = selected_sub_plan,
        subscription_cost = sub_cost,
        paypal_subscription_id = subID,
        is_active = True,
        user = request.user
        
    )
    context = {'SubscriptionPlan':selected_sub_plan}
    
    return render(request, 'client/create-subscription.html', context)
