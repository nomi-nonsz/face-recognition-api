FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

COPY setup.sh /setup.sh
COPY runner.sh /runner.sh
COPY python/requirements.txt /requirements.txt

RUN chmod +x /setup.sh /runner.sh

RUN /setup.sh

WORKDIR /app

COPY node/package.json ./

RUN yarn

COPY . .
EXPOSE 3002

CMD ["sh", "/runner.sh"]
