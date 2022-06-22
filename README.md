# netools

An online network testing toolset.

## Ping

|  Field  | Optional |  Type  | Default |                      Describe                      |
| :-----: | :------: | :----: | :-----: | :------------------------------------------------: |
| server  |   `NO`   | `str`  |         |        IPv4, IPv6 address or a domain name         |
| v6First |  `YES`   | `bool` | `false` | IPv6 is preferred when the server is a domain name |
|  count  |  `YES`   | `int`  |  `16`   |  The number of ping requests sent, range `1 - 64`  |
|  fast   |  `YES`   | `bool` | `true`  |         Ping as soon as reply is recevied          |
|  size   |  `YES`   | `int`  |  `56`   |      Data bytes in packets, range `4 - 1016`       |
| timeout |  `YES`   | `int`  |  `20`   |    Time limit for all requests, range `1 - 60`     |

