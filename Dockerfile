ARG ALPINE="alpine:3.16"
ARG GOLANG="golang:1.18-alpine3.16"
ARG PYTHON="python:3.10-alpine3.16"

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
COPY best-trace.sh /
RUN sh best-trace.sh

FROM ${ALPINE} AS build
COPY --from=tcping /tmp/tcping /release/
COPY --from=tlsping /tmp/tlsping /release/
COPY --from=dnslookup /tmp/dnslookup /release/
COPY --from=best-trace /tmp/besttrace /release/

FROM ${PYTHON} AS wheels
WORKDIR /wheels/
RUN pip3 wheel dnspython flask gevent IPy
RUN ls *.whl | xargs -n1 unzip && rm *.whl && rm -rf $(find ./ -name '__pycache__')

FROM ${PYTHON}
RUN apk add --no-cache bind-tools mtr
COPY --from=wheels /wheels/ /usr/local/lib/python3.10/site-packages/
COPY --from=build /release/ /usr/bin/
WORKDIR /netools/
COPY ./ /netools/
EXPOSE 5633
# TODO: docker entrypoint with single exec-file
CMD ["python3", "api.py"]
