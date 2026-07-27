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
DATASETS=("census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census" "census"  "census" "census" "census" "census" "census" "census" "census" "census" "census" "census")
SLEEP_DURATION=5

RUN=1

for DATASET in "${DATASETS[@]}"
do
  echo "Running on measure_"$DATASET"_dask.py $RUN"
  sudo python measure_"$DATASET"_dask.py $RUN

  echo "Sleeping for $SLEEP_DURATION seconds before next script..."
  sleep $SLEEP_DURATION

  RUN=$((RUN+1))
done

echo " All Runs Complete "