from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre=models.CharField(primary_key=True,max_length=20)
    foto=models.ImageField(upload_to='foto',null=True)

    def __str__(self) -> str:
        return self.nombre 

class Noticia(models.Model):
    idNoticia=models.AutoField(primary_key=True)
    titulo=models.CharField(max_length=100)
    fecha=models.DateField()
    ubicacion=models.TextField()
    encabezado=models.TextField()
    cuerpo=models.TextField()
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    foto=models.ImageField(upload_to='foto',default='foto/descargar.jpg')
    usuario=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    publicar=models.BooleanField(default=False)
    comentario=models.TextField(default='Sin comentarios')

    def __str__(self) -> str:
        return self.titulo

class Galeria(models.Model):
    idGaleria = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to='foto')
    noticia=models.ForeignKey(Noticia,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "N°"+str(self.idGaleria)+" / "+self.noticia.titulo

class Articulo(models.Model):
    idArticulo = models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=20)
    foto=models.ImageField(upload_to='foto',null=True)
    precio=models.IntegerField()

    def __str__(self) -> str:
        return self.nombre

class Contacto(models.Model):
    idContacto=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    titulo=models.CharField(max_length=100)
    texto=models.TextField()

    def __str__(self) -> str:
        return self.nombre