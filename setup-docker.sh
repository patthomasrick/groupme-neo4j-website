#!/bin/sh

CONTAINER_NAME="groupme_neo4j"
CWD=$(pwd)

docker run \
    --name "$CONTAINER_NAME" \
    -p7474:7474 -p7687:7687 \
    -v $CWD/neo4j/data:/data \
    -v $CWD/neo4j/logs:/logs \
    -v $CWD/neo4j/import:/var/lib/neo4j/import \
    -v $CWD/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/groupme \
    -d \
    neo4j:latest