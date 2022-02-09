# ----------- Other module files ------------
import colorama

import config
import utils
import operations
from shared_imports import *
import psutil
from tabulate import tabulate
from utils import get_size

# ----------- Standard Libraries ------------
def CPU():
    clear_command = "cls" if platform.system() == "Windows" else "clear"
    os.system(clear_command)
    print("\n" + "-"*30 + f"===== {F.LIGHTCYAN_EX}CPU{S.RESET_ALL} =====" + "-"*30)

    cpufreq = psutil.cpu_freq()

    print(tabulate([[psutil.cpu_count(logical=False), psutil.cpu_count(logical=True), f"{cpufreq.min:.2f}Mhz",
                     f"{cpufreq.max:.2f}Mhz", f"{cpufreq.current:.2f}Mhz"]],
                    headers=("Physical Cores", "Total Cores", "Min Frequency", "Max Frequency", "Current Frequency")))

    input("Press ENTER to return to the previous screen...")

def GPU():
    pass

def RAM():
    clear_command = "cls" if platform.system() == "Windows" else "clear"
    os.system(clear_command)
    print("\n" + "-" * 30 + f"===== {F.LIGHTCYAN_EX}RAM{S.RESET_ALL} =====" + "-" * 30)

    print("\n No information to show here yet :(")
    input("Press ENTER to return to the previous screen...")

def Disk():
    clear_command = "cls" if platform.system() == "Windows" else "clear"
    os.system(clear_command)
    print("\n" + "-" * 30 + f"===== {F.LIGHTCYAN_EX}Disk{S.RESET_ALL} =====" + "-" * 30)

    partitions = []

    for partition in psutil.disk_partitions():

        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue

        partitions.append([partition.device, partition.mountpoint, partition.fstype,
                           f"{get_size(partition_usage.used)}/{get_size(partition_usage.total)} ({partition_usage.percent}%)"])

    print(tabulate(partitions,
                   headers=("Device", "Mountpoint", "File system type", "Total size", "Usage")))

    input("\nPress ENTER to return to the previous screen...")

def Network():
    clear_command = "cls" if platform.system() == "Windows" else "clear"
    os.system(clear_command)
    print("\n" + "-" * 30 + f"===== {F.LIGHTCYAN_EX}Disk{S.RESET_ALL} =====" + "-" * 30)

    print("\n" + "-" * 30 + f"===== {F.LIGHTCYAN_EX}Network{S.RESET_ALL} =====" + "-" * 30)

    mac = []
    ip = []

    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:

            if str(address.family) == 'AddressFamily.AF_INET':
                ip.append([address.address, address.netmask, address.broadcast])
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                mac.append([address.address, address.netmask, address.broadcast])

    if len(ip) > 0:
        print(tabulate(ip, headers=("IP Address", "Netmask", "Broadcast")))
        print()
    if len(mac) > 0:
        print(tabulate(mac, headers=("Mac Address", "Netmask", "Broadcast")))
    input("\nPress ENTER to return to the previous screen...")

# ------------ Program Start -------------

def main():
    colorama.init()
    # The system needs to be running python 3.6 or higher for f-strings
    global log
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        print("Error Code U001: This program requires running python 3.6 or higher. You are running python " +
              str(sys.version_info[0]) + "." + str(sys.version_info[1]))
        input("Press Enter to exit...")
        sys.exit()

    clear_command = "cls" if platform.system() == "Windows" else "clear"
    os.system(clear_command)

    S.R = S.RESET_ALL
    F.R = F.RESET
    B.R = B.RESET

    config_file = config.config("assets\configs\config.json")

    os.system(clear_command)
    # -------------- Start showing program ---------------------
    print(f"{F.YELLOW}\n========================== Hardware Monitor =========================={S.R}")
    print("======================================================================")
    print("===================== Author: Lukas Anthonissen ======================")

    print("\nNOTES: This program is currently configured for Windows 10 and Linux.")
    print("     Other operating systems to follow in future updates\n")

    print(f"\n> Enter '{F.GREEN}M{S.R}' at any prompt to return to this page")
    print(f"> Enter '{F.GREEN}X{S.R}' now to exit")

    print("\n\n---------------------------- Monitoring Options ----------------------------")
    print(f"      1. Show {F.LIGHTCYAN_EX}all statistics{S.R}.")
    print(f"      2. Show {F.LIGHTCYAN_EX}specific statistics{S.R} according to config file.")
    print(f"      3. Show {F.LIGHTCYAN_EX}CPU{S.R} information.")
    print(f"      4. Show {F.LIGHTCYAN_EX}GPU{S.R} information.")
    print(f"      5. Show {F.LIGHTCYAN_EX}Memory{S.R} information.")
    print(f"      6. Show {F.LIGHTCYAN_EX}Disk{S.R} information.")
    print(f"      7. Show {F.LIGHTCYAN_EX}Network{S.R} information.")
    print("------------------------------ Other Options -------------------------------")
    print(f"      8. Configure {F.LIGHTCYAN_EX}config file{S.R}.")
    print(f"      9. Check for and download {F.LIGHTCYAN_EX}updates{S.R}.")

    choice = input("\nChoice (1-9): ")

    # ------------ Choices ------------------------\
    if choice == 'X':
        os.system(clear_command)
        sys.exit()
    elif choice == '1':
        if config_file['log_file'] == 'ask':
            log = utils.user_answer(input("\nSave recorded statistics to log file? (y/n)... "))
        elif config_file['log_file'] == 'always':
            log = True
        elif config_file['log_file'] == 'never':
            log = False

        operations.main_loop(config.config("assets\configs\default.json"), log, platform.system())

    elif choice == '2':
        if config_file['log_file'] == 'ask':
            log = utils.user_answer(input("\nSave recorded statistics to log file? (y/n)... "))
        elif config_file['log_file'] == 'always':
            log = True
        elif config_file['log_file'] == 'never':
            log = False
        operations.main_loop(config_file, log, platform.system())

    elif choice == '3':
        CPU()
    elif choice == '4':
        GPU()
    elif choice == '5':
        RAM()
    elif choice == '6':
        Disk()
    elif choice == '7':
        Network()
    elif choice == '8':
        pass
    elif choice == '9':
        pass

while True:
    main()