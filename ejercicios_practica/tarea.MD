![Inove banner](/inove.jpg)
Inove Escuela de Código\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

---
# Tarea: Django - DRF - Autenticación y Permisos

Al realizar esta tarea pondremos en práctica los conocimientos adquiridos en clase.
Una vez finalizada, el alumno debe subir el enlace a su repositorio "forkeado" el foro de tarea correspondiente -NO SE ADMITE LA DEVOLUCIÓN POR OTRO CANAL SALVO SE ESPECIFIQUE LO CONTRARIO- 

Recuerde que no debe subir la base de datos al sistema, para ello se encuentra el archivo .gitignore que especifica los archivos y directorios omitidos.

---


### 1. Utilizar el proyecto de "Marvel" visto en clase.
Inicializar el contenedor de docker, compilar la imagen del repositorio con:
**$** `docker-compose up` 


### 2. Realizar las migraciones del sistema.
Recuerde que para poder comenzar a utilizar el Django Admin, es necesario que el sistema se encuentre alineado con la base de datos. Para ello debemos realizar las migraciones de la aplicación y crear un nuevo superusuario.
Los comandos necesarios se encuentran detallados en el archivo README.md


### 3. Realice la class-based API view para el Login del usuario.
Basado en el material visto en clase, incluido en la carpeta "ejemplos_clase" desarrolle una API view basada en clase para el login del usuario.
La misma debe incluir la creación de un Token con su asignación al correspondiente usuario.
Requisitos:
  - Su correspondiente URL debe poseer el 'name' = 'login'.


### 4. Cree los serializadores.
Cree los serializadores tanto para el UserLogin como para el Token. 
Debe crear un serializador llamado UserLoginSerializer y otro llamado TokenSerializer, ambos dentro del archivo serializers.py

    UserLoginSerializer debe heredar de Serializer.
    Debe poder serializar y/o deserializar los campos 'username' y 'password'.

    TokenSerializer debe heredar de ModelSerializer.
    Debe poder serializar y/o deserializar los campos 'user' y 'token'.


### 5 Realizar las vistas de API (class-based) para el modelo WishList, con permisos determinados.
Debe realizar las siguientes vistas de API (class-based) necesarias para realizar el CRUD de la base de datos para la entidad "WishList". A dichas views, deberá asignarle los permisos aclarados a continuación, con las urls detalladas.
  -  GetWishListAPIView (GET) / endpoint: 'wishlist/<int:pk>/' / name: 'get_wishlist_api_view' / Permisos: IsAuthenticated - Autenticación: TokenAuthentication.
  -  PostWishListAPIView (POST) / endpoint: 'wishlist/create/' / name: 'post_wishlist_api_view' / Permisos: IsAuthenticated & IsAdminUser.
  -  UpdateWishListAPIView (UPDATE) / endpoint: 'wishlist/update/<int:pk>/' / name: 'update_wishlist_api_view' / Permisos: IsAuthenticated | IsAdminUser.
  -  DeleteWishListAPIView (DELETE) / endpoint: 'wishlist/delete/<int:pk>/' / name: 'delete_wishlist_api_view' / Permisos: IsAdminUser.

Recuerde utilizar el serializador creado la clase anterior.

 - **NOTA 1**: Tener en cuenta que para la actualización (*PUT/UPDATE*) se pide únicamente que permita actualizar los siguientes campos del modelo de forma **opcional o parcial** (esto significa que si uno de los campos no es enviado en el body de la request, el response no retorne o devuelva un error de validación indicando que falta determinado parámetro o campo):
   - **favorite**
   - **cart**
   - **wished_qty**
   - **bought_qty**

 Para eso puede seguir 2 posible flujos:
 1) Sobreescribir el método `.put()` de clase que va a realizar la actualización, en donde deberá llamar al serializador utilizado en dicha clase y pasarle como argumentos la **instancia**, la **data** (contiene los parámetros y sus valores enviados en la request), y, finalmente indicarle que se trata de una **actualización parcial**. Luego deberá validar dichos campos pasados, y, guardar la nueva instancia con los datos actualizados utilizando dicho serializador, proceso conocido como `deserialización`.
 Tome como ejemplo la vista: `UpdateComicAPIView`.

 2) Pruebe enviando una petición/request `PATCH`, en vez de tipo `PUT` y observe lo que sucede. Observe que DRF interpretó la petición y se resolvió de forma automática, sin necesidad de sobreescribir ningún método:
 - [método patch](https://www.cdrf.co/3.13/rest_framework.generics/UpdateAPIView.html#patch).
 - [método partial_update](https://www.cdrf.co/3.13/rest_framework.generics/UpdateAPIView.html#partial_update).

**NOTA 2**: Tanto para los endpoints de actualización y delete, deberá ingresar el id del comic como un parámetro estático, podrá acceder a dicho comic que desee actualizar o borrar. Ahora bien, ¿qué sucede si hay varios usuarios que tienen el mismo comic en el carritos de compras o en favoritos?, ¿se debería realizar una actualización de todos esos comics que están dentro de WishList?
  - Para solucionar este inconveniente, un camino podría ser que nos actualice sólo el comic (cuyo id pasamos por parámetro estático) del usuario que está authenticado. Para esto debemos sobreescribir además el método `.get_queryset()` y filtrar por el usuario en cuestión. Ahora bien, ¿cómo sabemos qué usuario está authenticado?, ¿se puede obtener la instancia del usuario authenticado? La respuesta es SI, y, DRF nos resuelve este problema. ¿Cómo? mediante la clase u objeto `request`. Entonces para obtener la instancia podemos hacer lo siguiente: `request.user` o `self.request.user`. Entonces dentro de nuestro método vamos a filtrar por user haciendo:
  ```queryset.filter(user=self.request.user)```. Una vez hecho esto simplemente el método `.get_object()` se va a encargar de buscar el comic que coincida con el id pasado por parámetro de ese usuario.


### 6. Instale Swagger para poder ver la documentación general de las APIs. 
Basandose en la documentación de clase y el ejemplo brindado en "ejemplo_clase" instale Swagger para poder ver la documentación de sus APIs.


## ¡Hora de evaluar nuestro código!
Puede evaluar que ha alcanzo los solicitado en el desafio ejecutando los tests que vienen dentro la carpeta ejercicios_practica dónde ha estando incoporando su código. Para eso debe realizar los siguientos:

1 - Abrir una consola dentro de la carpeta ejercicios_practica

2 - Lanzar el docker de ejercicios_practica (si es que está usando docker):\
**$** `docker-compose up`

3 - Abrir una nueva consola dentro de la carpeta ejercicios_practica

4 - Ingresar su consola dentro del contenedor con el siguiente comando (si es que está usando docker):\
**$** `docker exec -it modulo_4c_tp bash`

5 - Lance los tests con el siguiente comando:\
**$** `pytest -s`

---

## ¿Dudas?
Ante cualquier inquietud, debe referirse a los canales especificados para su trato en inove.
