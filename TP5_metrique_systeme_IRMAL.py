import psutil, os, time, sys

def clear(): os.system('cls' if os.name == 'nt' else 'clear')
def to_gb(b): return b / (1024**3)

def get_dashboard_output():
    lines = []
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"=== Tableau de Bord - {timestamp} ===")

    cpu_total = psutil.cpu_percent(interval=1)
    lines.append(f"\n--- CPU ---\nTotal: {cpu_total:.1f}%")
    for i, pct in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
        lines.append(f"  Cœur {i+1}: {pct:.1f}%")
    bar = '#' * int(cpu_total / 2) + '-' * (50 - int(cpu_total / 2))
    lines.append(f"  [{bar}]")

    mem = psutil.virtual_memory()
    lines.append(f"\n--- RAM ---")
    lines.append(f"Total: {to_gb(mem.total):.2f} Go")
    lines.append(f"Utilisée: {to_gb(mem.used):.2f} Go ({mem.percent:.1f}%)")
    lines.append(f"Libre: {to_gb(mem.available):.2f} Go")

    lines.append(f"\n--- Disque ---")
    for p in psutil.disk_partitions():
        try:
            u = psutil.disk_usage(p.mountpoint)
            lines.append(f"  {p.mountpoint}: {to_gb(u.used):.2f}/{to_gb(u.total):.2f} Go ({u.percent:.1f}%)")
        except: lines.append(f"  {p.mountpoint}: accès refusé")

    net = psutil.net_io_counters()
    lines.append(f"\n--- Réseau ---")
    lines.append(f"Octets envoyés: {to_gb(net.bytes_sent):.2f} Go")
    lines.append(f"Octets reçus: {to_gb(net.bytes_recv):.2f} Go")

    lines.append(f"\n--- Interfaces Réseau ---")
    stats = psutil.net_if_stats()
    pernic = psutil.net_io_counters(pernic=True)
    for iface in stats:
        lines.append(f"  {iface} ({'UP' if stats[iface].isup else 'DOWN'})")
        if iface in pernic:
            i = pernic[iface]
            lines.append(f"    Envoyés: {to_gb(i.bytes_sent):.2f} Go | Reçus: {to_gb(i.bytes_recv):.2f} Go")
            lines.append(f"    Paquets envoyés: {i.packets_sent} | reçus: {i.packets_recv}")

    lines.append(f"\n--- Température CPU ---")
    temps = getattr(psutil, 'sensors_temperatures', lambda: {})()
    if temps:
        for name, entries in temps.items():
            for e in entries:
                lines.append(f"  {name} ({e.label or 'N/A'}): {e.current}°C")
    else:
        lines.append("  Non disponible")

    return "\n".join(lines)

def main():
    input("Appuyez sur Entrée pour lancer le tableau de bord...")
    log_file = "system_dashboard_log.txt"
    
    while True:
        clear()
        dashboard_output = get_dashboard_output()
        print(dashboard_output)

        with open(log_file, "a") as f:
            f.write(dashboard_output + "\n\n")

        print("\nAppuyez sur 'q' pour quitter ou attendez 5s...")

        start = time.time()
        while time.time() - start < 5:
            try:
                if os.name == 'nt':
                    import msvcrt
                    if msvcrt.kbhit() and msvcrt.getch().decode().lower() == 'q':
                        return print("Arrêt.")
                else:
                    import select
                    if select.select([sys.stdin], [], [], 0)[0]:
                        if sys.stdin.read(1).lower() == 'q':
                            return print("Arrêt.")
            except: pass
            time.sleep(0.1)

if __name__ == "__main__":
    main()
