# netools

An online network testing toolset.

## Ping

|  Field  | Optional |  Type  | Default |                      Describe                      |
|:-------:|:--------:|:------:|:-------:|:--------------------------------------------------:|
| server  |   `NO`   | `str`  |         |        IPv4, IPv6 address or a domain name         |
| v6First |  `YES`   | `bool` | `false` | IPv6 is preferred when the server is a domain name |
|  count  |  `YES`   | `int`  |  `16`   |  The number of ping requests sent, range `1 - 64`  |
|  fast   |  `YES`   | `bool` | `true`  |         Ping as soon as reply is recevied          |
|  size   |  `YES`   | `int`  |  `56`   |      Data bytes in packets, range `4 - 1016`       |
| timeout |  `YES`   | `int`  |  `20`   |    Time limit for all requests, range `1 - 60`     |


Example of response:

```
{
  "ip": "220.181.38.148",
  "alive": true,
  "ttl": 38,
  "times": 16,
  "avg": "77.885",
  "cv": "0.105",
  "value": [
    "81.997",
    "120.573",
    "61.290",
    "78.400",
    "78.623",
    "66.632",
    "77.715",
    "79.042",
    "88.348",
    "70.319",
    "74.119",
    "92.237",
    "75.648",
    "98.559",
    "83.566",
    "82.458"
  ]
}
```

## TCPing

|  Field  | Optional |  Type  | Default |                      Describe                      |
|:-------:|:--------:|:------:|:-------:|:--------------------------------------------------:|
| server  |   `NO`   | `str`  |         |        IPv4, IPv6 address or a domain name         |
|  port   |   `NO`   | `str`  |         |     TCP port for connection, range `1 - 65535`     |
| v6First |  `YES`   | `bool` | `false` | IPv6 is preferred when the server is a domain name |
|  count  |  `YES`   | `int`  |   `4`   | The number of tcp connection tried, range `1 - 16` |
| timeout |  `YES`   | `int`  |   `3`   |   Time limit for each connection, range `1 - 10`   |

Example of response:

```
{
  "ip": "8.210.148.24",
  "times": 4,
  "count": 4,
  "avg": "61.086",
  "cv": "0.148",
  "value": [
    "73.433",
    "61.607",
    "56.976",
    "52.327"
  ]
}
```
