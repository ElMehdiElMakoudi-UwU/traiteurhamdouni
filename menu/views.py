from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, Menu
from .forms import DishForm, MenuForm


# Dish Views
def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'menu/dish_list.html', {'dishes': dishes})


def create_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu:dish_list')
    else:
        form = DishForm()
    return render(request, 'menu/dish_form.html', {'form': form})


def edit_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('menu:dish_list')
    else:
        form = DishForm(instance=dish)
    return render(request, 'menu/dish_form.html', {'form': form})


def delete_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        dish.delete()
        return redirect('menu:dish_list')
    return render(request, 'menu/delete_confirmation.html', {
        'object': dish,
        'type': 'Dish',
        'redirect_url': 'menu:dish_list'  # Pass the URL name for redirection
    })



# Menu Views
def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'menu/menu_list.html', {'menus': menus})


def create_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu:menu_list')
    else:
        form = MenuForm()
    return render(request, 'menu/menu_form.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menu:menu_list')
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_form.html', {'form': form})

def delete_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        menu.delete()
        return redirect('menu:menu_list')
    return render(request, 'menu/delete_confirmation.html', {
        'object': menu,
        'type': 'Menu',
        'redirect_url': 'menu:menu_list'  # Pass the URL name for redirection
    })

