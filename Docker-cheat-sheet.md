docker start 522150a13a36  #docker-elk_elasticsearch
docker start 0c5f9de05dc8  #docker-elk_kibana
docker start a21b6447335b   #docker-elk_logstash 

docker exec -it 99d256a0d066 /bin/bash

Jenkins Token : 112bbce2b771319f426091b743892f05fd


docker run -d \
  --name=metricbeat \
  --user=root \
  --volume="$(pwd)/metricbeat.docker.yml:/usr/share/metricbeat/metricbeat.yml:ro" \
  --volume="/var/run/docker.sock:/var/run/docker.sock:ro" \
  --volume="/sys/fs/cgroup:/hostfs/sys/fs/cgroup:ro" \
  --volume="/proc:/hostfs/proc:ro" \
  --volume="/:/hostfs:ro" \
  docker.elastic.co/beats/metricbeat:7.8.1 metricbeat -e \
  -E output.elasticsearch.hosts=["elasticsearch:9200"]
  
  Welcome@2021
  
  docker run docker.elastic.co/beats/metricbeat:7.8.1 setup -E setup.kibana.host=10.1.0.22:5601 -E output.elasticsearch.hosts=["10.1.0.22:9200"] username="elastic" password="changeme"
