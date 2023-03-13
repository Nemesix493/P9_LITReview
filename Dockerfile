FROM python:3.10
WORKDIR /app
COPY ./requirements.txt /app/
COPY ./LITReview/ /app
RUN pip install -r requirements.txt
RUN rm db.sqlite3
RUN python -m manage migrate
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
#RUN pip install gunicorn
EXPOSE 8000
CMD ["python", "-m", "manage", "runserver", "0.0.0.0:8000"]