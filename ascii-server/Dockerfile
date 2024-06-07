FROM ubuntu:23.04

COPY http_response.sh http_response.sh
RUN apt-get update && apt-get install -y --no-install-recommends \
ucspi-tcp \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

EXPOSE 8081

CMD ["tcpserver", "0", "8081", "./http_response.sh"]
