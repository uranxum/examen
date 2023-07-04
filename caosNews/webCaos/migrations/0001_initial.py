# Generated by Django 4.2.2 on 2023-06-29 00:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('idArticulo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
                ('foto', models.ImageField(null=True, upload_to='foto')),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('foto', models.ImageField(null=True, upload_to='foto')),
            ],
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('idContacto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('titulo', models.CharField(max_length=100)),
                ('texto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('idNoticia', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('ubicacion', models.TextField()),
                ('encabezado', models.TextField()),
                ('cuerpo', models.TextField()),
                ('foto', models.ImageField(default='foto/descargar.jpg', upload_to='foto')),
                ('publicar', models.BooleanField(default=False)),
                ('comentario', models.TextField(default='Sin comentarios')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webCaos.categoria')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('idGaleria', models.AutoField(primary_key=True, serialize=False)),
                ('foto', models.ImageField(upload_to='foto')),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webCaos.noticia')),
            ],
        ),
    ]
