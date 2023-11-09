import pytest
import uuid

from e_commerce.models import Comic, WishList


@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        username = 'inovecode_{}'.format(uuid.uuid4().hex[:6].lower())
        return django_user_model.objects.create_user(
            username=username,
            password='12345678hola',
            email='inovecode@mail.com'
        )
    return make_user


@pytest.fixture
def create_comic():
    def make_comic(**kwargs):
        return Comic.objects.create(
            marvel_id=9999,
            title='Inove SuperHeroe',
            description='Coding School',
            price=10.0,
            stock_qty=15,
            picture=''
        )
    return make_comic

@pytest.fixture
def create_wishlist(create_user, create_comic):
    comic = create_comic()
    user = create_user()
    def make_wishlist(**kwargs):
        return WishList.objects.create(
            user=user,
            comic=comic,
            favorite=True,
            cart=False,
            wished_qty=1,
            bought_qty=0
        )
    return make_wishlist
