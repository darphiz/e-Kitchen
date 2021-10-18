from django.urls import path
from . import views


urlpatterns = [
        
        path('take_orders/', views.take_orders, name="take_orders"),
        path('fulfil_orders/<action>/<int:id>', views.fulfil_orders, name="fulfil_orders"),

]