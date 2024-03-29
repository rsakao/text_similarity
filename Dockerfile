FROM python:3.12.2-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN python manage.py migrate
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]