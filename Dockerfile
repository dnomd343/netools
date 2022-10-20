ARG ALPINE="alpine:3.16"
ARG GOLANG="golang:1.18-alpine3.16"
ARG PYTHON="python:3.10-alpine3.16"

FROM ${PYTHON} AS wheels
WORKDIR /wheels/
RUN pip3 wheel dnspython flask gevent IPy
RUN ls *.whl | xargs -n1 unzip -d ./site-packages/ && rm *.whl && rm -rf $(find ./ -name '__pycache__')
RUN cd /usr/local/lib/python*/ && mkdir -p /packages/$(basename ${PWD})/ && mv /wheels/* /packages/python*/

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
RUN wget https://cdn.ipip.net/17mon/besttrace4linux.zip && unzip besttrace4linux.zip
RUN case "$(uname -m)" in \
      'i386' | 'i686' | 'amd64' | 'x86_64') mv besttrace32 /tmp/besttrace;; \
      'armv7' | 'armv7l' | 'armv8' | 'aarch64') mv besttracearm /tmp/besttrace;; \
      *) echo "Architecture not supported" && exit 1;; \
    esac
RUN chmod +x /tmp/besttrace

FROM ${ALPINE} AS build
COPY --from=wheels /packages/ /asset/usr/local/lib/
COPY --from=best-trace /tmp/besttrace /asset/usr/bin/
COPY --from=dnslookup /tmp/dnslookup /asset/usr/bin/
COPY --from=tlsping /tmp/tlsping /asset/usr/bin/
COPY --from=tcping /tmp/tcping /asset/usr/bin/
COPY ./ /asset/netools/
RUN ln -s /netools/netools.py /asset/usr/bin/netools

FROM ${PYTHON}
RUN apk add --no-cache bind-tools mtr
COPY --from=build /asset/ /
EXPOSE 5633
ENTRYPOINT ["netools"]
