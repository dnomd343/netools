FROM golang:1.18.3-alpine3.16 AS build
RUN apk add build-base git && \
  git clone https://github.com/cloverstd/tcping.git && \
  cd /go/tcping && go mod vendor && \
  CGO_ENABLED=0 go build -mod=vendor -ldflags "-s -w" && \
  mv /go/tcping/tcping /tmp

FROM python:alpine3.16
COPY --from=build /tmp /usr/bin
RUN pip3 install dnspython flask
