class Formulario{
    //atributos
    nombre;
    apellido;
    rut;
    email;
    telefono;
    fecha_nacimiento;
    password;
    //mutadores
    setNombre(nombre){
        this.nombre=nombre;
    }
    setApellido(ape){
        this.apellido=ape;
    }
    setRut(rut){
        this.rut=rut;
    }
    setEmail(email){
        this.email=email;
    }
    setTelefono(fono){
        this.telefono=fono;
    }
    setFechaNacimiento(fech){
        this.fecha_nacimiento=fech;
    }
    setPassword(pass){
        this.password=pass;
    }
    //accesadores
    getNombre(){return this.nombre;}
    getApellido(){ return this.apellido;}
    getRut(){ return this.rut;}
    getEmail(){ return this.email;}
    getTelefono(){ return this.telefono;}
    getFechaNacimiento(){ return this.fecha_nacimiento;}
    getPassword(){ return this.password;}
}