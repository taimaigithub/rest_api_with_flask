FROM python:3.9
WORKDIR /app
EXPOSE 5000
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD [ "flask", "run", "--host", "0.0.0.0" ]