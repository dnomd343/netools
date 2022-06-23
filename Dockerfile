FROM golang:1.18.3-alpine3.16 AS build
RUN apk add build-base git && \
  git clone https://github.com/cloverstd/tcping.git && \
  git clone https://github.com/dnomd343/tlsping.git && \
  git clone https://github.com/ameshkov/dnslookup.git && \
  cd /go/tcping && go mod vendor && CGO_ENABLED=0 go build -mod=vendor -ldflags "-s -w" && \
  cd /go/dnslookup && CGO_ENABLED=0 go build -ldflags "-s -w" && \
  cd /go/tlsping && go mod init github.com/dnomd343/tlsping && \
  cd cmd/tlsping && CGO_ENABLED=0 go build -ldflags "-s -w" && \
  mv /go/tlsping/cmd/tlsping/tlsping /tmp && \
  mv /go/dnslookup/dnslookup /tmp && \
  mv /go/tcping/tcping /tmp

FROM python:alpine3.16
WORKDIR /netools
COPY . /netools
COPY --from=build /tmp /usr/bin
RUN pip3 install dnspython flask gevent IPy
CMD ["python3", "api.py"]
