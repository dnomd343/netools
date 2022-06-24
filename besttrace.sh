get_architecture() {
  case "$(uname -m)" in
    'i386' | 'i686')
      MACHINE='i386';;
    'amd64' | 'x86_64')
      MACHINE='amd64';;
    'armv7' | 'armv7l')
      MACHINE='arm';;
    'armv8' | 'aarch64')
      MACHINE='arm64';;
    *)
    echo "Architecture not supported" && exit 1
  esac
}

mkdir -p /tmp/best-trace && cd /tmp/best-trace || exit 1
wget https://cdn.ipip.net/17mon/besttrace4linux.zip
unzip besttrace4linux.zip

get_architecture
case "$MACHINE" in
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

mv ./$BEST_TRACE /tmp/besttrace
chmod +x /tmp/besttrace
rm -rf /tmp/best-trace
