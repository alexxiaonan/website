from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record, Communication_Record, Group_Record, Sender, Group_Communication_Record
from .forms import AddRecordForm, AddGroupForm, AddSenderForm, ChatMessageForm, ChatGroupMessageForm
from django import template
import json,random, string, time, requests, re
import phonenumbers
from phonenumbers.phonenumberutil import number_type
from email_validator import validate_email, EmailNotValidError
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def validate_au_mobile(number):
    try:
        parsed_number = phonenumbers.parse(number, "AU")
        return number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE
    except phonenumbers.phonenumberutil.NumberFormatException:
        return False

def is_email_valid(email):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        email = emailinfo.normalized
        return True
    except EmailNotValidError as e:
        print(str(e))
        return False

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
        VERIFY_TOKEN = '4eee0753-2969-4c14-9bc7-387234169bc5'
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']
        
        if mode == 'subscribe' and token ==  VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('error', status=403)
    
    if request.method =='POST':
        data = json.loads(request.body)
        print(data)
        if 'object' in data and 'entry' in data:
             if data['object'] == 'whatsapp_business_account':
                 try:
                     for entry in data['entry']:
                         phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                         print(phoneNumber)
                         phoneID = entry['changes'][0]['value']['metadata']['phone_number_id']
                         profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                         print(profileName)
                         whatsAppID = entry['changes'][0]['value']['contacts'][0]['wa_id']
                         fromID = entry['changes'][0]['value']['messages'][0]['from']
                         print(fromID)
                         messageID = entry['changes'][0]['value']['messages'][0]['id']
                         timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                         text = entry['changes'][0]['value']['messages'][0]['text']['body']
                         
                         print(text)

                         phone = "+61447284449"
                         # message = 'RE: {} was received'.format(text)
                         # message = '2'
                         # token = 'EAAO1oqsZAGHUBO6UOy4vzHncBwb8YWliGSZBl7cmAmlbsluBKiAUbTZCx7y1aOom2tib3zvrXUeZB5dOjbKB3x9dHqq1CVNQsM4wgWwZAqQqYYZBZCgVjdQvwgxVlDPOAfeUE5QjaGck4RFwFw8X0acFnBE5F67Yhj5oJlbFIeEG1ZACMxkH8LqkIb5P5hrNVBUZB5FxBdNeVDEwZCKLqIhPkZD'
                         # ans = sendWAMessage(phone, message, token)
                         string_test = 'Bearer EAAO1oqsZAGHUBOzddh29L9ZBNbPYwfdSdBAuQi162H59oyth5fkvdKKJqz9K8aNjonxmP1ZA38cJfVzQzNZA4OqV0vUiPcR7lEM1z8O78BP4EeaRfGb8PIFcXK9dBoYoMzAme8tWpMOUZCkj59hTLLFyStPfOwEQcPrBck22ZAbVMYjCpZAQYpoyjFxsBRCinhzQN05WlSMNRthq7AYSBnC'
    
                         headers = {"Authorization": string_test}
                         payload = {
                                  "messaging_product": "whatsapp",
                                  "recipient_type": "individual",
                                  "to": phone,
                                  "type": "text",
                                  "text": {"body":text}  
                                   }
                         respone = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
                         ans = respone.json()
                         print(ans)


                 except:
                     pass

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
            data = request.POST.copy()
            _muatble = data._mutable
            data._mutable = True
            
            phone = request.POST.get('phone')
            phone_str=str(phone)
            
            if len(phone_str) == 10 and phone_str[0] == '0':
                new_phone_str =  '+61' + phone_str[1:] 
                print(new_phone_str)
                data['phone'] = new_phone_str
                data._mutable = _muatble
            elif len(phone_str) == 9:
                new_phone_str =  '+61' + phone_str 
                print(new_phone_str)
                data['phone'] = new_phone_str
                data._mutable = _muatble
        
            form = AddRecordForm(data)
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            verify_phone_exists = Record.objects.filter(phone=str(phone)).exists()
            
            if form.is_valid():
                is_au_mobile = validate_au_mobile(phone)
                is_email_address_valid = is_email_valid(email)
                #print(is_au_mobile, is_email_address_valid)
                
                if is_au_mobile == True and is_email_address_valid == True and verify_phone_exists == False:
                    add_customer_record = form.save()
                    messages.success(request, "New Customer Infor Added...")
                    return redirect('home')
                elif verify_phone_exists:
                    messages.success(request, "Phone Number Existed in Database")
                elif is_au_mobile == False:
                    messages.success(request, "Incorrect Phone Number")
                elif is_email_address_valid == False:
                    messages.success(request, "Incorrect Email Address")
                else:
                    messages.success(request, "Incorrect Phone Number and Email Address")
        
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
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            
            #print(phone, email)
             
            is_au_mobile = validate_au_mobile(phone)
            is_email_address_valid = is_email_valid(email)
            verify_phone_exists = Record.objects.filter(phone=str(phone)).exists()
            
            if is_au_mobile == True and is_email_address_valid == True and verify_phone_exists == False:
                updateform = form.save(commit=False)
                phone_str=str(updateform.phone)
                if len(phone_str) == 10 and phone_str[0] == '0':
                    new_phone_str =  '+61' + phone_str[1:] 
                    #print(new_phone_str)
                    updateform.phone = new_phone_str
                elif len(phone_str) == 9:
                    new_phone_str =  '+61' + phone_str 
                    #print(new_phone_str)
                    updateform.phone = new_phone_str
                
                if Record.objects.filter(phone=str(updateform.phone)).exists() == False:
                    updateform.save()
                    messages.success(request, "Record Updated...")
                    return redirect('home')
                else:
                    messages.success(request, "Phone Number Existed in Database")
                    
            elif verify_phone_exists:
                    messages.success(request, "Phone Number Existed in Database")
            elif is_au_mobile == False:
                messages.success(request, "Incorrect Phone Number")
            elif is_email_address_valid == False:
                messages.success(request, "Incorrect Email Address")
            else:
                messages.success(request, "Incorrect Phone Number and Email Address")
        
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
                    new_message.status = 'error'
                    new_message.save()
                    messages.success(request, "Error...")
                    return redirect('home')
        
        return render(request, 'sendMessageIndividual.html', {'form':form})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')

def sendGroupMessageIndividual(request):
    
    form = ChatGroupMessageForm(request.POST or None)
    
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

                    token = new_group_message.sender.access_token
                    phone = individual_object.phone
                    message = new_group_message.group_message_text
                    ans = sendWAMessage(phone, message, token)

                    if ans == True:
                        individual_message.status = 'sent'
                        individual_message.save()
                   
                    
                    else:
                        individual_message.status = 'error'
                        individual_message.save()
                  
                    
                new_group_message.save()
               
                messages.success(request, "New Group Message send...")
                return redirect('home')
        
        return render(request, 'sendGroupMessageIndividual.html', {'form':form})
    
    else:
        messages.success(request, "Login First...")
        return redirect('home')

