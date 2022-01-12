# Configuring Metricbeat On Docker

* [Metricbeat](https://www.elastic.co/guide/en/beats/metricbeat/current/running-on-docker.html)

## Contents

1. [Configurations](#configurations)
   * [Image Pulling](#image-pulling)
   * [Metricbeat Configuration File](#metricbeat-configuration-file)
   * [Start Metricbeat Container](#start-metricbeat-container)

## Configurations
  The Docker image provides several methods for configuring Metricbeat. 
  The conventional approach is to provide a configuration file via a volume mount, but it’s also possible to create a custom 
  image with your configuration included.

### Image Pulling

Obtaining Metricbeat for Docker is as simple as issuing a docker pull command against the Elastic Docker registry.

```console
$ docker pull docker.elastic.co/beats/metricbeat:7.8.1
```

### Metricbeat configuration File

We are using Volume mounted configuration , for that  create a configuration file with below details:

metricbeat.docker.yml

```console
metricbeat.config:
  modules:
    path: ${path.config}/modules.d/*.yml
    # Reload module configs as they change:
    reload.enabled: false

metricbeat.autodiscover:
  providers:
    - type: docker
      hints.enabled: true

metricbeat.modules:
- module: docker
  metricsets:
    - "container"
    - "cpu"
    - "diskio"
    - "healthcheck"
    - "info"
    #- "image"
    - "memory"
    - "network"
  hosts: ["unix:///var/run/docker.sock"]
  period: 10s
  enabled: true

processors:
  - add_cloud_metadata: ~

output.elasticsearch:
  hosts: '[hostIp:9200]'
  username: 'username'
  password: 'password'

setup.kibana:
  host: 'hostIp:5601'

```

### Start Metricbeat Container

Execute below command in the same directory where you have your metricbeat.docker.yml file.

* Substitute your Elasticsearch hosts and ports in below command before executing it.
  (Note: If you are running Elasticsearch as a docker container then your host name/ IP should be your Host machines IP not containers.)

```console
$ docker run -d \
  --name=metricbeat \
  --user=root \
  --volume="$(pwd)/metricbeat.docker.yml:/usr/share/metricbeat/metricbeat.yml:ro" \
  --volume="/var/run/docker.sock:/var/run/docker.sock:ro" \
  --volume="/sys/fs/cgroup:/hostfs/sys/fs/cgroup:ro" \
  --volume="/proc:/hostfs/proc:ro" \
  --volume="/:/hostfs:ro" \
  docker.elastic.co/beats/metricbeat:7.8.1 metricbeat -e \
  -E output.elasticsearch.hosts=["elasticsearchHosts:9200"] 
```
* And after successful execution of above command your Metricbeat container will be up and It starts sending metric logs to Elasticsearch.
* You can see a new index created in elasticsearch with name "metricbeat-XXXXXXX" and same you can see into Kibana as well.
* Just add that index pattern into your Kibana and start discovering metric logs into Kibana. 

