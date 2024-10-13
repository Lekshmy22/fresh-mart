from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect

from django.urls import reverse_lazy

# Create your views here.
from store.forms import SignUpForm,SignInForm,UserProfileForm,DelivaryaddressForm,ReviewForm

from django.contrib import messages

from django.views.generic import View,TemplateView,UpdateView,CreateView,DetailView,FormView

from django.contrib.auth import authenticate,login,logout

from store.models import UserProfile,Product,Category,CartItems,Ordersummary

from store.decorators import signin_required

from django.utils.decorators import method_decorator

from decouple import config

KEY_ID = config('KEY_ID')

KEY_SECRET = config('KEY_SECRET')


class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,'store/signup.html',{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"account created successfully")

            return redirect('signin')
            
        else:

            messages.error(request,'failed to create account')

            return render(request,'store/signup.html',{"form":form_instance})
        
        
class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"store/login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            user_object=authenticate(request,**data)

            if user_object:

                login(request,user_object)

                messages.success(request,"login successfully")

                return redirect("index")
            
        messages.error(request,"failed to login")

        return render(request,"store/login.html",{"form":form_instance})


# listing products and categories========>
class IndexView(View):

    template_name="store/index.html"

    def get(self,request,*args,**kwargs):

        qs=Category.objects.all()

        products=Product.objects.all()

        return render(request,self.template_name,{"categories":qs,"products":products})
    

# ======user profile created using signals.its updates the user profile=====>
class UserProfileCreateView(UpdateView):

    model=UserProfile

    form_class=UserProfileForm

    template_name="store/profile_edit.html"

    # success url using for only create and update functions

    success_url=reverse_lazy("index") #reverse_lazy ensure that when the success page is generated



    # def get(self,request,*args,**kwargs):

    #     id=kwargs.get("pk")

    #     profile_obj=UserProfile.objects.get(id=id)

    #     form_instance=UserProfileForm(instance=profile_obj)

    #     return render(request,"store/profile_edit.html",{"form":form_instance})


# =====all products listing page=====

class ProductListView(View):

    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        return render(request,"store/product_list.html",{"products":qs})
    
    
# =======specific product details will be displayed====

class ProductDetailView(DetailView):

    template_name="store/product_detail.html"

    model=Product

    # query key passing to the template ({"product":qs})====denoting context_object_name

    context_object_name="product"


# filtering products based on the category id======
class CategoryProductListView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Product.objects.filter(category_object=id)

        return render(request,"store/category_product.html",{"product":qs})
    
    
@method_decorator(signin_required,name="dispatch")
class AddToCartView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Product_obj=Product.objects.get(id=id)


        CartItems.objects.create(
                                  cart_object=request.user.basket,
                                  product_object=Product_obj,
                                  category_object=Product_obj.category_object,
                                  updated_price=Product_obj.price
        )
        
        print("item has been added to cart")

        return redirect("index")
    

@method_decorator(signin_required,name="dispatch")
class MyCartListView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_items.filter(is_order_placed=False)

        total=request.user.basket.cart_total

        return render(request,"store/cartitems_summary.html",{"cartitems":qs,"total":total})


@method_decorator(signin_required,name="dispatch")
class CartItemDeleteView(View):
    
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        CartItems.objects.get(id=id).delete()

        return redirect("cart-summary")
    
    
    
@method_decorator(signin_required,name="dispatch")
class QuantityUpdateView(FormView):

    def post(self,request,*args,**kwargs):

        cart_id=kwargs.get("pk")

        cart_obj=CartItems.objects.get(id=cart_id)

        product_obj=Product.objects.get(id=cart_obj.product_object_id)

        update_type=request.POST.get('update')

        current_quantity=cart_obj.quantity

        current_price=cart_obj.product_object.price

        if update_type =='increase':

            cart_obj.quantity=current_quantity + 1


        elif update_type =='decrease' and current_quantity >1:

            cart_obj.quantity =current_quantity - 1

        # Product_obj.price=current_price * cart_obj.quantity

        cart_obj.updated_price=current_price * cart_obj.quantity

        cart_obj.save()

        # context={'updated_price':updated_price,'cart_obj':cart_obj,'product_obj':Product_obj}

        # return render(request,"store/cartitems_summary.html",context)

        return redirect("cart-summary")
    
@method_decorator(signin_required,name="dispatch")
class AddressView(CreateView):



    # def get(self,request,*args,**kwargs):

    #     form_instance=DelivaryaddressForm()

    #     qs=request.user.orders.all()

    #     return render(request,'store/address.html',{"form":form_instance,"address":qs})
    
    # def post(self,request,*args,**kwargs):

    #     form_instance=DelivaryaddressForm(request.POST)

    #     if form_instance.is_valid():

    #         form_instance.instance.user_object=request.user

    #         form_instance.save()

    #         return redirect('checkout')
    #     else:
    #         return render(request,'store/address.html',{"form":form_instance})


    def get(self,request,*args,**kwargs):

        form_instance=DelivaryaddressForm()

        return render(request,"store/address.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        Cart_Items=request.user.basket.basket_items.filter(is_order_placed=False)

        form_instance= DelivaryaddressForm(request.POST)    

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            order_summary_obj=Ordersummary.objects.create(user_object=request.user,total=request.user.basket.cart_total,**data)

        for ci in Cart_Items:

            order_summary_obj.product_objects.add(ci.product_object)

            order_summary_obj.save()

        if order_summary_obj.payment_method =='cash':

            for ci in Cart_Items:

                ci.is_order_placed=True

                ci.save()
                
            return redirect('order-summary')
            
        else:

            return redirect('checkout')


import razorpay

@method_decorator(signin_required,name="dispatch")
class CheckoutView(View):

    def get(self,request,*args,**kwargs):

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        amount=request.user.basket.cart_total*100

        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        Ordersummary.objects.filter(user_object=request.user,payment_method='upi',order_id__isnull=True).update(order_id=payment.get("id"))

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

        for ci in cart_items:

            ci.is_order_placed=True

            ci.save()


        context={
            "key":KEY_ID,
            "amount":data.get("amount"),
            "currency":data.get("currency"),
            "order_id":payment.get("id")
        }

        print(payment)

        # return redirect("index")

        return render(request,"store/payment.html",context)
    

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt,name='dispatch')    
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        client = razorpay.Client(auth=(KEY_ID,KEY_SECRET ))

        order_summary_object=Ordersummary.objects.get(order_id=request.POST.get("razorpay_order_id"))

        login(request,order_summary_object.user_object)

        try:
            # doubtfull code
            client.utility.verify_payment_signature(request.POST)

            print("payment success")

            order_id=request.POST.get("razorpay_order_id")

            Ordersummary.objects.filter(order_id=order_id).update(is_paid=True)

            cart_items= request.user.basket.basket_items.filter(is_order_placed=False)

            for ci in cart_items:
                
                ci.is_order_placed=True

                ci.save()

        except:

            # handling code
            print("payment failed")

        # return render(request,"store/success.html")

        return redirect("order-summary")

@method_decorator(signin_required,name="dispatch")
class MyPurchaseView(View):

    model=Ordersummary

    context_object_name="orders"

    def get(self,request,*args,**kwargs):

        qs=Ordersummary.objects.filter(user_object=request.user,is_paid=True).order_by('-created_date')

        cod=Ordersummary.objects.filter(user_object=request.user,payment_method='cash')

        return render(request,"store/order_summary.html",{"orders":qs,"cod":cod})
    

    
#url  localhost8000/project/<int:pk>/review/add/

@method_decorator(signin_required,name="dispatch")
class ReviewCreateView(FormView):

    template_name="store/review.html"

    form_class=ReviewForm

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        form_instance=ReviewForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object=(request.user)

            form_instance.instance.product_object=product_obj

            form_instance.save()

            return redirect('index')
        
        else:

            return render(request,self.template_name,{"form":form_instance})
        

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")


        





        


    









        
        






    




        



    


        




