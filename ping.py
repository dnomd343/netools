import re
import subprocess

def pingProcess(server: str, count: int, fast: bool, size: int, timeout: int) -> str:
    pingCmd = ['ping', server, '-c', str(count), '-s', str(size), '-w', str(timeout)]
    if fast:  # fast mode
        pingCmd.append('-A')
    process = subprocess.Popen(pingCmd, stdout = subprocess.PIPE, stderr = subprocess.DEVNULL)
    process.wait()
    return process.stdout.read().decode()

def ping(server: str, v6First: bool or None, count: int or None,
         fast: bool or None, size: int or None, timeout: int or None) -> dict:

    # TODO: server is domain -> IP address (v4/v6)

    if count is None: count = 16  # default times of ping
    if type(count) != int:
        raise RuntimeError('invalid `count` value')
    if count < 1 or count > 64:  # count between 1 ~ 64
        raise RuntimeError('`count` value out of range')

    if fast is None: fast = bool  # default use fast mode
    if type(fast) != bool:
        raise RuntimeError('invalid `fast` value')

    if size is None: size = 56  # default data bytes in packets
    if type(size) != int:
        raise RuntimeError('invalid `size` value')
    if size < 4 or size > 1016:  # size between 4 ~ 1016
        raise RuntimeError('`size` value out of range')

    if timeout is None: timeout = 20  # default wait for 20s
    if type(timeout) != int:
        raise RuntimeError('invalid `timeout` value')
    if timeout < 1 or timeout > 60:  # timeout between 1 ~ 60
        raise RuntimeError('`timeout` value out of range')

    pingResult = []
    rawOutput = pingProcess(server, count, fast, size, timeout).split('\n')
    for i in range(1, len(rawOutput)):  # skip first line
        if rawOutput[i].strip() == '': continue
        if 'ping statistics' in rawOutput[i]: break
        if 'bytes from' not in rawOutput[i]: continue
        pingResult.append({
            'seq': int(re.search(r'seq=(\d+)', rawOutput[i])[1]),
            'ttl': int(re.search(r'ttl=(\d+)', rawOutput[i])[1]),
            'time': re.search(r'time=([\d.]+)', rawOutput[i])[1],
        })
    return {'ret': pingResult}

result = ping('127.0.0.1', v6First=None, count=48, fast=True, size=None, timeout=10)
print(result)
