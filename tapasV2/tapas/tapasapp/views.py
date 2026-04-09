from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Account

# Used to show "Account created successfully" on the login page after signup
login_message = ""

def login(request):
    global login_message
    msg = login_message
    login_message = ""

    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        acc_qs = Account.objects.filter(username=u, password=p)
        if acc_qs:
            acc = acc_qs[0]
            return redirect('basic_list', pk=acc.pk)
        else:
            return render(request, "tapasapp/login.html", {"message": "Invalid login"})

    return render(request, "tapasapp/login.html", {"message": msg})

def signup(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        if Account.objects.filter(username=u):
            return render(request, "tapasapp/signup.html", {"message": "Account already exists"})
        else:
            Account.objects.create(username=u, password=p)

            global login_message
            login_message = "Account created successfully"
            return redirect('login')

    return render(request, "tapasapp/signup.html")

def basic_list(request, pk):
    dishes = Dish.objects.all()
    return render(request, "tapasapp/basic_list.html", {"pk": pk, "dishes": dishes})

def manage_account(request, pk):
    acc = get_object_or_404(Account, pk=pk)
    return render(request, "tapasapp/manage_account.html", {"acc": acc})

def change_password(request, pk):
    acc = get_object_or_404(Account, pk=pk)

    if request.method == "POST":
        current = request.POST.get("current_password")
        new1 = request.POST.get("new_password1")
        new2 = request.POST.get("new_password2")

        if current == acc.password and new1 == new2:
            Account.objects.filter(pk=pk).update(password=new1)
            return redirect('manage_account', pk=pk)
        else:
            return render(request, "tapasapp/change_password.html", {
                "acc": acc,
                "message": "Invalid password change"
            })

    return render(request, "tapasapp/change_password.html", {"acc": acc})

def delete_account(request, pk):
    Account.objects.filter(pk=pk).delete()
    return redirect('login')

def logout(request):
    return redirect('login')

# Existing dish pages
def better_menu(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes': dish_objects})


def add_menu(request):
    if request.method == "POST":
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')


def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})


def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')


def update_dish(request, pk):
    if request.method == "POST":
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d': d})