FROM python:3.13.2
WORKDIR /usr/app
COPY ./requirements.txt /usr/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/app/requirements.txt
COPY . /usr/app
CMD ["fastapi", "run", "main.py", "--port", "80"]