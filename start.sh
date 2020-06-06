#!/bin/sh

source ./bin/activate
export FLASK_APP="src/main.py"

CONTAINER_NAME="groupme_neo4j"

trap_ctrlc () {
    # perform cleanup here
    echo "Ctrl-C caught...performing clean up"
    # Once done, this will run.
    docker stop $CONTAINER_NAME
}
 
# initialise trap to call trap_ctrlc function
# when signal 2 (SIGINT) is received
trap "trap_ctrlc" 2

docker container ls -a | grep $CONTAINER_NAME
RESULT=$?

if [ $RESULT -gt 0 ]
then
    sh "./setup_docker.sh"
else
    docker start $CONTAINER_NAME
fi

flask run 

trap "trap_ctrlc" 2
exit 0
