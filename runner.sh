#!/bin/bash

# Path to the monitoring script
MONITOR_SCRIPT="./mon.sh"

# Path to the Python script
PYTHON_SCRIPT="experiment.py"

# Start the monitoring script in the background and capture its PID
bash $MONITOR_SCRIPT &
MONITOR_PID=$!

echo "Started GPU and Memory monitoring script with PID: $MONITOR_PID"
sleep 5
# Run the Python script and wait for it to finish
python3 $PYTHON_SCRIPT

# After the Python script finishes, kill the monitoring script
echo "Python script finished. Stopping monitoring script..."
kill $MONITOR_PID

# Ensure the monitoring script has stopped
wait $MONITOR_PID 2>/dev/null

echo "Monitoring script stopped."
