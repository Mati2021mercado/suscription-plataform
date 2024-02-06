from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from writer.models import Article
from . models import Subscription
from account.models import CustomUser
from . paypal import *




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
    
    try:
        
        subDetails = Subscription.objects.get(user=request.user)
        
        subscription_id = subDetails.paypal_subscription_id
        
        context = {'SubscriptionID': subscription_id}
    
        return render(request,'client/account-management-client.html', context)
    
    except:
        
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
        
        sub_cost = "1.99"
    
    elif selected_sub_plan == "Premium":
        
        sub_cost = "4.99"
        
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




###############
###############
###############


@login_required(login_url='my_login')
def delete_subscription(request, subID):
    
    # Delete subscription from paypal
    
    access_token = get_access_token()
    cancel_subscription_paypal(access_token, subID)
    
    #Delete a subscription from Django (application side)
    
    subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=subID)
    subscription.delete()
    
    return render(request, 'client/delete-subscription.html')




###############
###############
###############



@login_required(login_url='my_login')
def update_subscription(request, subID):
    
    access_token = get_access_token()
    
    #approve_link = Hateoas link from paypal
    
    approve_link = update_subscription_paypal(access_token, subID)
    
    #si no es None
    if approve_link:
        return redirect(approve_link)
    
    else:
        return HttpResponse("no se puede obtener el enlace de aprobación")
    
    
    

###############
###############
###############


@login_required(login_url='my_login')
def paypal_update_sub_confirmed(request):
    
    try: 
    
        subDetails = Subscription.objects.get(user=request.user)
        
        subscriptionID = subDetails.paypal_subscription_id
        
        context = {'SubscriptionID':subscriptionID}
        
        return render(request, 'client/paypal-update-sub-confirmed.html', context)
    
    except:
        
        return render(request, 'client/paypal-update-sub-confirmed.html')



###############
###############
###############


@login_required(login_url='my_login')
def django_update_sub_confirmed(request, subID):
    
    access_token = get_access_token()
    
    current_plan_id = get_current_subscription(access_token, subID)
    
    #Si el ID del plan coinside con el ID del plan Standard (variable plan_id en subscription-plans.html)
    if current_plan_id == 'P-2NY579910G678903UMXA5S7Q': # Standard
        
        new_plan_name = "Standard"
        new_cost = "1.99"
        
        #Redefino los valores de las variables (fields) del Modelo del usuario
        Subscription.objects.filter(paypal_subscription_id=subID).update(
            subscription_plan = new_plan_name,
            subscription_cost = new_cost
            )
    
    elif current_plan_id == 'P-7FN8721886700203NMXA5UNA': # Premium
        
        new_plan_name = "Premium"
        new_cost = "4.99"
        
        #Redefino los valores de las variables (fields) del Modelo del usuario
        Subscription.objects.filter(paypal_subscription_id=subID).update(
            subscription_plan = new_plan_name,
            subscription_cost = new_cost
            )
        
    return render(request, 'client/paypal-update-sub-confirmed.html')