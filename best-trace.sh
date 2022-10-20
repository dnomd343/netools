#!/usr/bin/env sh

wget https://cdn.ipip.net/17mon/besttrace4linux.zip
unzip besttrace4linux.zip

case "$(uname -m)" in
  'i386' | 'i686' | 'amd64' | 'x86_64')
    BEST_TRACE='besttrace32';;
  'armv7' | 'armv7l' | 'armv8' | 'aarch64')
    BEST_TRACE="besttracearm";;
  *)
  echo "Architecture not supported" && exit 1
esac

mv ${BEST_TRACE} /tmp/besttrace
chmod +x /tmp/besttrace
