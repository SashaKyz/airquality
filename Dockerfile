FROM python:alpine
RUN apk add --update --no-cache \
    bash build-base python-dev \
    tzdata py-rrd py-pip py-jinja2 && \
    pip3 install -y rrdtool

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py"]