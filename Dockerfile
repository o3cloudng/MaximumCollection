# start from an official image
FROM python:3.10.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser ./

USER appuser


RUN pip install --upgrade pip

# install our dependencies
COPY ./requirements.txt ./requirements.txt

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python manage.py makemigrations --no-input

# RUN python manage.py migrate --no-input 

# RUN python manage.py collectstatic --no-input -v 2

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
# CMD ["gunicorn", "--chdir", "nsib", "--bind", ":8000", "nsib.wsgi:application", "--reload"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# runs the production server
ENTRYPOINT ["python", "./manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
