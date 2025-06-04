import socket, argparse, concurrent.futures, sys

def scan_port(ip, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return port, "Ouvert" if s.connect_ex((ip, port)) == 0 else "Fermé"
    except socket.timeout:
        return port, "Fermé (Timeout)"
    except socket.error:
        return port, "Fermé (Erreur)"

def main():
    p = argparse.ArgumentParser(description="Scanner de ports multithreadé.")
    p.add_argument("--ip", required=True)
    p.add_argument("--start-port", type=int, default=1)
    p.add_argument("--end-port", type=int, default=1024)
    p.add_argument("-t", "--threads", type=int, default=1)
    p.add_argument("-k", "--timeout", type=float, default=0.5)
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-o", "--output")
    a = p.parse_args()

    try:
        ip = socket.gethostbyname(a.ip)
    except socket.gaierror:
        print(f"[!] Adresse invalide: {a.ip}"); sys.exit(1)

    if not (1 <= a.start_port <= a.end_port <= 65535) or a.threads <= 0 or a.timeout <= 0:
        print("[!] Paramètres invalides."); sys.exit(1)

    print(f"[*] Scan de {ip} (ports {a.start_port}-{a.end_port}) avec {a.threads} threads, timeout {a.timeout}s.")
    ports = range(a.start_port, a.end_port + 1)
    if not ports:
        print("[*] Aucune plage de ports à scanner."); sys.exit(0)

    print("[*] Scan en cours...")
    results, open_ports = [], []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=a.threads) as ex:
            futures = {ex.submit(scan_port, ip, port, a.timeout): port for port in ports}
            for f in concurrent.futures.as_completed(futures):
                try:
                    port, status = f.result()
                except Exception as e:
                    port, status = futures[f], "Fermé (Erreur Interne)"
                    if a.verbose: print(f"Port {port}: {status} ({e})")
                else:
                    if status == "Ouvert":
                        open_ports.append(port); print(f"Port {port}: Ouvert")
                    elif a.verbose:
                        print(f"Port {port}: {status}")
                results.append((port, status))
    except KeyboardInterrupt:
        print("\n[!] Scan interrompu.")
    except Exception as e:
        print(f"\n[!] Erreur: {e}")

    open_ports.sort(); results.sort()
    print("\n===== RÉSUMÉ DU SCAN =====")
    if open_ports:
        print("Ports Ouverts:\n " + "\n ".join(map(str, open_ports)))
    else:
        print("Aucun port ouvert trouvé.")
        if a.verbose: print("(Mode verbose actif : détails affichés ci-dessus.)")

    if a.output:
        try:
            with open(a.output, 'w') as f:
                f.write("Port,Statut\n")
                for port, status in results:
                    if status == "Ouvert" or a.verbose:
                        f.write(f"{port},{status}\n")
            print(f"\n[+] Résultats sauvegardés dans {a.output}")
        except IOError as e:
            print(f"[!] Erreur d'écriture: {e}")
    
    print("[*] Scan terminé.")

if __name__ == "__main__":
    main()