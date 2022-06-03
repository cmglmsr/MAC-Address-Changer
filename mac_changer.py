#!/usr/bin/env python

import subprocess
import optparse
import re

# Add shell options to read arguments from the command line
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help=" Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help=" New MAC address")
    return parser.parse_args()

# Execute commands to change the MAC Address
def change_mac( interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"]) 
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

# Check if the arguments are proper and return the current MAC Address
def check_result( interface, new_mac):
    if not interface:
        print("[-] Please specify an interface.")
    elif not new_mac:
        print("[-] Please specify a MAC address.")

    output = subprocess.check_output(["ifconfig", interface])
    changed_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(output))

    if changed_mac:
        return changed_mac.group(0)
    else:
        print("[-] MAC address could not be found.")


(options, arguments) = get_arguments()
result_mac = check_result( options.interface, options.new_mac)
print("Current MAC: " + str(result_mac))

change_mac(options.interface, options.new_mac)
result_mac = check_result( options.interface, options.new_mac)

if result_mac == options.new_mac:
    print( "[+] MAC Address was successfully changed to " + options.new_mac)
else:
    print("[-] MAC Address could not be changed.")
