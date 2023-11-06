import requests

from django.core.management.base import BaseCommand

from e_commerce.models import Comic
from e_commerce.utils import MARVEL_DICT, get_marvel_params


class Command(BaseCommand):
    help = 'Obtiene los primeros comics de la API de Marvel y los persiste.'

    def handle(self, *args, **options):
        self._print_info('####### Inicio de Comando #######')
        response = requests.get(
            url=MARVEL_DICT.get('URL'),
            params=get_marvel_params()
        )
        if response.status_code == 200:
            self._print_success(f'response: {response}')
            _data = response.json().get('data', {}).get('results', {})
            for _row in _data[:50]:
                _price = _row.get('prices', [{}])[0].get('price', 0.00)
                _description = _row.get('description', '')
                if _price > 0.00 and _description:
                    _instance, _created = Comic.objects.get_or_create(
                        marvel_id=_row.get('id'),
                        defaults={
                            'title': _row.get('title'),
                            'description': _description,
                            'price': _price,
                            'stock_qty': 5,
                            'picture': f"{_row.get('thumbnail', {}).get('path')}/standard_xlarge.jpg",
                            'marvel_id': _row.get('id')
                        }
                    )
                    self._print_debug(
                        f'instance: {_instance} - created: {_created}'
                    )
        else:
            self._print_error(
                f'response: {response} - content: {response.json()}'
            )
        self._print_info('####### Fin de Comando #######')

    def _print_debug(self, text):
        self.stdout.write(self.style.SQL_TABLE(text))

    def _print_success(self, text):
        self.stdout.write(self.style.SUCCESS(text))

    def _print_info(self, text):
        self.stdout.write(self.style.WARNING(text))

    def _print_error(self, text):
        self.stdout.write(self.style.ERROR(text))
