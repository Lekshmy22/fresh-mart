"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("registration/",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("profile/<int:pk>/change/",views.UserProfileCreateView.as_view(),name="profile-update"),
    path("product/list/",views.ProductListView.as_view(),name="product-all"),
    path("product/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("category/<int:pk>/",views.CategoryProductListView.as_view(),name="category-product"),
    path("product/<int:pk>/cart/add/",views.AddToCartView.as_view(),name="add-cart"),
    path("cart/summary/",views.MyCartListView.as_view(),name="cart-summary"),
    path("cart/<int:pk>/remove",views.CartItemDeleteView.as_view(),name='cart-remove'),
    path("cart/<int:pk>/",views.QuantityUpdateView.as_view(),name='cart-update'),
    path("address/",views.AddressView.as_view(),name='address'),
    path("checkout/",views.CheckoutView.as_view(),name='checkout'),
    path('payment/verification/',views.PaymentVerificationView.as_view(),name='payment-verify'),
    path("order/summary/",views.MyPurchaseView.as_view(),name='order-summary'),
    path("product/<int:pk>/review/add/",views.ReviewCreateView.as_view(),name="review-add"),
    path('signout/',views.SignOutView.as_view(),name='signout'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
