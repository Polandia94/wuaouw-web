from django.db import models, connection
from django.forms import model_to_dict

class Shop(models.Model):
    id_shop = models.AutoField(db_column='id_shop', primary_key=True)
    nombre = models.CharField(db_column='nombre', max_length=80)
    precio = models.IntegerField(db_column='precio')
    descripcion = models.CharField(db_column='descripcion', max_length=400)
    categoria = models.CharField(db_column='categoria', max_length=60)
    
    class Meta:
        app_label  = 'wuaow'
        managed = True
        db_table = 'shop'  # Para que en la migracion no ponga el prefijo de la app

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.nombre

class ShopImagenes(models.Model):
    id_shop_imagenes = models.AutoField(db_column='id_shop_imagenes', primary_key=True)
    id_shop = models.ForeignKey( 'shop', models.DO_NOTHING, db_column='id_shop')
    ruta = models.CharField(db_column='ruta', max_length=200)
    prioridad = models.IntegerField(db_column='prioridad')
    
    class Meta:
        app_label  = 'wuaow'
        managed = True
        db_table = 'shop_imagenes'  # Para que en la migracion no ponga el prefijo de la app

    def __str__(self):
        return Shop.objects.get(self.id_shop).nombre + " -  " +  str(self.prioridad)

class Valoracion(models.Model):
    id_valoracion = models.AutoField(db_column='id_valoracion', primary_key=True)
    id_shop = models.ForeignKey( 'shop', models.DO_NOTHING, db_column='id_shop')
    valoracion = models.CharField(db_column='ruta', max_length=500)
    estrellas = models.IntegerField(db_column='estrellas')
    
    class Meta:
        app_label  = 'wuaow'
        managed = True
        db_table = 'valoracion'  # Para que en la migracion no ponga el prefijo de la app

    def __str__(self):
        return Shop.objects.get(self.id_shop).nombre + " -  " +  str(self.id_valoracion)


class Ordenes(models.Model):
    id_orden = models.AutoField(db_column='id_orden', primary_key=True)
    transaccion = models.CharField(db_column='transaccion', max_length=60)
    direccion = models.CharField(db_column='direccion', max_length=300)
    telefono = models.CharField(db_column='telefono', max_length=25)
    email = models.CharField(db_column='email', max_length=50)
    nombre = models.CharField(db_column='nombre', max_length=50)
    apellido = models.CharField(db_column='apellido', max_length=50)
    pais = models.CharField(db_column='pais', max_length=50)
    provincia = models.CharField(db_column='provincia', max_length=50)
    precio = models.IntegerField(db_column='precio')
    
    class Meta:
        app_label  = 'wuaow'
        managed = True
        db_table = 'shop_ordenes'  # Para que en la migracion no ponga el prefijo de la app

    def __str__(self):
        return self.transaccion


class OrdenesProducto(models.Model):
    id_orden_producto = models.AutoField(db_column='id_orden_producto', primary_key=True)
    id_shop = models.IntegerField( 'shop')
    id_orden = models.IntegerField( 'shop_ordenes')
    cantidad = models.IntegerField(db_column='cantidad')
    
    class Meta:
        app_label  = 'wuaow'
        managed = True
        db_table = 'shop_ordenes_producto'  # Para que en la migracion no ponga el prefijo de la app

    def __str__(self):
        return Shop.objects.get(self.id_shop).nombre + " -  " +  str(self.cantidad)
