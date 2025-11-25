from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Plant, Comment, Country
from .forms import PlantForm

from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


def add_view(request:HttpRequest):
        
    if not request.user.is_staff:
        messages.success(request, "only staff can add game", "alert-warning")
        return redirect("main:home_view")

    try:
        plant_form = PlantForm()
        countries = Country.objects.all().order_by('name')
        if request.method == "POST":
            plant_form = PlantForm(request.POST, request.FILES)
            if plant_form.is_valid():
                plant_form.save()
                messages.success(request, "Plant added successfully", "alert-success")
                return redirect('main:home_view')
            return render(request, 'plants/add_plant.html', {'form':plant_form})
    except Exception as e:
        print(e)
        messages.error(request, "Can't add plant right now, please try again later", "alert-danger")

    return render(request, 'plants/add_plant.html', {"countries":countries})

def plant_detail_view(request:HttpRequest, plant_id:int):
    
    plant = Plant.objects.get(pk=plant_id)
    comments = Comment.objects.filter(plant=plant)


    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:6]
    
    context = {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments

    }
    
    return render(request, 'plants/plant_details.html', context)

def update_view(request: HttpRequest, plant_id: int):

    if not request.user.is_staff:
        messages.warning(request, "only staff can add game", "alert-warning")
        return redirect("main:home_view")

    try:
        plant = Plant.objects.get(pk=plant_id)
        countries = Country.objects.all().order_by('name')
        if request.method == "POST":
            plant_form = PlantForm(request.POST, request.FILES, instance=plant)
            if plant_form.is_valid():
                plant_instance = plant_form.save()
                selected_countries = request.POST.getlist('countries')
                plant_instance.countries.set(selected_countries)
                messages.success(request, "Plant updated successfully", "alert-success")
                return redirect('plants:plant_detail_view', plant_id=plant.id)
            return render(request, 'plants/update_plant.html', {'form': plant_form, 'plant': plant, 'countries': countries})
    except Exception as e:
        print(e)
        messages.error(request, "Can't update plant right now, please try again later", "alert-danger")
    
    plant_form = PlantForm(instance=plant)
    return render(request, 'plants/update_plant.html', {'form': plant_form, 'plant': plant, 'countries': countries})

def search_view(request: HttpRequest):
    query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '')
    
    plants = Plant.objects.all()

    if query:
        plants = plants.filter(name__icontains=query)

    if order_by == "edible":
        plants = plants.filter(is_edible=True)
    elif order_by == "non_edible":
        plants = plants.filter(is_edible=False)
    elif order_by == "trees":
        plants = plants.filter(category="Trees")
    elif order_by == "fruits":
        plants = plants.filter(category="Fruits")
    elif order_by == "vegetables":
        plants = plants.filter(category="Vegetables")
    elif order_by == "flowers":
        plants = plants.filter(category="Flowers")
    elif order_by == "herbs":
        plants = plants.filter(category="Herbs")
    elif order_by == "succulents":
        plants = plants.filter(category="Succulents")
    
    context = {
        'plants': plants,
        'query': query,
        'order_by': order_by,
    }
    return render(request, 'plants/search_plant.html', context)

def all_view(request:HttpRequest):
    plants = Plant.objects.all().order_by("-created_at")
    countries = Country.objects.all()
    
    country_filter = request.GET.get('country', '')
    if country_filter:
        plants = plants.filter(countries__id=country_filter)

    page_number = request.GET.get("page", 1)
    paginator = Paginator(plants,6)
    plants_page = paginator.get_page(page_number)


    return render(request, 'plants/all_plants.html', {'plants':plants_page, 'countries':countries, 'country_filter':country_filter })

def delete_view(request:HttpRequest, plant_id):

    if not request.user.is_staff:
        messages.warning(request, "only staff can add game", "alert-warning")
        return redirect("main:home_view")
    
    try:
        plant = Plant.objects.get(pk=plant_id)
        plant.delete()
        messages.success(request, "Plant deleted successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Can't delete plant right now, please try again later", "alert-danger")

    return redirect("main:home_view")

def add_comment_view(request:HttpRequest, plant_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered user can add review","alert-danger")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        plant_object = Plant.objects.get(pk=plant_id)
        new_comment= Comment(plant=plant_object, user = request.user, comment = request.POST["comment"])
        new_comment.save()
        messages.success(request, "Comment added successfully", "alert-success")
    return redirect("plants:plant_detail_view", plant_id=plant_id)

def plants_by_country(request:HttpRequest, country_id:int):

    country = Country.objects.get(pk=country_id)
    plants = country.plant_set.all()

    return render(request, 'plants/plants_by_country.html', {'country':country, 'plants':plants})