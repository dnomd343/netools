# netools

> An online network testing toolset.

## Ping

|  Field  | Optional |  Type  | Default |                      Describe                      |
|:-------:|:--------:|:------:|:-------:|:--------------------------------------------------:|
| server  |   `NO`   | `str`  |         |        IPv4, IPv6 address or a domain name         |
| v6First |  `YES`   | `bool` | `false` | IPv6 is preferred when the server is a domain name |
|  count  |  `YES`   | `int`  |  `16`   |  The number of ping requests sent, range `1 - 64`  |
|  fast   |  `YES`   | `bool` | `true`  |         Ping as soon as reply is received          |
|  size   |  `YES`   | `int`  |  `56`   |      Data bytes in packets, range `4 - 1016`       |
| timeout |  `YES`   | `int`  |  `20`   |    Time limit for all requests, range `1 - 60`     |

<details>

<summary><b>Response Example</b></summary>

<br/>

The target server is normal

```json
{
  "success": true,
  "ip": "220.181.38.148",
  "alive": true,
  "ttl": 49,
  "statistics": {
    "count": 16,
    "reply": 16,
    "rate": "100.0%",
    "avg": "38.345",
    "min": "38.281",
    "max": "38.417",
    "sd": "0.029"
  }
}
```

The target server is offline

```json
{
  "success": true,
  "ip": "255.255.255.255",
  "alive": false
}
```

Invalid request or error in netools service

```json
{
  "success": false,
  "message": "..."
}
```

</details>

## TCPing

|  Field  | Optional |  Type  | Default |                      Describe                      |
|:-------:|:--------:|:------:|:-------:|:--------------------------------------------------:|
| server  |   `NO`   | `str`  |         |        IPv4, IPv6 address or a domain name         |
|  port   |   `NO`   | `str`  |         |     TCP port for connection, range `1 - 65535`     |
| v6First |  `YES`   | `bool` | `false` | IPv6 is preferred when the server is a domain name |
|  count  |  `YES`   | `int`  |   `4`   | The number of tcp connection tried, range `1 - 16` |
| timeout |  `YES`   | `int`  |   `3`   |   Time limit for each connection, range `1 - 10`   |

<details>

<summary><b>Response Example</b></summary>

<br/>

The tcp port of target server is open

```json
{
  "success": true,
  "ip": "8.210.148.24",
  "port": 80,
  "alive": true,
  "statistics": {
    "count": 4,
    "reply": 4,
    "rate": "100.0%",
    "avg": "3.208",
    "min": "2.597",
    "max": "3.462",
    "sd": "0.358"
  }
}
```

The target server is offline or the port is not open

```json
{
  "success": true,
  "ip": "8.210.148.24",
  "port": 8888,
  "alive": false
}
```

Invalid request or error in netools service

```json
{
  "success": false,
  "message": "..."
}
```

</details>

## TLSPing

|  Field  | Optional |  Type  | Default |                      Describe                      |
|:-------:|:--------:|:------:|:-------:|:--------------------------------------------------:|
| server  |   `NO`   | `str`  |         |        IPv4, IPv6 address or a domain name         |
|  port   |   `NO`   | `str`  |         |     TCP port for connection, range `1 - 65535`     |
|  host   |  `YES`   | `str`  | server  |          SNI parameter in TLS connection           |
| v6First |  `YES`   | `bool` | `false` | IPv6 is preferred when the server is a domain name |
| verify  |  `YES`   | `bool` | `true`  |    Make sure TLS is not subject to MITM attacks    |
|  count  |  `YES`   | `int`  |   `4`   | The number of tcp connection tried, range `1 - 16` |

<details>

<summary><b>Response Example</b></summary>

<br/>

The TLS connection of target server and port is normal

```json
{
  "success": true,
  "ip": "8.210.148.24",
  "port": 443,
  "host": "ip.343.re",
  "alive": true,
  "statistics": {
    "count": 4,
    "avg": "51.763",
    "min": "36.902",
    "max": "66.559",
    "sd": "11.043"
  }
}
```

Failed to establish TLS connection

```json
{
  "success": true,
  "ip": "8.210.148.24",
  "port": 443,
  "host": "dns.343.re",
  "alive": false
}
```

Invalid request or error in netools service

```json
{
  "success": false,
  "message": "..."
}
```

</details>

## HTTPing

WIP...

## Dig

WIP...

## DnsLookUp

WIP...

## MTR

WIP...

## Trace

WIP...

## BestTrace

WIP...
