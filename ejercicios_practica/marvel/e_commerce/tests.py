from django.test import TestCase

# Create your tests here.
import json
import pytest

from pytest_fixtures import *

from django.urls import reverse, NoReverseMatch

from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your tests here.

# Testeamos que la view solo permite requests de tipo POST
@pytest.mark.django_db
def test_login_user_api_view_post_only():
    api_view_name = "LoginUserAPIView"
    client = APIClient()
    
    try:
        endpoint_url = reverse('login')
    except NoReverseMatch:
        msg = (
            'El parámetro "name" no se encuentra definido o no es el '
            f'correcto cuando definió la URL de la view: {api_view_name}.'
        )
        assert False, msg
        
    # Tratamos de hacer una request de tipo GET
    response = client.get(endpoint_url)

    # Chequeamos el status_code
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, 'Método HTTP incorrecto. Debe ser una request de tipo POST.'
    

# Test para chequear el login y creación/asignación del token
@pytest.mark.django_db
def test_login_user_api_view():
    api_view_name = "LoginUserAPIView"
    client = APIClient()
    
    try:
        endpoint_url = reverse('login') # El endpoint para el login lo moví al urls.py de marvel.marvel
    except NoReverseMatch:
        msg = (
            'El parámetro "name" no se encuentra definido o no es el '
            f'correcto cuando definió la URL de la view: {api_view_name}.'
        )
        assert False, msg

    user_credentials = {
        "username": "root",
        "password": "12345"
    }

    User.objects.create_user(**user_credentials)

    # Intentamos realizar el login
    response = client.post(endpoint_url, data=json.dumps(user_credentials), content_type='application/json')

    # Chequeamos el endpoint
    assert response.status_code != 404, 'Endpoint no encontrado'

    response_data = response.json()

    # Chequeamos que el token sea devuelto en la respuesta
    assert 'token' in response_data, 'Error al asignar el Token. No fue encontrado en la response.'

    # Chequeamos que el token corresponda al usuario. Para eso:
    # 1. Autenticamos al usuario con las credenciales con las que lo creamos arriba
    user = authenticate(**user_credentials)
    assert user is not None, 'Falló la autenticación. No se encontró el usuario.'
    
    # 2. Tratamos de obtener el Token asignado al usuario
    token, created = Token.objects.get_or_create(user=user)
    assert response_data['token'] == token.key, 'El Token de la respuesta no coincide con el del usuario.'
    
    
# Tests para chequear las Permission Classes:

# WishList tests:

# Para GetWishListAPIView (Permisos: IsAuthenticated; Autenticacion: TokenAuthentication)
@pytest.mark.django_db
def test_get_wishlist_api_view_permissions(create_user, create_wishlist):
    api_view_name = "GetWishListAPIView"
    client = APIClient()
    
    user = create_user()
    
    # Primero necesitamos la wishlist:
    wishlist = create_wishlist(user=user)
    
    token, created = Token.objects.get_or_create(user=user)
    try:
        url = reverse('get_wishlist_api_view', kwargs={'pk': wishlist.id})
    except NoReverseMatch:
        msg = (
            'El parámetro "name" no se encuentra definido o no es el '
            f'correcto cuando definió la URL de la view: {api_view_name}.'
        )
        assert False, msg
        
    # Testeamos que el usuario NO autenticado (y SIN token) NO tenga acceso
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, 'El endpoint NO debería ser accesible sin Token.'
    
    # Testeamos que el usuario autenticado con Token tenga acceso
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK, 'El endpoint debería ser accesible con un Token válido.'


# Para PostWishListAPIView (Permisos: IsAuthenticated & IsAdminUser)
@pytest.mark.django_db
def test_post_wishlist_api_view_permissions(create_user, create_comic):
    api_view_name = "PostWishListAPIView"
    client = APIClient()
    
    comic = create_comic()
    user = create_user(username="random1")
    
    wishlist_data = {
        'comic': comic.id,
        'user': user.id,
        'favorite': True,
        'cart': False,
        'wished_qty': 1,
        'bought_qty': 0
    }
    
    try:
        url = reverse('post_wishlist_api_view')
    except NoReverseMatch:
        msg = (
            'El parámetro "name" no se encuentra definido o no es el '
            f'correcto cuando definió la URL de la view: {api_view_name}.'
        )
        assert False, msg
        
    # Testeamos que un usuario normal no tenga acceso
    client.force_authenticate(user=user)
    response = client.post(url, wishlist_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN, 'El endpoint NO debería ser accesible sin estar autenticado.'
    
    # Testeamos que un Admin User tenga acceso
    admin_user = User.objects.create_superuser(username='admin_user', password='adminpass')
    client.force_authenticate(user=admin_user)
    
    response = client.post(url, wishlist_data)
    assert response.status_code == status.HTTP_201_CREATED, 'Un usuario Admin o Superuser debería poder realizar la request POST.'



# Para UpdateWishListAPIView (Permisos: IsAuthenticated | IsAdminUser)
@pytest.mark.django_db
def test_update_wishlist_api_view_permissions(create_user, create_wishlist):
    api_view_name = "UpdateWishListAPIView"
    client = APIClient()
    user = create_user(username="random2")
    
    wishlist = create_wishlist(user=user)
    
    try:
        url = reverse('update_wishlist_api_view', kwargs={'pk': wishlist.id})
    except NoReverseMatch:
        msg = (
            'El parámetro "name" no se encuentra definido o no es el '
            f'correcto cuando definió la URL de la view: {api_view_name}.'
        )
        assert False, msg
        
    # Testeamos que un usuario no autenticado no tenga acceso
    client.force_authenticate(user=None)
    response = client.patch(url, {'wished_qty': 9})
    assert response.status_code == status.HTTP_403_FORBIDDEN, 'El endpoint NO debería ser accesible sin estar autenticado.'
    
    # Testeamos que un usuario autenticado tenga acceso
    client.force_authenticate(user=user)
    response = client.patch(url, {'wished_qty': 3})
    assert response.status_code == status.HTTP_200_OK, 'Un usuario autenticado debería tener acceso a este endpoint.'
    
    # Testeamos que un usuario Admin tenga acceso
    admin_user = User.objects.create_superuser(username='admin_user2', password='adminpass')
    client.force_authenticate(user=admin_user)
    
    response = client.patch(url, {'wished_qty': 4})
    assert response.status_code == status.HTTP_200_OK, 'Un superuser debería tener acceso a este endpoint.'
    



# Para DeleteWishListAPIView (Permisos: IsAdminUser)
@pytest.mark.django_db
def test_delete_wishlist_api_view_permissions(create_user, create_wishlist):
    api_view_name = "DeleteWishListAPIView"
    client = APIClient()
    user = create_user(username="random3")
    wishlist = create_wishlist(user=user)
    
    try:
        url = reverse('delete_wishlist_api_view', kwargs={'pk': wishlist.id})
    except NoReverseMatch:
        msg = (
            'El parámetro "name" no se encuentra definido o no es el '
            f'correcto cuando definió la URL de la view: {api_view_name}.'
        )
        assert False, msg
        
    # Testeamos que un usuario normal no tenga acceso
    client.force_authenticate(user=user)
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, 'El endpoint NO debería ser accesible sin estar autenticado.'
    
    # Testeamos que un usuario Admin tenga acceso
    admin_user = User.objects.create_superuser(username='admin_user3', password='adminpass')
    client.force_authenticate(user=admin_user)
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, 'Un superuser debería tener acceso a este endpoint.'
