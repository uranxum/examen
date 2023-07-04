from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout,authenticate,login as login_aut
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .Carrito import *
import requests
# Create your views here.
    
def cliente_check(user):
    return user.is_authenticated and user.groups.filter(name='clientes').exists()

def index(request):
    url = "http://worldtimeapi.org/api/timezone/America/Santiago"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hora_actual = data['datetime'].split('T')[1][:8]
    grupo = Group.objects.get(name="periodistas")
    usuarios = User.objects.filter(groups=grupo)
    categorias=Categoria.objects.all()
    noticias=Noticia.objects.filter(publicar=True).order_by("-idNoticia")[:3]
    contexto={'categorias':categorias, 'noticias':noticias,'usuarios':usuarios,'hora_actual':hora_actual}
    return render(request,"index.html", contexto)

def carrito(request):
    return render(request,"carrito.html")

def categoria(request):
    categorias=Categoria.objects.all()
    noticias=Noticia.objects.filter(publicar=True)
    contexto={'categorias':categorias,'noticias':noticias}
    return render(request,"categoria.html",contexto)

def contacto(request):
    categorias=Categoria.objects.all()
    contexto={'categorias':categorias}
    if request.POST:
        contacto = Contacto()

        nombre=request.POST.get("txtNombre")
        email=request.POST.get("txtEmail")
        titulo=request.POST.get("txtTitulo")
        texto=request.POST.get("txtTexto")
        contacto.nombre=nombre
        contacto.email=email
        contacto.titulo=titulo
        contacto.texto=texto
        contacto.save()
        messages.success(request, "Envio exitoso")
        contexto["mensaje"]="Grabo"
        return render(request,"contacto.html",contexto)
    return render(request,"contacto.html")

@login_required(login_url='/login/')
@permission_required('webCaos.add_noticia',login_url='/login/')
def formulario(request):
    categorias=Categoria.objects.all()
    contexto={'categorias':categorias}

    if request.POST:
        noticia = Noticia()

        titulo=request.POST.get("txtTitulo")
        fecha=request.POST.get("txtFecha")
        ubicacion=request.POST.get("txtUbicacion")
        encabezado=request.POST.get("txtEncabezado")
        cuerpo=request.POST.get("txtCuerpo")
        cate = request.POST.get("cboCategoria")
        foto = request.FILES.get("txtImg")
        obj_cate = Categoria.objects.get(nombre=cate)
        if request.user.is_authenticated:
            usuario=request.user
        noticia.titulo=titulo
        noticia.fecha=fecha
        noticia.ubicacion=ubicacion
        noticia.encabezado=encabezado
        noticia.cuerpo=cuerpo
        noticia.categoria=obj_cate
        noticia.usuario=usuario
        noticia.foto=foto
        noticia.save()
        messages.success(request, "Envio exitoso")
        contexto["mensaje"]="Grabo"
        return render(request,"formulario.html",contexto)

    return render(request,"formulario.html",contexto)

def galeria(request):
    categorias=Categoria.objects.all()
    noticias=Noticia.objects.filter(publicar=True)
    contar=noticias.count()
    contexto={'categorias':categorias,'noticias':noticias,'contar':contar}
    return render(request,"galeria.html",contexto)

def login(request):
    if request.POST:
        nombre=request.POST.get("txtUser")
        contraseña=request.POST.get("pwdPass")
        usuario=authenticate(request,username=nombre,password=contraseña)
        if usuario is not None and usuario.is_active:
            login_aut(request,usuario)
            return redirect('IND')
    contexto={'mensaje':'Usuario/contraseña incorrecto'}
    return render(request,"login.html", contexto)

@login_required(login_url='/login/')
@permission_required('webCaos.change_noticia',login_url='/login/')
def modificar(request,id):
    noticia=Noticia.objects.get(idNoticia=id)
    categorias=Categoria.objects.all()
    data={'noticia':noticia,'categorias':categorias}
    return render(request,"modificar.html", data)

@login_required(login_url='/login/')
@permission_required('webCaos.change_noticia',login_url='/login/')
def modificar_noticia(request):
    if request.POST:
        id=request.POST.get("txtId")
        titulo=request.POST.get("txtTitulo")
        fecha=request.POST.get("txtFecha")
        ubicacion=request.POST.get("txtUbicacion")
        encabezado=request.POST.get("txtEncabezado")
        cuerpo=request.POST.get("txtCuerpo")
        cate=request.POST.get("cboCategoria")
        foto=request.FILES.get("txtImg")
        obj_cate=Categoria.objects.get(nombre=cate)
        if request.user.is_authenticated:
            usuario=request.user

        noticia = Noticia.objects.get(idNoticia=id)
        noticia.titulo=titulo
        noticia.fecha=fecha
        noticia.ubicacion=ubicacion
        noticia.encabezado=encabezado
        noticia.cuerpo=cuerpo
        noticia.categoria=obj_cate
        noticia.usuario=usuario
        if foto is not None:
            noticia.foto=foto
        noticia.save()
    return redirect('/perfil_periodista/')

@login_required(login_url='/login/')
@permission_required('webCaos.add_galeria',login_url='/login/')
def grabar_galeria(request):
    if request.POST:
        id = request.POST.get("txtId")
        foto = request.FILES.get("txtFoto")
        noticia = Noticia.objects.get(idNoticia=id)
        gal= Galeria(
            foto = foto,
            noticia = noticia
        )
        gal.save()
    return redirect("/perfil_periodista/")

def noticia(request,id):
    categoria = Categoria.objects.all()
    grupo = Group.objects.get(name="periodistas")
    usuarios = User.objects.filter(groups=grupo)
    noticia=Noticia.objects.get(idNoticia=id)
    galeria=Galeria.objects.filter(noticia=noticia)
    data={'noticia':noticia,'usuarios':usuarios,'galeria':galeria,'categoria':categoria}
    return render(request,"noticia.html",data)

@login_required(login_url='/login/')
@permission_required(['webCaos.add_galeria','webCaos.view_galeria','webCaos.add_noticia','webCaos.change_noticia','webCaos.delete_noticia','webCaos.view_noticia'],login_url = '/login/')
def perfil_periodista(request):
    if request.user.is_authenticated:
        usuario=request.user
    categorias=Categoria.objects.all()
    noticias = Noticia.objects.filter(usuario=usuario, publicar=False)
    noticias2 = Noticia.objects.filter(usuario=usuario, publicar=True)
    contar = Noticia.objects.filter(usuario=usuario).count()
    contexto={'categorias':categorias,'noticias':noticias,'noticias2':noticias2,'cantidad':contar}
    return render(request,"perfil_periodista.html",contexto)

def periodista(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    categorias = Categoria.objects.all()
    noticias = Noticia.objects.filter(usuario=usuario, publicar=True)
    contar = noticias.count()
    contexto = {'categorias': categorias, 'noticias': noticias, 'cantidad': contar,'usuario':usuario}
    return render(request, "periodista.html", contexto)

@login_required(login_url='/login/')
@permission_required('auth.add_user',login_url='/login/')
def registro_periodista(request):
    categorias = Categoria.objects.all()
    contexto = {'categorias': categorias, 'mensaje': ''}
    
    if request.method == 'POST':
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        email = request.POST.get("txtEmail")
        password = request.POST.get("pwdPass1")
        password2 = request.POST.get("pwdPass2")
        
        if password == password2:
            try:
                usuario = User.objects.create_user(username=nombre, password=password, email=email, first_name=nombre, last_name=apellido)
                usuario.is_staff = True  
                usuario.save()
                grupo = Group.objects.get(name='periodistas')
                usuario.groups.add(grupo)
                messages.success(request, "Usuario registrado")
                contexto['mensaje'] = 'Usuario grabado'
                
            except:
                messages.error(request, "Error al registrar usuario")
                contexto['mensaje'] = 'Error al grabar'
                
        else:
            messages.error(request, "Las contraseñas no coinciden")
            contexto['mensaje'] = 'Las contraseñas no coinciden'
            
    return render(request, "registro_periodista.html", contexto)

def registro(request):
    categorias = Categoria.objects.all()
    contexto = {'categorias': categorias, 'mensaje': ''}
    
    if request.method == 'POST':
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        email = request.POST.get("txtEmail")
        password = request.POST.get("pwdPass1")
        password2 = request.POST.get("pwdPass2")
        
        if password == password2:
            try:
                usuario = User.objects.create_user(username=nombre, password=password, email=email, first_name=nombre, last_name=apellido)
                grupo = Group.objects.get(name='clientes')
                usuario.groups.add(grupo)
                messages.success(request, "Usuario registrado")
                contexto['mensaje'] = 'Usuario grabado'
                return redirect('LOG') 
                
            except:
                messages.error(request, "Error al registrar usuario")
                contexto['mensaje'] = 'Error al grabar'
                
        else:
            messages.error(request, "Las contraseñas no coinciden")
            contexto['mensaje'] = 'Las contraseñas no coinciden'
            
    return render(request,"registro.html",contexto)
    
@user_passes_test(cliente_check, login_url='/login/')
def tienda(request):
    articulos=Articulo.objects.all()
    contexto={'articulos':articulos}
    return render(request,"tienda.html",contexto)

@login_required(login_url='/login/')
@permission_required('webCaos.delete_noticia',login_url='/login/')
def eliminar(request,id):
    noticia=Noticia.objects.get(idNoticia=id)
    categorias=Categoria.objects.all()
    if request.user.is_authenticated:
        usuario=request.user
    noticias=Noticia.objects.filter(usuario=usuario)
    data={'categorias':categorias,'noticias':noticias}
    data['mensaje']=''
    try:
        noticia.delete()
        data["mensaje"]='elimino'
    except:
        data["mensaje"]='no elimino'
    return render(request,"perfil_periodista.html",data)

def filtro_categoria(request,id):
    cate=id
    categorias=Categoria.objects.all()
    obj_cate=Categoria.objects.get(nombre=cate)
    noticias=Noticia.objects.filter(categoria=obj_cate).filter(publicar=True)
    contar=Noticia.objects.filter(categoria=obj_cate).count()
    contexto={'noticias':noticias,'cantidad':contar,'categorias':categorias}
    return render(request,"categoria.html",contexto)

def filtro_contenido(request):
    categorias = Categoria.objects.all()
    contenido = request.POST.get("txtBuscar")
    noticias = Noticia.objects.filter(Q(titulo__icontains=contenido) | Q(encabezado__icontains=contenido), publicar=True)
    contar = noticias.count()
    contexto = {'noticias': noticias, 'cantidad': contar, 'categorias': categorias}
    return render(request, "galeria.html", contexto)

def filtro_periodista(request):
    categorias=Categoria.objects.all()
    user=request.POST.get("txtBuscar2")
    noticias=Noticia.objects.filter(usuario__contains=user).filter(publicar=True)
    contar=Noticia.objects.filter(usuario__contains=user).filter(publicar=True).count()
    contexto={'noticias':noticias,'cantidad':contar,'categorias':categorias}
    return render(request,"galeria.html",contexto)

def cerrar(request):
    logout(request)
    return redirect(to="IND")

def agregar_articulo(request, id_articulo):
    carrito = Carrito(request)
    articulo = Articulo.objects.get(idArticulo = id_articulo)
    carrito.agregar(articulo)
    return redirect('/carrito/')

def quitar_articulo(request, id_articulo):
    carrito = Carrito(request)
    articulo = Articulo.objects.get(idArticulo = id_articulo)
    carrito.quitar(articulo)
    return redirect('/carrito/')

def vaciar(request):
    carrito = Carrito(request)
    carrito.vaciar()
    return redirect('/carrito/')

def eliminar_arti(request,id_articulo):
    carrito = Carrito(request)    
    articulo = Articulo.objects.get(idArticulo = id_articulo)
    carrito.eliminar(articulo)
    return redirect('/carrito/')







