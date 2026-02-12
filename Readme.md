🔀 MAC Changer
A lightweight command-line tool written in Python to change or randomize the MAC address of any network interface on Linux.

✨ Features

Set a custom MAC address manually
Generate and apply a random MAC address with a single flag
Validates MAC address format before applying changes
Color-coded terminal output for clear feedback
Root privilege check with a friendly error message


📋 Requirements
RequirementDetailsOperating SystemLinux (Debian, Ubuntu, Kali, Arch, etc.)Python3.10 or highernet-toolsifconfig must be installedPrivilegesMust be run as root (sudo)
Install net-tools if missing:
bashsudo apt install net-tools      # Debian / Ubuntu / Kali
sudo pacman -S net-tools        # Arch Linux

🚀 Usage
bashsudo python3 mac_changer.py -i <interface> [-m <mac_address>] [-r]
Arguments
FlagLong formDescription-i--interfaceTarget network interface (e.g. eth0, wlan0)-m--macNew MAC address to assign (XX:XX:XX:XX:XX:XX)-r--randomGenerate and assign a random MAC address
Examples
Assign a specific MAC address:
bashsudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
Assign a random MAC address:
bashsudo python3 mac_changer.py -i wlan0 -r
View help:
bashpython3 mac_changer.py --help

🖥️ Sample Output
[+] Current MAC : 08:00:27:ab:cd:ef
[+] Target  MAC : 00:16:3e:4f:a1:22
[*] Bringing eth0 down ...
[*] Changing MAC address of eth0 to 00:16:3e:4f:a1:22 ...
[*] Bringing eth0 up ...
[+] Success! MAC address changed to: 00:16:3e:4f:a1:22

⚠️ Disclaimer
This tool is intended for educational purposes and authorized network testing only.
Changing MAC addresses on networks you do not own or have explicit permission to test is illegal.
The author takes no responsibility for any misuse of this tool.
