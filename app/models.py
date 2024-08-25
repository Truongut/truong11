from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
# change froms register django
class CreatUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()  # Added parentheses after FloatField
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url    
class Order(models.Model):  # Corrected the spelling from 'Oder' to 'Order'
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=False, null=True)
    date_order = models.DateTimeField(auto_now_add=True)  # Corrected the field name from 'date_oder' to 'date_order'
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)  # Corrected 'max_Length' to 'max_length'
    
    def __str__(self):
        return str(self.id)  
    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total
    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total
class OrderItem(models.Model):  # Corrected the spelling from 'OderItem' to 'OrderItem'
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False, null=True)  # Corrected the spelling from 'oder' to 'order'
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False, null=True)  # Corrected the spelling from 'oder' to 'order'
    address = models.CharField(max_length=200, null=True)  # Corrected 'max_Length' to 'max_length'
    city = models.CharField(max_length=200, null=True)  # Corrected 'max_Length' to 'max_length'
    state = models.CharField(max_length=200, null=True)  # Corrected 'max_Length' to 'max_length'
    mobile = models.CharField(max_length=200, null=True)  # Corrected 'max_Length' to 'max_length'
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
