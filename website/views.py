from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record, Communication_Record, Group_Record, Sender, Group_Communication_Record
from .forms import AddRecordForm, AddGroupForm, AddSenderForm, ChatMessageForm, ChatGroupMessageForm
from django import template
import json,random, string, time, requests
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

register = template.Library()
@register.simple_tag
def to_list(*args):
    return args

# Create your views here.
def sendWAMessage(phoneNumber, message, token):
    string = 'Bearer '
    full_token = string + token
    headers = {"Authorization": full_token}
    payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phoneNumber,
            "type": "text",
            "text": {"body":message}  
               }
    respone = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = respone.json()
    print(ans)
    
    dict_ans=json.dumps(ans)
    
    key = 'error'
    if key in dict_ans:
        print('error found')
        return False
    else:
        print('no error')
        return True
    

@csrf_exempt
def whatsAppWebhook(request):
    if request.method =='GET':
        VERIFY_TOKEN = ''
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']
        
        if mode == 'subscribe' and token ==  VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('error', status=403)
    
    if  request.method == 'POST':
        data = json.loads(request.body)
        
        return HttpResponse('success', status=200)
    
    
def home(request):
    
    # load data records
    records = Record.objects.all()
    group_records = Group_Record.objects.all()
    sender_records = Sender.objects.all()
    
    
    
    # check login
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect('home')
        else:
            messages.success(request, "Error Login...")
            return redirect('home')
    else:          
        return render(request, 'home.html', {'records': records, 'group_records': group_records, 'sender_records': sender_records})
    


def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out....")
    return redirect('home')


def customer_record(request, pk):
    if request.user.is_authenticated:
        
        # lookup records
        customer_record = Record.objects.get(id=pk)
        chats = Communication_Record.objects.all()
        return render(request, 'record.html', {'customer_record': customer_record, 'chats':chats})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    

def  delete_customer_record(request, pk):
    if request.user.is_authenticated:
        
        #delete records
        delete_customer = Record.objects.get(id=pk)
        delete_customer.delete()
        messages.success(request, "Record Deleted...")
        return redirect('home')
        
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    
    
def  add_customer_record(request):
    if request.user.is_authenticated:
        
        form = AddRecordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                add_customer_record = form.save()
                messages.success(request, "New Customer Infor Added...")
                return redirect('home')
        
        return render(request, 'add_customer_record.html', {'form':form})
        
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    
    
    
def update_customer_record(request, pk):
    
    if request.user.is_authenticated:
            
        #delete records
        current_customer = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_customer)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated...")
            return redirect('home')
        
        return render(request, 'update_customer_record.html', {'form':form})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    

def group_record(request, pk):
    if request.user.is_authenticated:
        
        # lookup records
        group_member_record = Group_Record.objects.get(id=pk)
        group_chats = Group_Communication_Record.objects.all()
        return render(request, 'group_record.html', {'group_member_record': group_member_record, 'group_chats':group_chats })
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    

def  delete_group_record(request, pk):
    if request.user.is_authenticated:
        
        #delete records
        delete_group = Group_Record.objects.get(id=pk)
        delete_group.delete()
        messages.success(request, "Group Deleted...")
        return redirect('home')
        
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    
    
def  add_group_record(request):
    if request.user.is_authenticated:
        
        form = AddGroupForm(request.POST or None)
        
        if request.method == "POST":
            if form.is_valid():
                add_group_record = form.save()
                messages.success(request, "New Group Created...")
                return redirect('home')
        
        return render(request, 'add_group_record.html', {'form':form})
        
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    
    
def update_group_record(request, pk):
    
    if request.user.is_authenticated:
            
        #delete records
        current_group = Group_Record.objects.get(id=pk)
        form = AddGroupForm(request.POST or None, instance=current_group)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Group Updated...")
            return redirect('home')
        
        return render(request, 'update_group_record.html', {'form':form})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    
    
def sender_record(request, pk):
    if request.user.is_authenticated:
            
        #delete records
        sender_record = Sender.objects.get(id=pk)
        return render(request, 'sender.html', {'sender_record':sender_record})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    

def  delete_sender_record(request, pk):
    if request.user.is_authenticated:
        
        #delete records
        delete_sender_record = Sender.objects.get(id=pk)
        delete_sender_record.delete()
        messages.success(request, "Group Deleted...")
        return redirect('home')
        
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    
    
def  add_sender_record(request):
    if request.user.is_authenticated:
        
        form = AddSenderForm(request.POST or None)
        
        if request.method == "POST":
            if form.is_valid():
                add_sneder_record = form.save()
                messages.success(request, "New Sender Created...")
                return redirect('home')
        
        return render(request, 'add_sender_record.html', {'form':form})
        
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    
    
def update_sender_record(request, pk):
    
    if request.user.is_authenticated:
            
        #delete records
        current_group = Sender.objects.get(id=pk)
        form = AddSenderForm(request.POST or None, instance=current_group)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Sender Updated...")
            return redirect('home')
        
        return render(request, 'update_sender_record.html', {'form':form})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')
    
def sendMessageIndividual(request):
    
    if request.user.is_authenticated:
        
        form = ChatMessageForm(request.POST or None)
        
        #sender = Sender.objects.get(id=request.POST.get('sender'))
        #receiver = Record.objects.get(id=request.POST.get('contact'))
        #sender = request.POST.get('sender')
        #receiver = request.POST.get('contact')
        
        if request.method == "POST":
            if form.is_valid():
                new_message = form.save(commit=False)
                new_message.sender = Sender.objects.get(id=request.POST.get('sender'))
                new_message.contact = Record.objects.get(id=request.POST.get('contact'))
                
                token = new_message.sender.access_token
                phone = new_message.contact.phone
                message = new_message.message_text
                ans = sendWAMessage(phone, message, token)
                
                if ans == True:
                    new_message.status = 'sent'
                    new_message.save()
                    messages.success(request, "New Message send...")
                    return redirect('home')
                else:
                    # 这里要搞re-sent那个东西
                    messages.success(request, "Error...")
                    return redirect('home')
        
        return render(request, 'sendMessageIndividual.html', {'form':form})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')

def sendGroupMessageIndividual(request):
    
    form = ChatGroupMessageForm(request.POST or None)
    #individual = ChatMessageForm(request.POST or None)
    
    if request.user.is_authenticated:
        
        if request.method == "POST":
            if form.is_valid():
                new_group_message = form.save(commit=False)
                new_group_message.sender = Sender.objects.get(id=request.POST.get('sender'))
                new_group_message.group = Group_Record.objects.get(id=request.POST.get('group'))
                
                print(new_group_message.group.user.all())
                print(new_group_message.group_message_text)
                
               
                
                for individual_object in new_group_message.group.user.all():
                    individual_message = Communication_Record.objects.create(
                    sender = new_group_message.sender,
                    contact = individual_object,
                    message_text = new_group_message.group_message_text,
                    )
                    individual_message.save
                    
                new_group_message.save()
                
                #records = new_group_message.group.user.all()
              
               
                messages.success(request, "New Group Message send...")
                return redirect('home')
        
        return render(request, 'sendGroupMessageIndividual.html', {'form':form})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')

