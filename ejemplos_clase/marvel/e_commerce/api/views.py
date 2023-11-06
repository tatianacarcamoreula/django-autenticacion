from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
# (GET - ListAPIView) Listar todos los elementos en la entidad:
# (POST - CreateAPIView) Inserta elementos en la DB
# (GET - RetrieveAPIView) Devuelve un solo elemento de la entidad.
# (GET-POST - ListCreateAPIView) Para listar o insertar elementos en la DB
# (GET-PUT - RetrieveUpdateAPIView) Devuelve o actualiza un elemento en particular.
# (DELETE - DestroyAPIView) Permite eliminar un elemento.
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    GenericAPIView,
    UpdateAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

# NOTE: Importamos este decorador para poder customizar los 
# parámetros y responses en Swagger, para aquellas
# vistas de API basadas en funciones y basadas en Clases 
# que no tengan definido por defecto los métodos HTTP.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from e_commerce.api.serializers import *
from e_commerce.models import Comic


mensaje_headder = '''
Class API View

```
headers = {
  'Authorization': 'Token 92937874f377a1ea17f7637ee07208622e5cb5e6',
  
  'actions': 'GET', 'POST', 'PUT', 'PATCH', 'DELETE',
  
  'Content-Type': 'application/json',
  
  'Cookie': 'csrftoken=cfEuCX6qThpN6UC9eXypC71j6A4KJQagRSojPnqXfZjN5wJg09hXXQKCU8VflLDR'
}
```
'''

@api_view(http_method_names=['GET'])
def comic_list_api_view(request):
    _queryset = Comic.objects.all()
    _data = list(_queryset.values()) if _queryset.exists() else []
    return Response(data=_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def comic_retrieve_api_view(request):
    instance = get_object_or_404(
        Comic, id=request.query_params.get('id')
    )
    return Response(
        data=model_to_dict(instance), status=status.HTTP_200_OK
    )


@api_view(http_method_names=['POST'])
def comic_create_api_view(request):
    _marvel_id = request.data.pop('marvel_id', None)
    print(request.data)
    if not _marvel_id:
        raise ValidationError(
            {"marvel_id": "Este campo no puede ser nulo."}
        )
    _instance, _created = Comic.objects.get_or_create(
        marvel_id=_marvel_id,
        defaults=request.data
    )
    if _created:
        return Response(
            data=model_to_dict(_instance), status=status.HTTP_201_CREATED
        )
    return Response(
        data={
            "marvel_id": "Ya existe un comic con ese valor, debe ser único."
        },
        status=status.HTTP_400_BAD_REQUEST
    )


class GetComicAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # permission_classes = (IsAdminUser,)
    # permission_classes = (IsAuthenticated | IsAdminUser,)
    # permission_classes = (IsAuthenticated & IsAdminUser,)
    # permission_classes = (IsAuthenticated, IsAdminUser)
    # Token Authentication
    # authentication_classes = [TokenAuthentication]


class PostComicAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)


class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-POST]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos, pero en este caso ordenados según "marvel_id".
    Tambien nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all().order_by('marvel_id')
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)


class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro,
    o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)


# En este caso observamos como es el proceso de actualización "parcial"
# utilizando el serializador para validar los datos que llegan del request.
# Dicho proceso se conoce como "deserialización".
class UpdateComicAPIView(UpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro,
    o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)
    lookup_field = 'marvel_id'

    def put(self, request, *args, **kwargs):
        _serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data,
            many=False,
            partial=True
        )
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class DestroyComicAPIView(DestroyAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO DELETE]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)


# class GetOneComicAPIView(RetrieveAPIView):
#     __doc__ = f'''{mensaje_headder}
#     `[METODO GET]`
#     Esta vista de API nos devuelve un comic en particular de la base de datos.
#     '''
#     serializer_class = ComicSerializer
#     permission_classes = (IsAuthenticated | IsAdminUser,)
#     queryset = Comic.objects.all()


class GetOneComicAPIView(RetrieveAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos.
    '''
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated | IsAdminUser,)
    queryset = Comic.objects.all()

    def get_queryset(self):
        '''
        Sobrescribimos el método `get_queryset()` para poder filtrar el 
        request por medio de la url. En este caso traemos de la url 
        por medio de `self.kwargs` el parámetro `id` y con él 
        realizamos una query para traer el comic del ID solicitado. 
        '''
        comic_id = self.kwargs['pk']
        queryset = self.queryset.filter(id=comic_id)
        return queryset


class GetOneMarvelComicAPIView(RetrieveAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos
    a partir del valor del campo "marvel_id" pasado por URL.
    '''
    serializer_class = ComicSerializer
    permission_classes = (IsAuthenticated | IsAdminUser,)
    queryset = Comic.objects.all()
    lookup_field = 'marvel_id'

# Otra forma de realizar un Get y traernos un solo
# # objeto o instancia(Detalle) utilizando el método ".get_object()"
# y sobreescribiendo el método ".get()".
# class GetOneMarvelComicAPIView(RetrieveAPIView):
#     serializer_class = ComicSerializer
#     permission_classes = (IsAuthenticated | IsAdminUser,)
#     queryset = Comic.objects.all()
#     lookup_field = 'marvel_id'

#     def get(self, request, *args, **kwargs):
#         serializer = self.get_serializer(
#             instance=self.get_object(), many=False
#         )
#         return Response(
#             data=serializer.data, status=status.HTTP_200_OK
#         )


# Si tuvieramos que hacerlo más genérico, usamos APIView, lo cual
# nos permite tener más personalización sobre la View.
# class GetOneMarvelComicAPIView(APIView):
#     permission_classes = (IsAuthenticated | IsAdminUser,)

#     def get_queryset(self):
#         return Comic.objects.filter(
#             marvel_id=self.kwargs.get('marvel_id')
#         )

#     def get(self, request, *args, **kwargs):
#         _queryset = self.get_queryset()
#         if not _queryset.exists():
#             return Response(
#                 data={'detail': 'Not found.'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = ComicSerializer(
#             instance=_queryset.first(), many=False
#         )
#         return Response(
#             data=serializer.data, status=status.HTTP_200_OK
#         )


class LoginUserAPIView(APIView):
    '''
    ```
    Vista de API personalizada para recibir peticiones de tipo POST.
    Esquema de entrada:
    {"username":"root", "password":12345}
    
    Esta función sobrescribe la función post original de esta clase,
    recibe "request" y hay que setear format=None, para poder recibir 
    los datos en "request.data", la idea es obtener los datos enviados en el 
    request y autenticar al usuario con la función "authenticate()", 
    la cual devuelve el estado de autenticación.
    Luego con estos datos se consulta el Token generado para el usuario,
    si no lo tiene asignado, se crea automáticamente.
    Esquema de entrada:\n
    {
        "username": "root",
        "password": 12345
    }
    ```
    '''
    authentication_classes = ()
    permission_classes = ()

    # NOTE: Agregamos todo esto para personalizar
    # el body de la request y los responses
    # que muestra como ejemplo el Swagger para
    # esta view.

    # NOTE 2: Descomentar dicho decorador para
    # mostrarlo en clase.

    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT, 
    #         properties={
    #             'username': openapi.Schema(
    #                 type=openapi.TYPE_STRING,
    #                 description='username'
    #             ),
    #             'password': openapi.Schema(
    #                 type=openapi.TYPE_STRING,
    #                 format=openapi.FORMAT_PASSWORD,
    #                 description='password'
    #             ),
    #         }
    #     ),
    #     responses= {
    #         "201": openapi.Response(
    #             description='Token: api-key',
    #             examples={
    #                 "application/json": {
    #                     "user": {
    #                         "id": 1,
    #                         "last_login": "2023-01-21T20:45:49.915124Z",
    #                         "is_superuser": True,
    #                         "username": "root",
    #                         "first_name": "first_name",
    #                         "last_name": "last_name",
    #                         "email": "info@inove.com.ar",
    #                         "is_staff": True,
    #                         "is_active": True,
    #                         "date_joined": "2023-01-21T20:45:37.572526Z",
    #                         "groups": [],
    #                         "user_permissions": []
    #                     },              
    #                     "token": "2c9dc08814ad3354bcd924a1ca70edef4032efc5"
    #                 }
    #             }
    #         ),
    #        "400": openapi.Response(
    #             description='Credenciales Inválidas',
    #             examples={
    #                 "application/json": {
    #                     'error': 'Invalid Credentials'
    #                 }
    #             }
    #         ),
    #     }
    # )
    def post(self, request):
        # Realizamos validaciones a través del serializador
        user_login_serializer = UserLoginSerializer(data=request.data)
        if user_login_serializer.is_valid():
            _username = request.data.get('username')
            _password = request.data.get('password')

            # Si el usuario existe y sus credenciales son validas,
            # tratamos de obtener el TOKEN:
            _account = authenticate(username=_username, password=_password)
            if _account:
                _token, _created = Token.objects.get_or_create(user=_account)
                return Response(
                    data=TokenSerializer(instance=_token, many=False).data,
                    status=status.HTTP_200_OK
                )
            return Response(
                data={'error': 'Invalid Credentials.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=user_login_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
