class Carrito:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"]={}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
    
    def agregar(self, articulo):
        id = str(articulo.idArticulo)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "id":articulo.idArticulo,
                "nombre":articulo.nombre,
                "precio":articulo.precio,
                "cantidad":1,
                "total":articulo.precio,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["total"] += articulo.precio
        self.actualizar()
    
    def quitar(self, articulo):
        id = str(articulo.idArticulo)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["total"] -= articulo.precio
            if self.carrito[id]["cantidad"] == 0:
                self.eliminar(articulo)
            self.actualizar()

    def eliminar(self,articulo):
        id = str(articulo.idArticulo)
        if id in self.carrito.keys():
            del self.carrito[id]
            self.actualizar()

    def actualizar(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def vaciar(self):        
        self.session["carrito"] = {}
        self.session.modified = True
