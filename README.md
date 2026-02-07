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

Uso
1. Habilitar IP forwarding en el atacante
2. Ejecutar con permisos de root: `sudo python3 script.py --iface eth0 --victim-ip 192.168.1.10 --gateway-ip 192.168.1.1`

Evidencias
Coloca las capturas de resultado (por ejemplo, `show_ip_arp.png`) en la carpeta `images/` de este repositorio.

Responsable y Legal
Solo para entornos de laboratorio con autorización. No usar en redes de terceros sin permiso.
