import socket
import threading
from queue import Queue
import time
import os

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3389, 8080]

def scan_port(ip, port, timeout=1, verbose=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            if verbose:
                print(f"Port {port} est OUVERT sur {ip}")
            return port
        else:
            if verbose:
                print(f"Port {port} est FERMÉ sur {ip}")
            return None
    except socket.gaierror:
        if verbose:
            print(f"Hostname could not be resolved: {ip}")
        return None
    except socket.error as e:
        if verbose:
            print(f"Couldn't connect to server {ip} on port {port}: {e}")
        return None
    finally:
        sock.close()

def simple_port_scan(ip, ports=COMMON_PORTS, timeout=1, verbose=False):
    print(f"\nScan de ports mono-thread pour {ip}...")
    open_ports = []
    for port in ports:
        if scan_port(ip, port, timeout, verbose):
            open_ports.append(port)
    print(f"Scan mono-thread pour {ip} terminé. Ports ouverts: {open_ports if open_ports else 'Aucun'}")
    return {ip: open_ports}

class ThreadedPortScanner:
    def __init__(self, ips, ports=COMMON_PORTS, timeout=1, num_threads=10, verbose=False):
        self.ips = ips
        self.ports = ports
        self.timeout = timeout
        self.num_threads = num_threads
        self.verbose = verbose
        self.open_ports_results = {}
        self.queue = Queue()
        self.lock = threading.Lock()

    def _worker(self):
        while True:
            ip, port = self.queue.get()
            if ip is None:
                break
            
            opened_port = scan_port(ip, port, self.timeout, self.verbose)
            
            if opened_port:
                with self.lock:
                    if ip not in self.open_ports_results:
                        self.open_ports_results[ip] = []
                    self.open_ports_results[ip].append(opened_port)
            self.queue.task_done()

    def run_scan(self):
        print(f"\nScan de ports multi-thread (avec {self.num_threads} threads) pour les IPs: {self.ips}...")
        start_time = time.time()

        for ip in self.ips:
            self.open_ports_results[ip] = [] 
            for port in self.ports:
                self.queue.put((ip, port))

        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)

        self.queue.join()

        for _ in range(self.num_threads):
            self.queue.put((None, None))
        for thread in threads:
            thread.join()

        end_time = time.time()
        print(f"Scan multi-thread terminé en {end_time - start_time:.2f} secondes.")
        return self.open_ports_results

def multi_threaded_port_scan(ips, ports=COMMON_PORTS, timeout=1, num_threads=10, verbose=False):
    scanner = ThreadedPortScanner(ips, ports, timeout, num_threads, verbose)
    return scanner.run_scan()