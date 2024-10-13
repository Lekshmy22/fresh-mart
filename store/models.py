from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator,MinValueValidator

from django.db.models import Sum,Avg


class UserProfile(models.Model):

    bio=models.CharField(max_length=200)

    profile_pic=models.ImageField(upload_to="profile_pictures",default="/profile_pictures/default.png")

    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")  #related_name="profile-->request.user.profile (to get user=user profile)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.user_object.username
    

class Category(models.Model):

    name= models.CharField(max_length=200)

    description=models.TextField(null=True)

    image=models.ImageField(upload_to="category_images",default="/category_images/default.png")

    def __str__(self):

        return self.name
      

class Product(models.Model):

    category_object=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='Categories')

    product_image=models.ImageField(upload_to="product_images",default="/product_images/default.png")

    title=models.CharField(max_length=200)

    description=models.TextField(null=True)

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="prducts")

    price=models.PositiveIntegerField(null=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def review_count(self):

        return self.product_reviews.all().count()
    
    @property
    def average_rating(self):

        return self.product_reviews.all().values('rating').aggregate(avg=Avg('rating')).get('avg',0)

    def __str__(self) -> str:

        return self.title
    
    

class Cart(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)
    
    @property
    def cart_total(self):

        return self.basket_items.filter(is_order_placed=False).values("updated_price").aggregate(total=Sum("updated_price")).get("total")
    
    


class CartItems(models.Model):

    cart_object=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="basket_items")

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)

    quantity= models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(20)])

    updated_price=models.PositiveIntegerField(null=True)

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class Ordersummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    product_objects=models.ManyToManyField(Product)

    order_id=models.CharField(max_length=200,null=True)

    payment_options=(
        ("cash","cash"),
        ("upi","upi")
    )

    payment_method=models.CharField(max_length=200,choices=payment_options,default="cash")

    name=models.CharField(max_length=200,null=True)

    address=models.CharField(max_length=200,null=True)

    pincode=models.CharField(max_length=6,null=True)

    phone=models.CharField(max_length=20,null=True,unique=True)

    is_paid=models.BooleanField(default=False)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    total=models.FloatField(null=True)

    

class Reviews(models.Model):

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_reviews')

    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    comment=models.TextField(null=True)

    rating=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)],null=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

#signals
#creating basket for a user

from django.db.models.signals import post_save

def create_basket(sender,instance,created,*args,**kwargs):

    if created:

        Cart.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_basket)

def create_profile(sender,instance,created,*args,**kwargs):

    if created:

        UserProfile.objects.create(user_object=instance)

post_save.connect(sender=User,receiver=create_profile)

