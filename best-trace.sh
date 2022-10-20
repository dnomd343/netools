#!/usr/bin/env sh

wget https://cdn.ipip.net/17mon/besttrace4linux.zip
unzip besttrace4linux.zip

# get machine architecture
case "$(uname -m)" in
  'i386' | 'i686')
    ARCH='i386';;
  'amd64' | 'x86_64')
    ARCH='amd64';;
  'armv7' | 'armv7l')
    ARCH='arm';;
  'armv8' | 'aarch64')
    ARCH='arm64';;
  *)
  echo "Architecture not supported" && exit 1
esac

case "${ARCH}" in
  'i386')
    BEST_TRACE='besttrace32';;
  'amd64')
    BEST_TRACE='besttrace32';;
  'arm')
    BEST_TRACE="besttracearm";;
  'arm64')
    BEST_TRACE="besttracearm";;
  *)
  exit 1
esac

mv ${BEST_TRACE} /tmp/besttrace
chmod +x /tmp/besttrace
