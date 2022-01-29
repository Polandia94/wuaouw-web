from pyexpat import model
from turtle import position
from unittest import result
from urllib.request import ProxyDigestAuthHandler
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView, View
from django.http import JsonResponse
from .elements import imagenbasejson
from wuaow.models import *
from django.db.models import Q


def vistaInicial(request):
    context = {"homeIsActive":"active"}
    return render(request,'index.html', context)

def imagenbase(request):
    return JsonResponse(imagenbasejson.json)

def token(request):
    context = {"tokenIsActive":"active"}
    return render(request,'token.html', context)

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
    context = {"vacanciesIsActive": "active"}
    return render(request,'vacancies.html', context)


def cart(request):
    try:
        productos = {}
        carrito = request.GET.get("carrito")
        carrito = carrito.split(",")
        for element in carrito:
            if element not in productos:
                productos[element] = 1
            else:
                productos[element] = productos[element] +1
        context = {'listado' : []}
        total = 0
        for element in productos:
            producto = Shop.objects.get(id_shop=int(element))
            imagen = ShopImagenes.objects.filter(id_shop=producto).order_by("prioridad").first()
            if imagen is not None:
                ruta = imagen.ruta
            else:
                ruta = ""
            total = total + (producto.precio/100)*productos[element]
            context['listado'].append({"nombre" :producto.nombre, "cantidad": productos[element], "imagen":ruta,"precio": producto.precio/100, "subtotal": (producto.precio/100)*productos[element]})
        context["total"]= total
        print(context)
        return render(request,'cart.html', context)
    except Exception as e:
        print(e)
        return redirect("/")

def product(request):
    id = request.GET.get('id')
    resultado = Shop.objects.get(id_shop=id)
    producto = resultado.toJSON()
    producto['precioDividido'] = producto['precio']/100
    imagenes = []
    for i in ShopImagenes.objects.filter(id_shop=id).order_by("prioridad"):
        imagenes.append(i.ruta)
    context = {"producto":producto, "imagenes":imagenes, "id_shop":id}
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

def confirmarCompra(request):
    print(request.POST)
    productos = {}
    carrito = request.POST.get("productos")
    if carrito == None:
        carrito = request.POST.get("productos[]")
    value = request.POST.get("value")
    carrito = carrito.split(",")
    for element in carrito:
        if element not in productos:
            productos[element] = 1
        else:

            productos[element] = productos[element] +1
    total = 0
    for element in productos:
        producto = Shop.objects.get(id_shop=int(element))
        total = total + (producto.precio/100)*productos[element]
    if total < float(value)/(10**18):
        orden = Ordenes(transaccion=request.POST.get("tx"), precio=int(float(value)/(10**16)), direccion=request.POST.get("direccion"), pais=request.POST.get("pais"), provincia=request.POST.get("provincia"), telefono=request.POST.get("telefono"), email=request.POST.get("email"),nombre = request.POST.get("nombre"), apellido=request.POST.get("apellido"))
        orden.save()
        for element in productos:
            ordenesProducto = OrdenesProducto(id_orden=orden.id_orden, id_shop=int(element), cantidad=productos[element])
            ordenesProducto.save()
        return JsonResponse({"result": "Compra Correcta", "correcto": "ok"})
    else:
        return JsonResponse({"result": "Monto Incorrecto", "correcto": "mal"})
