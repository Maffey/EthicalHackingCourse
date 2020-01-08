#! /usr/bin/env python3
# network_scanner.py - A network scanner which uses Scapy to find out info about a network.
# Python 2.7 and 3.7 compatible.

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="target address or network to scan")
    arguments = parser.parse_args()
    if arguments.target is None:
        parser.error("[-] please specify a target, use --help for more information")

    return arguments


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_frame / arp_request
    answered = scapy.srp(arp_packet, timeout=1, verbose=False)[0]

    clients_list = []
    for answer in answered:
        client_dict = {"ip": answer[1].psrc, "mac": answer[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("".center(40, "="))
    print("IP\t\t\tMAC Address")
    print("".center(40, "="))

    for result in results_list:
        print(result["ip"] + "\t\t" + result["mac"])


args = get_arguments()
print_result(scan(args.target))