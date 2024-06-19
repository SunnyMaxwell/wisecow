import psutil
import logging
from datetime import datetime
import time
import argparse

logging.basicConfig(filename='./wisecow_Dummy_test/system_health.log', level=logging.INFO)

CPU_THRESHOLD = 10
MEMORY_THRESHOLD = 20
DISK_THRESHOLD = 20
PROCESS_THRESHOLD = 20

def check_cpu(threshold):
    cpu_usage = psutil.cpu_percent(interval=1)
    #print(cpu_usage)
    if cpu_usage > threshold:
        logging.info(f"{datetime.now()}: High memory Usage Detected: {cpu_usage}%")
        return (f"{cpu_usage}%")
    return None

def check_memory(threshold):
    memory_usage = psutil.virtual_memory()
    if memory_usage.percent > threshold:
        logging.info(f"{datetime.now()}: High Memory Usage Detected: {memory_usage.percent}%")
        return (f"{memory_usage.percent}%")
    
    return None

def check_disk(threshold):
    disk_usage = psutil.disk_usage("/")
    #print(disk_usage)
    if disk_usage.percent > threshold:
        logging.info(f"{datetime.now()}: High Disk Usage Detected: {disk_usage.percent}%")
        return (f"{disk_usage.percent}%")
    
    return None

def check_processes(threshold):
    process_count = len(psutil.pids())
    if process_count > threshold:
        logging.info(f"{datetime.now()}: High Number Of Processes Detected: {process_count}")
        return (f"{process_count}")
    return None
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='System Health Checker')
    parser.add_argument('--cpu_threshold', type=int, default=20, help='CPU usage threshold')
    parser.add_argument('--memory_threshold', type=int, default=20, help='Memory usage threshold')
    parser.add_argument('--disk_threshold', type=int, default=20, help='Disk usage threshold')
    parser.add_argument('--process_threshold', type=int, default=20, help='Number of processes threshold')
    parser.add_argument('--interval', type=int, default=10, help='Check interval in seconds')

    args = parser.parse_args()

    while True:
        cpu = check_cpu(args.cpu_threshold)
        memory = check_memory(args.memory_threshold)
        disk = check_disk(args.disk_threshold)
        processes = check_processes(args.process_threshold)

        if cpu:
            print(f"ALERT: High CPU Usage: {cpu}")
        if memory:
            print(f"ALERT: High Memory Usage: {memory}")
        if disk:
            print(f"ALERT: High Disk Usage: {disk}")
        if processes:
            print(f"ALERT: High Number of Processes: {processes}")
        print("=================================================")
        time.sleep(args.interval)
    
