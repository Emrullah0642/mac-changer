#!/usr/bin/env python3
"""
mac_changer.py - A command-line tool to change the MAC address of a network interface.

Usage:
    sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
    sudo python3 mac_changer.py -i wlan0 -r

Requirements:
    - Linux OS
    - Root / sudo privileges
    - net-tools (ifconfig) installed
"""

import subprocess
import argparse
import re
import random
import sys
import os

GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def get_random_mac() -> str:
    """Generate and return a random, locally-administered unicast MAC address."""
    mac = [
           0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def is_valid_mac(mac: str) -> bool:
    """Return True if *mac* matches the standard XX:XX:XX:XX:XX:XX format."""
    pattern = r"^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})$"
    return bool(re.match(pattern, mac))


def get_user_input() -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description="MAC Changer — change or randomize a network interface's MAC address.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55\n"
            "  sudo python3 mac_changer.py -i wlan0 -r\n"
        ),
    )
    parser.add_argument(
        "-i", "--interface",
        dest="interface",
        required=True,
        help="Target network interface (e.g. eth0, wlan0)",
    )
    parser.add_argument(
        "-m", "--mac",
        dest="new_mac",
        help="New MAC address to assign (format: XX:XX:XX:XX:XX:XX)",
    )
    parser.add_argument(
        "-r", "--random",
        action="store_true",
        help="Generate and assign a random MAC address",
    )

    args = parser.parse_args()

    if not args.new_mac and not args.random:
        parser.error(f"{RED}[-] Error: Please specify a MAC address (-m) or use the random flag (-r).{RESET}")

    return args


def get_current_mac(interface: str)-> str | None:
    """
    Read and return the current MAC address of *interface*.

    Returns None if the interface does not exist or the MAC cannot be parsed.
    """
    try:
        output = subprocess.check_output(
            ["ifconfig", interface], stderr=subprocess.STDOUT
        ).decode("utf-8")
        
        # Modern Linux 'ifconfig' output uses 'ether'
        match = re.search(r"ether\s+([0-9a-fA-F:]{17})", output)
    
        if not match:
            # Fallback for older distributions
            match = re.search(r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})", output)

        return match.group(1) if match else None
    except subprocess.CalledProcessError:
        print(
            f"{RED}[-] Error: Could not read interface '{interface}'. "
            f"Check that it exists and is accessible.{RESET}"
        )
        return None


def change_mac(interface: str, new_mac: str) -> None:
    """
    Change the MAC address of *interface* to *new_mac*.

    Raises:
        SystemExit: if *new_mac* has an invalid format.
        subprocess.CalledProcessError: if any ifconfig command fails.
    """
    if not is_valid_mac(new_mac):
        print(f"{RED}[-] Error: Invalid MAC address format!{RESET}")
        sys.exit(1)

    print(f"{BLUE}[*] Shutting down {interface}...{RESET}")
    subprocess.run(["ifconfig",interface,"down"], check=True)
    print(f"{BLUE}[*] Changing MAC for {interface} to {new_mac}...{RESET}")
    subprocess.run(["ifconfig",interface,"hw","ether",new_mac], check=True)
    print(f"{BLUE}[*] Powering up {interface}...{RESET}")
    subprocess.run(["ifconfig",interface,"up"], check=True)

if __name__ == "__main__":
    # Root privilege check
    if os.getuid() != 0:
        print(f"{RED}[!] Error: This script must be run with sudo/root privileges.{RESET}")
        sys.exit(1)

    args = get_user_input()

    target_mac = get_random_mac() if args.random else args.new_mac

    current_mac = get_current_mac(args.interface)
    if not current_mac:
        sys.exit(1)

    print(f"{GREEN}[+] Current MAC : {current_mac}{RESET}")
    print(f"{GREEN}[+] Target  MAC : {target_mac}{RESET}")

   
        
    try:
        change_mac(args.interface, target_mac)

        final_mac = get_current_mac(args.interface)
        if final_mac and final_mac.lower() == target_mac.lower():
            print(f"{GREEN}[+] Success! MAC address changed to: {final_mac}{RESET}")
        else:
            print(f"{RED}[-] Failed: MAC address did not change as expected.{RESET}")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"{RED}[-] A system command failed: {e}{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}[-] Unexpected error: {e}{RESET}")
        sys.exit(1)
