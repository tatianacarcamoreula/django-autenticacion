FROM python:3.9.5
ENV PYTHONUNBUFFERED=1
# Corremos este comando para actualizar pip.
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
# En este caso como ya está creado el proyecto asignamos
# como directorio de trabajo el directorio raíz del mismo.
WORKDIR /opt/back_end/marvel
COPY . /opt/back_end
RUN apt-get update && apt-get -y install vim
CMD python manage.py runserver 0.0.0.0:8000