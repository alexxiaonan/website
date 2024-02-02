from django.db import models
# Create your models here.

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contact_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    
    def __str__(self):
        return (f"{self.first_name} {self.last_name}")

class Sender(models.Model):
    phone_number_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=255)
    url =  models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

class Communication_Record(models.Model):
    sender_info = models.ForeignKey(Sender, on_delete=models.CASCADE)
    contact_id = models.ForeignKey(Record, on_delete=models.CASCADE)
    message_id = models.CharField(max_length=100)
    from_id = models.CharField(max_length=100)
    to_id = models.CharField(max_length=100)
    message_text = models.CharField(max_length=255)
    sent_datetime = models.CharField(max_length=100)
    
    def __str__(self):
        return (f"{self.contact_id} {self.message_id}")
    
    
class Group_Record(models.Model):
    group_name = models.CharField(max_length=90)
    user = models.ManyToManyField(Record)
    
    def __str__(self):
        return (f"{self.group_name} {self.user}")


    
    
