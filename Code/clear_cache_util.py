import subprocess

def clear_caches():
    print("Clearing system caches...")
    subprocess.run(["sync"])
    subprocess.run(["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"])

    print("Setting CPU governor to performance...")
    subprocess.run(["sudo", "bash", "-c", 
        "for CPUFREQ in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; "
        "do echo performance > $CPUFREQ; done"])

    print("Disabling Turbo Boost...")
    subprocess.run(["sudo", "sh", "-c", "echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo"])

    print("Clearing Python caches...")
    subprocess.run(["find", ".", "-type", "d", "-name", "__pycache__", "-exec", "rm", "-r", "{}", "+"])
    subprocess.run(["find", ".", "-type", "f", "-name", "*.pyc", "-delete"])
