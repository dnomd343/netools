# netools

> An online network testing toolset.

## Ping

|  Field  | Essential |  Type  | Default |   Range    |                 Describe                 |
|:-------:|:---------:|:------:|:-------:|:----------:|:----------------------------------------:|
| server  |   `YES`   | `str`  |         |            |   IPv4, IPv6 address or a domain name    |
| v6First |   `NO`    | `bool` | `false` |            | IPv6 is preferred (only for domain name) |
|  count  |   `NO`    | `int`  |  `16`   |  `1 - 64`  |     The number of ping requests sent     |
|  fast   |   `NO`    | `bool` | `true`  |            |    Ping as soon as reply is received     |
|  size   |   `NO`    | `int`  |  `56`   | `4 - 1016` |          Data bytes in packets           |
| timeout |   `NO`    | `int`  |  `20`   |  `1 - 60`  |       Time limit for all requests        |

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

|  Field  | Essential |  Type  | Default |    Range    |                 Describe                 |
|:-------:|:---------:|:------:|:-------:|:-----------:|:----------------------------------------:|
| server  |   `YES`   | `str`  |         |             |   IPv4, IPv6 address or a domain name    |
|  port   |   `YES`   | `str`  |         | `1 - 65535` |         TCP port for connection          |
| v6First |   `NO`    | `bool` | `false` |             | IPv6 is preferred (only for domain name) |
|  count  |   `NO`    | `int`  |   `4`   |  `1 - 16`   |    The number of tcp connection tried    |
| timeout |   `NO`    | `int`  |   `3`   |  `1 - 10`   |      Time limit for each connection      |

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

|  Field  | Essential |  Type  | Default |    Range    |                   Describe                   |
|:-------:|:---------:|:------:|:-------:|:-----------:|:--------------------------------------------:|
| server  |   `YES`   | `str`  |         |             |     IPv4, IPv6 address or a domain name      |
|  port   |   `YES`   | `str`  |         | `1 - 65535` |           TCP port for connection            |
|  host   |   `NO`    | `str`  | server  |             |       SNI parameter in TLS connection        |
| v6First |   `NO`    | `bool` | `false` |             |   IPv6 is preferred (only for domain name)   |
| verify  |   `NO`    | `bool` | `true`  |             | Make sure TLS is not subject to MITM attacks |
|  count  |   `NO`    | `int`  |   `4`   |  `1 - 16`   |      The number of tcp connection tried      |

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

## MTR

|  Field  | Essential |  Type  | Default |                 Describe                 |
|:-------:|:---------:|:------:|:-------:|:----------------------------------------:|
| server  |   `YES`   | `str`  |         |   IPv4, IPv6 address or a domain name    |
| v6First |   `NO`    | `bool` | `false` | IPv6 is preferred (only for domain name) |

<details>

<summary><b>Response Example</b></summary>

<br/>

The MTR ICMP check of target server is normal

```json
{
  "success": true,
  "ip": "220.181.38.148",
  "result": [
    {
      "count": 1,
      "host": "172.18.0.1",
      "Loss%": 0,
      "Snt": 10,
      "Last": 0.041,
      "Avg": 0.04,
      "Best": 0.034,
      "Wrst": 0.052,
      "StDev": 0.005
    },
    {
      "count": 2,
      "host": "???",
      "Loss%": 100,
      "Snt": 10,
      "Last": 0,
      "Avg": 0,
      "Best": 0,
      "Wrst": 0,
      "StDev": 0
    },
    {
      "count": 3,
      "host": "11.73.0.153",
      "Loss%": 70,
      "Snt": 10,
      "Last": 1.298,
      "Avg": 1.354,
      "Best": 1.298,
      "Wrst": 1.468,
      "StDev": 0.098
    },
    {
      "count": 4,
      "host": "10.36.51.185",
      "Loss%": 10,
      "Snt": 10,
      "Last": 1.281,
      "Avg": 1.418,
      "Best": 1.221,
      "Wrst": 2.557,
      "StDev": 0.429
    },
    {
      "count": 5,
      "host": "10.54.154.178",
      "Loss%": 0,
      "Snt": 10,
      "Last": 1.309,
      "Avg": 1.313,
      "Best": 1.093,
      "Wrst": 2.028,
      "StDev": 0.289
    },
    {
      "count": 6,
      "host": "47.246.115.102",
      "Loss%": 0,
      "Snt": 10,
      "Last": 2.044,
      "Avg": 2.064,
      "Best": 1.987,
      "Wrst": 2.166,
      "StDev": 0.053
    },
    {
      "count": 7,
      "host": "47.246.113.249",
      "Loss%": 0,
      "Snt": 10,
      "Last": 2.004,
      "Avg": 2.384,
      "Best": 1.86,
      "Wrst": 6.532,
      "StDev": 1.457
    },
    {
      "count": 8,
      "host": "61.14.203.61",
      "Loss%": 0,
      "Snt": 10,
      "Last": 2.887,
      "Avg": 2.883,
      "Best": 2.834,
      "Wrst": 3.027,
      "StDev": 0.056
    },
    {
      "count": 9,
      "host": "203.160.84.121",
      "Loss%": 0,
      "Snt": 10,
      "Last": 4.273,
      "Avg": 5.834,
      "Best": 2.661,
      "Wrst": 9.611,
      "StDev": 2.429
    },
    {
      "count": 10,
      "host": "43.252.86.141",
      "Loss%": 0,
      "Snt": 10,
      "Last": 3.633,
      "Avg": 5.547,
      "Best": 2.574,
      "Wrst": 8.903,
      "StDev": 2.133
    },
    {
      "count": 11,
      "host": "219.158.10.61",
      "Loss%": 0,
      "Snt": 10,
      "Last": 7.935,
      "Avg": 9.537,
      "Best": 6.324,
      "Wrst": 13.251,
      "StDev": 2.433
    },
    {
      "count": 12,
      "host": "219.158.97.30",
      "Loss%": 0,
      "Snt": 10,
      "Last": 10.686,
      "Avg": 11.088,
      "Best": 7.614,
      "Wrst": 13.93,
      "StDev": 2.202
    },
    {
      "count": 13,
      "host": "219.158.8.113",
      "Loss%": 0,
      "Snt": 10,
      "Last": 11.24,
      "Avg": 11.022,
      "Best": 7.926,
      "Wrst": 14.239,
      "StDev": 2.177
    },
    {
      "count": 14,
      "host": "219.158.112.45",
      "Loss%": 70,
      "Snt": 10,
      "Last": 42.416,
      "Avg": 42.206,
      "Best": 42.095,
      "Wrst": 42.416,
      "StDev": 0.181
    },
    {
      "count": 15,
      "host": "219.158.5.138",
      "Loss%": 0,
      "Snt": 10,
      "Last": 42.799,
      "Avg": 46.692,
      "Best": 42.799,
      "Wrst": 50.285,
      "StDev": 2.593
    },
    {
      "count": 16,
      "host": "219.158.44.122",
      "Loss%": 70,
      "Snt": 10,
      "Last": 45.361,
      "Avg": 45.373,
      "Best": 45.361,
      "Wrst": 45.383,
      "StDev": 0.01
    },
    {
      "count": 17,
      "host": "202.97.17.113",
      "Loss%": 40,
      "Snt": 10,
      "Last": 42.777,
      "Avg": 41.829,
      "Best": 41.583,
      "Wrst": 42.777,
      "StDev": 0.467
    },
    {
      "count": 18,
      "host": "36.110.245.182",
      "Loss%": 90,
      "Snt": 10,
      "Last": 43.331,
      "Avg": 43.331,
      "Best": 43.331,
      "Wrst": 43.331,
      "StDev": 0
    },
    {
      "count": 19,
      "host": "36.110.251.74",
      "Loss%": 90,
      "Snt": 10,
      "Last": 41.735,
      "Avg": 41.735,
      "Best": 41.735,
      "Wrst": 41.735,
      "StDev": 0
    },
    {
      "count": 20,
      "host": "220.181.16.62",
      "Loss%": 10,
      "Snt": 10,
      "Last": 50.778,
      "Avg": 51.816,
      "Best": 50.677,
      "Wrst": 54.84,
      "StDev": 1.608
    },
    {
      "count": 21,
      "host": "106.38.244.146",
      "Loss%": 0,
      "Snt": 10,
      "Last": 46.118,
      "Avg": 46.064,
      "Best": 46.028,
      "Wrst": 46.118,
      "StDev": 0.028
    },
    {
      "count": 22,
      "host": "???",
      "Loss%": 100,
      "Snt": 10,
      "Last": 0,
      "Avg": 0,
      "Best": 0,
      "Wrst": 0,
      "StDev": 0
    },
    {
      "count": 23,
      "host": "???",
      "Loss%": 100,
      "Snt": 10,
      "Last": 0,
      "Avg": 0,
      "Best": 0,
      "Wrst": 0,
      "StDev": 0
    },
    {
      "count": 24,
      "host": "???",
      "Loss%": 100,
      "Snt": 10,
      "Last": 0,
      "Avg": 0,
      "Best": 0,
      "Wrst": 0,
      "StDev": 0
    },
    {
      "count": 25,
      "host": "220.181.38.148",
      "Loss%": 0,
      "Snt": 10,
      "Last": 45.766,
      "Avg": 45.773,
      "Best": 45.743,
      "Wrst": 45.796,
      "StDev": 0.015
    }
  ]
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

## Dig

WIP...

## DnsLookUp

WIP...

## BestTrace

WIP...

# Build

```bash
git clone https://github.com/dnomd343/netools.git
cd ./netools/
docker build -t netools .
```
