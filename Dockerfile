FROM python:3.10
WORKDIR /app
COPY ./requirements.txt /app/
COPY ./LITReview/ /app
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN python -m manage makemigrations
RUN python -m manage migrate
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
CMD ["python", "-m", "manage", "runserver", "0.0.0.0:8000"]