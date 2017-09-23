#!/bin/bash
screen -S incoming_observer -X quit
screen -S deserialize_observer -X quit
screen -S incoming_observer -dm bash -c "~/source/bcpp/scripts/incoming_observer.sh"
screen -S deserialize_observer -dm bash -c "~/source/bcpp/scripts/deserialize_observer.sh"
