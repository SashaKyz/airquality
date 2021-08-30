FROM python:alpine
RUN apk add --update --no-cache \
    bash build-base \
    tzdata py-pip
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py"]