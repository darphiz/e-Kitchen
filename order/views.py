from django.shortcuts import render, redirect,get_object_or_404
from .models import Order
from .forms import OrderForm
from .utils import generate_order_code

def take_orders(request):
    counter= False
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=True)
            form.order_code = generate_order_code()
            form.taken_by = request.user
            form.save()
            return redirect('dashboard', action='counter')
        else:
            counter= True
            form = OrderForm()

    else:
        counter= True
        form = OrderForm()
    return render(request,'dashboard.html',{'form':form ,'counter':counter})
          

def fulfil_orders(request, action,id):
    order = get_object_or_404(Order,id=id)
    if action == "fulfil":
        order.status = "completed"
        order.fulfilled_by = request.user
        order.save()
    else:
        pass
    return redirect('dashboard', action='kitchen') 