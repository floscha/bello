FROM python:3.6-alpine

# Build Trello client from source since pypi repo is outdated.
RUN apk add --update git \
    && git clone https://github.com/sarumont/py-trello.git \
    && pip install -e /py-trello \
    && apk del git \
    && rm -rf /var/cache/apk/*

# Install other dependencies.
WORKDIR /app
ADD requirements.txt /app
RUN cd /app && \
    pip install -r requirements.txt

# Add actual source code.
ADD src /app/src

EXPOSE 5000

CMD ["python", "src/run.py"]
