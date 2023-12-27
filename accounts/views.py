from django.shortcuts import render
from .decorators import *
from .forms import *
from .filters import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


@unauthenticadeUser
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            for _ in messages.get_messages(request):
                pass

            messages.info(request, "Username or password is incorrect")
            context = {}
            return render(request, 'accounts/login.html', context)

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@unauthenticadeUser
def register(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == "POST":
        formSubmmited = CreateUserForm(request.POST)

        if formSubmmited.is_valid():
            user = formSubmmited.save()

            group = Group.objects.get(name="customer")
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

            for _ in messages.get_messages(request):
                pass

            messages.success(request, "Account succesfuly created!")

            return redirect('login')

    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'totalOrders': totalOrders,
               'delivered': delivered, 'pending': pending}

    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'totalOrders': totalOrders,
               'delivered': delivered, 'pending': pending}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettingPage(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        formSubmmited = CustomerForm(request.POST, request.FILES, instance=customer)

        if formSubmmited.is_valid():
            formSubmmited.save()

    context = {'form': form}

    return render(request, 'accounts/accountSettings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    productsQuery = Products.objects.all()
    return render(request, 'accounts/products.html', {'products': productsQuery})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    totalOrders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'totalOrders': totalOrders, 'myFilter': myFilter}

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()

    if request.method == "POST":
        formSubmitted = OrderForm(request.POST)

        for _ in messages.get_messages(request):
            pass

        if formSubmitted.is_valid():
            formSubmitted.save()

            messages.success(request, "Order creation was succesful!")

            return redirect('/')

        else:
            messages.error(request, "Order creation failed")

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/orderForm.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        formSubmitted = OrderForm(request.POST, instance=order)

        if formSubmitted.is_valid():
            formSubmitted.save()

            messages.success(request, "Order was update succesfully!")

            return redirect('/')

        else:
            messages.error(request, "Unfortunely the order could not be updated")

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/orderForm.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    item = {"id": order.id,
            "text": f"{order.product.name} bought by {order.customer.name} at {order.dateCreated}, wich is {order.status}"}

    if request.method == "POST":
        order.delete()

        messages.success(request, "Order was deleted succesfully!")

        return redirect('/')

    context = {'item': item}

    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CustomerForm()

    if request.method == "POST":
        formSubmitted = CustomerForm(request.POST)

        if formSubmitted.is_valid():
            formSubmitted.save()

            messages.success(request, "Customer creation was succesful!")

            return redirect('/')

        else:
            messages.error(request, "Customer creation failed")

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/orderForm.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(pk=pk)
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        formSubmitted = CustomerForm(request.POST, instance=customer)

        if formSubmitted.is_valid():
            formSubmitted.save()

            messages.success(request, "Customer was update succesfully!")

            return redirect('/')

        else:
            messages.error(request, "Unfortunely the customer could not be updated")

            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/orderForm.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(pk=pk)
    item = {"id": customer.id,
            "text": f"{customer.name}, created {customer.dateCreated}"}

    if request.method == "POST":
        customer.delete()

        messages.success(request, "Order was deleted succesfully!")

        return redirect('/')

    context = {'item': item}

    return render(request, 'accounts/deleteCustomer.html', context)
