![Inove banner](/inove.jpg)
Inove Escuela de Código\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

---
# Tarea: Django - REST FRAMEWORK 2

Al realizar esta tarea pondremos en práctica los conocimientos adquiridos en clase.
Una vez finalizada, el alumno debe subir el enlace a su repositorio "forkeado" el foro de tarea correspondiente -NO SE ADMITE LA DEVOLUCIÓN POR OTRO CANAL SALVO SE ESPECIFIQUE LO CONTRARIO- 

Recuerde que no debe subir la base de datos al sistema, para ello se encuentra el archivo .gitignore que especifica los archivos y directorios omitidos.

---

### 1. Implemente el serializador necesario para el modelo WishList.
Basado en el material visto en clase, incluido en la carpeta "ejemplos_clase" desarrolle el serializador necesario para el modelo WishList.
Para poder incluir los campos relacionados --> Foreign Keys, un camino podría ser utilizar el método 'serializers.PrimaryKeyRelatedField' por ejemplo:
    ```user = serializers.PrimaryKeyRelatedField(write_only=True,
                                                   queryset=User.objects.all())```
Luego el atributo debe ser incluido dentro de los 'fields', junto con el resto de los atributos del modelo.

### 2. Realizar las vistas de API.
Debe realizar todas las vistas de API necesarias para realizar el CRUD de la base de datos para la entidad "WishList". A continuación le dejamos los nombres de las vistas. Puede optar por ponerle otro nombre siempre y cuando sea representativo.
  -  GetWishListAPIView (GET)
  -  PostWishListAPIView (POST)
  -  UpdateWishListAPIView (UPDATE)
  -  DeleteWishListAPIView (DELETE)
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

Debe proporcionar protección de acceso a estas vistas de API, la que debe ser accesible **solo** si el usuario está autenticado. En el caso del listado (método GET) agregar además de estar autenticado debe ser administrador.

### 3. Asignar las URLs para las vistas de API.
Asigne las URLs para poder acceder a estas vistas, utilize los siguientes endpoints:
```
- `path('wish/get', GetWishListAPIView.as_view())`
- `path('wish/post', PostWishListAPIView.as_view())`
- `path('wish/{comic_id}/', UpdateWishListAPIView.as_view())`
- `path('wish/{comic_id}/', DeleteWishListAPIView.as_view())`
```

### 4. Realizar una API "mixta".
Realice una API mixta para consultar los comics favoritos de un usuario particular.
Para ello recomendamos sobrescribir el método `.get_queryset()` y realizar allí todas las consultas lógicas.
Utilice el siguiente endpoint y el siguiente nombre para la view:
    
 ``` 
 path('favs/<username>/get', GetUserFavsAPIView.as_view()), 
 ```

La lógica a seguir podría ser:
* Obtener el parametro 'username' del request
* Consultar al modelo 'User' si existe dicho usuario y obtener el objeto del modelo.
    * ``` user = User.objects.filter(username=username) ```
* Con dicho objeto, consultar en el modelo "WishList" por los comics que este usuario posee en favoritos. La consulta puede ser similar a:
    * ``` wish_list = WishList.objects.filter(user=user.first(), favorite=True) ```
* Ahora dispondrá de un queryset con los objetos del modelo "WishList" de dicho usuario que están en favoritos.
* El paso siguiente es obtener un queryset con los comics, podemos optar por 2 de los posibles caminos:
    1) Iterando cada objeto que hay dentro de **wish_list** e ir accediendo al *id* del comic. Por ejemplo:
           * ```comic_obj = Comic.objects.get(id=wish.comic_id)```
        (Notese que llamamos "wish" al objeto que está iterando ya que es solo un elemento de la lista "wish_list".) 

        * El paso siguiente es armar la lista de diccionarios de retorno en la view, como por ejemplo:
            ``` 
            
            [{
                    'id': 1
                    'marvel_id': '',
                    'title': '',
                    'description': '',
                    'price': 1.00,
                    'stock_qty': '',
                    'picture': '',
                },
                {
                    'id': 2
                    'marvel_id': '',
                    'title': '',
                    'description': '',
                    'price': 1.00,
                    'stock_qty': '',
                    'picture': '',
                },
                ...] 
            ```
    2) Hacer uso del serializador `ComicSerializer` para manejar la data que vamos a retornar sin necesidad de armar nosotros mismos la lista (camino recomendado).
        * Para eso necesitamos profundizar un poco más en el ORM de Django. La idea es realizar un queryset sobre el modelo *Comic* pero sin hacer uso de un bloque iterativo. A continuación se deja los links de las herramientas que provee para poder aplicarlas en este caso:
          *  [in](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#in)
          *  [Subquery](https://docs.djangoproject.com/en/3.2/ref/models/expressions/#limiting-a-subquery-to-a-single-column)
          *  [values](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#values) ó [values_list](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#values-list)
        * Queda en usted investigar y ver como asociarlos para poder obtener lo esperado. Ante cualquier duda se puede realizar las consultas necesarias.

* La API también debe solicitar **autenticación** para su uso.

* **NOTA**: No es la única manera de encarar esta lógica para dicha View, existen varias maneras mucho más eficientes y óptimas, pero consideramos que es un 1er paso para acercarse e ir entendiendo como funciona el ORM de Django. Si usted considera otra manera de encarar el ejercicio, puede utilizarlo siempre y cuando cumpla con lo especificado. En la clase siguiente veremos un poco más esto y como poder mejorar dicha lógica.

* **Preguntas y conclusiones que deberíamos plantearnos luego de realizar el punto anterior:**
  - ¿Qué sucede si un usuario tiene cientos de comics en favoritos?.
  - El scroll que debemos hacer para ir viendo cada uno de ellos ¿se vuelve bastante incómodo?.
  - ¿Es una mala **experiencia para el usuario**?.
  - ¿Cómo podríamos solucionar lo anterior?.
  - Una solución, ¿podría ser agregar **paginado** a la API?. ¿Favorece la experiencia de usuario? Habrán notado que hoy en día mucha de las aplicaciones trabajan con esto.
  - Y si quisiéramos buscar dentro de todos esos resultados algún comic en particular, ¿sería un agregado favorable?. Piensen que hoy en día estando dentro de una aplicación las búsquedas de algo particular dentro de muchos resultados nos ahorra tiempo.
  - **¿Cómo podríamos implementar todo lo anterior?. ¿Dónde agregaríamos esa lógica?**.

**IMPORTANTE**: Al descargar la colección y el Ambiente de Trabajo (Environment) que se encuentran en el Campus e importarla dentro de Postam van a poder probar sus APIs.

### 5. Instale Swagger para poder ver la documentación general de las APIs. 
Basandose en la documentación de clase y el ejemplo brindado en "ejemplo_clase" instale Swagger para poder ver la documentación de sus APIs.

---

## ¿Dudas?
Ante cualquier inquietud, debe referirse a los canales especificados para su trato en inove.