Man-in-the-Middle (MitM) mediante ARP Spoofing

Este repositorio contiene un script educativo diseñado para interceptar el tráfico de red entre un host víctima y su puerta de enlace (Gateway). Utiliza la técnica de envenenamiento de tablas ARP para posicionar al atacante en medio de la comunicación.

📋 Requisitos del Sistema
- IP Forwarding: Debe estar habilitado en el host atacante (por ejemplo: `echo 1 > /proc/sys/net/ipv4/ip_forward`)
- Librerías: scapy, time, os

⚙️ Funcionamiento
- Suplantación: El script envía respuestas ARP falsas a la víctima y al router
- Interceptación: Los paquetes pasan por el host atacante antes de ser redirigidos a su destino real
- Restauración: Al finalizar, el script repara las tablas ARP de los nodos afectados para limpiar el rastro del ataque

🛡️ Medidas de Mitigación
- Implementación de Dynamic ARP Inspection (DAI) en switches
- Uso de tablas ARP estáticas en dispositivos críticos
- Configuración de DHCP Snooping para validar la relación IP-MAC

# Man-in-the-Middle (MitM) mediante ARP Spoofing

> **Proyecto educativo** — Envenenamiento ARP para prácticas de Capa 2

## 📖 Descripción

Script educativo en **Python** que realiza ARP spoofing para posicionar al atacante entre una víctima y su gateway. Incluye mecánicas de restauración de ARP y opciones de simulación (`--dry-run`).

⚠️ **AVISO:** Solo ejecutar en laboratorios autorizados.

---

## 📋 Requisitos

| Requisito | Detalle |
|-----------|--------:|
| IP Forwarding | Debe estar habilitado en el atacante (`echo 1 > /proc/sys/net/ipv4/ip_forward`) |
| Librerías | `scapy`, `time`, `os` |
| Privilegios | Root (o `--dry-run`) |

---

## ⚙️ Funcionamiento

- **Suplantación:** Envía ARP replies falsas a víctima y gateway
- **Interceptación:** El tráfico pasa por el atacante
- **Restauración:** Repara las tablas ARP al finalizar

---

## 🚀 Uso

```bash
# Habilitar IP forwarding (Linux)
sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

# Ejecutar (ejemplo)
sudo python3 script.py --iface eth0 --victim-ip 192.168.1.10 --gateway-ip 192.168.1.1

# Simulación sin enviar paquetes
sudo python3 script.py --dry-run --iface eth0 --victim-ip 192.168.1.10 --gateway-ip 192.168.1.1
```

### Opciones principales

```
--iface IFACE        Interfaz de red (default: eth0)
--victim-ip IP       IP de la víctima (obligatorio)
--gateway-ip IP      IP del gateway (obligatorio)
--dry-run            No enviar paquetes; solo simular
```

---

## 🛡️ Medidas de Mitigación

- Implementar **Dynamic ARP Inspection (DAI)**
- Usar **ARP estático** en equipos críticos
- Configurar **DHCP Snooping**

---

## 📸 Evidencias

Coloca capturas en `images/`:

```
images/
└── show_ip_arp.png
```

---

## ⚖️ Legal

Usar solo en entornos de laboratorio con permiso explícito.
