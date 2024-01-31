from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record, Communication_Record, Group_Record
from .forms import AddRecordForm, AddGroupForm

# Create your views here.

def home(request):
    
    # load data records
    records = Record.objects.all()
    group_records = Group_Record.objects.all()
    
    
    
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
        return render(request, 'home.html', {'records': records, 'group_records': group_records})
    


def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out....")
    return redirect('home')


def customer_record(request, pk):
    if request.user.is_authenticated:
        
        # lookup records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    
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
        return render(request, 'group_record.html', {'group_member_record': group_member_record })
    
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
    pass
            
