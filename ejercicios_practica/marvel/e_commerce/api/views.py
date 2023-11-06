from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from rest_framework import status
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
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from e_commerce.api.serializers import *
from e_commerce.models import Comic


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


# NOTE: APIs genéricas:
class GetComicAPIView(ListAPIView):
    '''
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer


class PostComicAPIView(CreateAPIView):
    '''
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer


class ListCreateComicAPIView(ListCreateAPIView):
    '''
    `[METODO GET-POST]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos, pero en este caso ordenados según "marvel_id".
    Tambien nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all().order_by('marvel_id')
    serializer_class = ComicSerializer


class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    '''
    `[METODO GET-PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro,
    o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer


# En este caso observamos como es el proceso de actualización "parcial"
# utilizando el serializador para validar los datos que llegan del request.
# Dicho proceso se conoce como "deserialización".
class UpdateComicAPIView(UpdateAPIView):
    '''
    `[METODO PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro,
    o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
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
    '''
    `[METODO DELETE]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer


# class GetOneComicAPIView(RetrieveAPIView):
#     '''
#     `[METODO GET]`
#     Esta vista de API nos devuelve un comic en particular de la base de datos.
#     '''
#     serializer_class = ComicSerializer
#     queryset = Comic.objects.all()


class GetOneComicAPIView(RetrieveAPIView):
    '''
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos.
    '''
    serializer_class = ComicSerializer
    queryset = Comic.objects.all()

    def get_queryset(self):
        '''
        Sobrescribimos el método `get_queryset()` para poder filtrar el 
        request por medio de la url. En este caso traemos de la url 
        por medio de `self.kwargs` el parámetro `id` y con él 
        realizamos una query para traer el comic del ID solicitado. 
        '''
        comic_id = self.kwargs.get('pk')
        queryset = self.queryset.filter(id=comic_id)
        return queryset


class GetOneMarvelComicAPIView(RetrieveAPIView):
    '''
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos
    a partir del valor del campo "marvel_id" pasado por URL.
    '''
    serializer_class = ComicSerializer
    queryset = Comic.objects.all()
    lookup_field = 'marvel_id'

# Otra forma de realizar un Get y traernos un solo
# # objeto o instancia(Detalle) utilizando el método ".get_object()"
# y sobreescribiendo el método ".get()".
# class GetOneMarvelComicAPIView(RetrieveAPIView):
#     serializer_class = ComicSerializer
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
