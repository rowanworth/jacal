#!/bin/bash

#set -x

waitNodeManager()
{ # Attempting to start NodeManager but timeout after 10 seconds
    echo -n Waiting for Node manager to startup...
    TIMEOUT=10
    STATUS=1
    while [ $STATUS -ne 0 ] && [ $TIMEOUT -ne 0 ]; do
        dlg nm -v --no-dlm &
        NMPID=$! 
        STATUS=$?
        TIMEOUT=`expr $TIMEOUT - 1`
        sleep 1
    done

    if [ $TIMEOUT -eq 0 ]; then
        echo FAILED
    else
        echo STARTED
    fi
}
waitDIManager()
{ # Wait for daliuge to start, but timeout after 10 seconds
    echo -n Waiting for DIM to startup...
    TIMEOUT=10
    STATUS=1
    while [ $STATUS -ne 0 ] && [ $TIMEOUT -ne 0 ]; do
        dlg dim -N localhost &
        DMPID=$! 
        STATUS=$?
        TIMEOUT=`expr $TIMEOUT - 1`
        sleep 1
    done

    if [ $TIMEOUT -eq 0 ]; then
        echo FAILED
    else
        echo STARTED
    fi
}
runBasicTest()
{ # Wait for daliuge to start, but timeout after 10 seconds
    echo -n Starting basic test
    TIMEOUT=10
    dlg unroll-and-partition -L ./simple_calibration.json -a metis | sed 's/DynlibApp/DynlibProcApp/g' | dlg map -N localhost,localhost -i 1 | dlg submit -H localhost -p 8001

}
cleanup()
{
source cleanup.cfg

kill $NMPID
kill $DMPID
wait $NMPID
wait $DMPID
echo "STOPPED"


}

# Setup the environment
source local.cfg
echo $ASKAP_ROOT

# Create directories library, data and parset location
# Start the registry

waitNodeManager
waitDIManager

# read -n1 -r -p "Press any key to start the test..." key
sleep 5 
# Run the tests
runBasicTest

#read -n1 -r -p "Press any key to shutdown" key

# Request IceGrid shutdown and wait
echo -n "Stopping NM and DIM..."
# Remove temporary directories

#cleanup

# exit $STATUS
