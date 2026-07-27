#!/bin/bash

echo "Clearing system caches..."
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

echo "Setting CPU governor to performance..."
for CPUFREQ in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
  echo performance | sudo tee $CPUFREQ > /dev/null
done

echo "Disabling Turbo Boost..."
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

echo "Clearing Python caches..."
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

echo "System ready for clean experiment."

echo "=================================="
echo " Starting All Energy Measurements "
echo "=================================="

# You can add/remove scripts here
DATASETS=("bank" "exam" "drug" "water")
SLEEP_DURATION=5

for DATASET in "${DATASETS[@]}"
do
  echo "Running on measure_"$DATASET"_dask.py"
  sudo python3 measure_"$DATASET"_dask.py

  echo "Sleeping for $SLEEP_DURATION seconds before next script..."
  sleep $SLEEP_DURATION
done

echo " All Runs Complete "