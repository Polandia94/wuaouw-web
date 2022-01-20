from pyexpat import model
from turtle import position
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView, View
from django.http import JsonResponse
from .elements import imagenbasejson
from wuaouw.models import *


def vistaInicial(request):
    context = {}
    return render(request,'index.html', context)

def imagenbase(request):
    return JsonResponse(imagenbasejson.json)

class Shop(ListView):
    model = Shop
    template_name = 'shop.html'

    def post(self, request, *args, **kwargs):
        data = []
        position=1
        for i in Shop.objects.all():
            item = i.toJSON()
            item['position'] = position
            imagen = ShopImagenes.objects.filter(id_shop=i).order_by("prioridad").first()
            if imagen is not None:
                item["imagenCabecera"] = imagen.ruta
            else:
                item["imagenCabecera"] = ""
            data.append(item)
            position += 1
        return JsonResponse(data, safe=False)

def future(request):
    context = {}
    return render(request,'future.html', context)

def vacancies(request):
    context = {}
    return render(request,'vacancies.html', context)


def cart(request):
    context = {}
    return render(request,'cart.html', context)
