ARG ALPINE="alpine:3.16"
ARG GOLANG="golang:1.18-alpine3.16"
ARG PYTHON="python:3.10-alpine3.16"

# TODO: python3 wheels build
# TODO: docker entrypoint with single exec-file

FROM ${GOLANG} AS tcping
RUN apk add git
RUN git clone https://github.com/cloverstd/tcping.git
WORKDIR ./tcping/
RUN go mod vendor
RUN env CGO_ENABLED=0 go build -v -mod=vendor -trimpath -ldflags \
      "-X main.version=$(git describe --tags) -X main.gitCommit=$(git rev-parse HEAD) -s -w"
RUN mv tcping /tmp/

FROM ${GOLANG} AS tlsping
RUN apk add git
RUN git clone https://github.com/dnomd343/tlsping.git
WORKDIR ./tlsping/
RUN go mod init github.com/dnomd343/tlsping
WORKDIR ./cmd/tlsping/
RUN env CGO_ENABLED=0 go build -v -trimpath -ldflags \
      "-X main.appVersion=$(git describe --tag) -X 'main.appBuildTime=$(date "+%Y-%m-%d %H:%M:%S")' -s -w"
RUN mv tlsping /tmp/

FROM ${GOLANG} AS dnslookup
ENV DNSLOOKUP="1.8.0"
RUN wget https://github.com/ameshkov/dnslookup/archive/refs/tags/v${DNSLOOKUP}.tar.gz && tar xf v${DNSLOOKUP}.tar.gz
WORKDIR ./dnslookup-${DNSLOOKUP}/
RUN env CGO_ENABLED=0 go build -v -trimpath -ldflags "-X main.VersionString=v${DNSLOOKUP} -s -w"
RUN mv dnslookup /tmp/

FROM ${ALPINE} AS best-trace
COPY besttrace.sh /
RUN sh besttrace.sh

FROM ${PYTHON}
WORKDIR /netools
COPY . /netools
COPY --from=build /tmp /usr/bin
RUN pip3 install dnspython flask gevent IPy
EXPOSE 5633
CMD ["python3", "api.py"]
RUN apk add --no-cache bind-tools mtr
