# T-Rex

A first overview fo the system:
![](./docs/system-diagram.svg)

# Important notes:
## mDNS specs:

device_name: `MyDevice.local.`
service_type: `_http._tcp.local.`
service_name (nome do serviço completo): `MyDevice._http._tcp.local.`

| Field           | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `0*`, `0?`      | DNS Header Flags. `0*` = authority question i.e. the service owner. `0?` = standard query. |
| `[0q]`, `[2q]`  | Number of queries (QdCount). `[0q]` = no queries. `[2q]` = Can be a question asking for a specific PTR and SRV for example.    |
| `5/0/0`         | Registry counting: **Answer / Authority / Additional**. Ex.: 5 in the Answer fiels means we are answering for all 5 register: **PTR**, **SRV**, **TXT**, **A**, **AAAA** and **NSEC**.               |
| `PTR`           | Points a service name to the instance  (`_http._tcp.local.` → service).|
| `SRV`           | Contains the host name, port, priority and wheigt.       |
| `TXT`           | Service metadata (key, value).                                  |
| `A`             | IPv4 record.                                         |
| `AAAA`          | IPv6 record.                                         |
| `NSEC`          | Cache coerence. (indicates the ausence of other types).        |
| `(Cache flush)` | Old records on cach must be discarded.               |
| `TTL`              | Time to keep the record on cache. If equals to zero, indicates the service is not available anymore|


First packets announces a service and a device:
``` text 
18:45:10.112345 IP 192.168.1.50.mdns > 224.0.0.251.mdns: 0*- [0q] 1/0/4 PTR MyDevice._ServiceType._tcp.local. (125)
```
Subsequent servies announces full details about the service, IP and Port:
``` text
18:45:10.325678 IP 192.168.1.50.mdns > 224.0.0.251.mdns: 0*- [0q] 5/0/0 PTR MyDevice._ServiceType._tcp.local., (Cache flush) SRV ServiceName.MyDevice._tcp.local.:ServicePort 0 0, (Cache flush) TXT "versao=1.0", (Cache flush) A 192.168.1.50, (Cache flush) NSEC (200)
```
# Discovery architecture
The discovery and gateway election process cas be described as the following diagram:

![](./docs/discover-announcer-sequence.svg)

The Discovery thread of each device waits for an event within a defined timeout. If no gateway is found, the system assumes itself as a gateway device and register it's service on the network. Every Dinasore subsequently started will search and find the previous gateway device and start announcing itself as a worker device.