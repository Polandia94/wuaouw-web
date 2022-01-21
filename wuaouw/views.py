from pyexpat import model
from turtle import position
from unittest import result
from urllib.request import ProxyDigestAuthHandler
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView, View
from django.http import JsonResponse
from .elements import imagenbasejson
from wuaouw.models import *
from django.db.models import Q


def vistaInicial(request):
    context = {"homeIsActive":"active"}
    return render(request,'index.html', context)

def imagenbase(request):
    return JsonResponse(imagenbasejson.json)

def shop(request):
    context = {"shopIsActive":"active"}
    data = []
    position=1
    for i in Shop.objects.all():
        item = i.toJSON()
        print(item)
        item['position'] = position
        print(item['precio'])
        item['precioDividido'] = item['precio']/100
        imagen = ShopImagenes.objects.filter(id_shop=i).order_by("prioridad").first()
        if imagen is not None:
            item["imagenCabecera"] = imagen.ruta
        else:
            item["imagenCabecera"] = ""
        data.append(item)
        position += 1
    context["products"] = data
    return render(request,'shop.html', context)

def future(request):
    context = {"futureIsActive": "active"}
    return render(request,'future.html', context)

def vacancies(request):
    
    context = {}
    return render(request,'vacancies.html', context)


def cart(request):
    productos = {}
    carrito = request.GET.get("carrito")
    carrito = carrito.split(",")
    for element in carrito:
        if element not in productos:
            productos[element] = 1
        else:
            productos[element] = productos[element] +1
    context = {'listado' : []}

    for element in productos:
        producto = Shop.objects.get(id_shop=int(element))
        imagen = ShopImagenes.objects.filter(id_shop=producto).order_by("prioridad").first()
        if imagen is not None:
            ruta = imagen.ruta
        else:
            ruta = ""
        context['listado'].append({"nombre" :producto.nombre, "cantidad": productos[element], "imagen":ruta,"precio": producto.precio/100, "subtotal": (producto.precio/100)*productos[element]})
    print(context)
    return render(request,'cart.html', context)

def product(request):
    id = request.GET.get('id')
    resultado = Shop.objects.get(id_shop=id)
    producto = resultado.toJSON()
    producto['precioDividido'] = producto['precio']/100
    imagenes = []
    for i in ShopImagenes.objects.filter(id_shop=id).order_by("prioridad"):
        imagenes.append(i.ruta)
    context = {"producto":producto, "imagenes":imagenes}
    print(context)
    return render(request,'product.html', context)


def search(request):
    context = {"shopIsActive":"active"}
    data = []
    position=1
    print(request.GET.get("busqueda"))
    resultado = False
    for i in Shop.objects.filter(Q(nombre__icontains = request.GET.get("busqueda")) | Q(descripcion__icontains = request.GET.get("busqueda"))):
        resultado = True
        item = i.toJSON()
        print(item)
        item['position'] = position
        print(item['precio'])
        item['precioDividido'] = item['precio']/100
        imagen = ShopImagenes.objects.filter(id_shop=i).order_by("prioridad").first()
        if imagen is not None:
            item["imagenCabecera"] = imagen.ruta
        else:
            item["imagenCabecera"] = ""
        data.append(item)
        position += 1
    context["products"] = data
    context["busqueda"] = request.GET.get("busqueda")
    if resultado == False:
        context = {"shopIsActive":"active"}
        data = []
        position=1
        for i in Shop.objects.all():
            item = i.toJSON()
            print(item)
            item['position'] = position
            print(item['precio'])
            item['precioDividido'] = item['precio']/100
            imagen = ShopImagenes.objects.filter(id_shop=i).order_by("prioridad").first()
            if imagen is not None:
                item["imagenCabecera"] = imagen.ruta
            else:
                item["imagenCabecera"] = ""
            data.append(item)
            position += 1
        context["products"] = data
        context["error"] = "La Busqueda No arrojó Resultados"

    return render(request,'shop.html', context)
