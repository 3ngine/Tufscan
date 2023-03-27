import argparse
import socket
import threading
import time

parser = argparse.ArgumentParser(description='Tufscan | Port Scanner | 1.0.0')
parser.add_argument('--target', dest='host', required=True, help='Target to scan')
parser.add_argument('--sP', dest='start', type=int, default=1, help='Start port [default 1]')
parser.add_argument('--eP', dest='end', type=int, default=1024, help='End port [default 1024]')
parser.add_argument('--threads', dest='threads', type=int, default=10, help='Threads to use [default 10]')

args = parser.parse_args()

open_ports = []

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((args.host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except KeyboardInterrupt:
        exit()
    except:
        pass

def scan_range(start_port, end_port):
    for port in range(start_port, end_port+1):
        scan_port(port)

def chunk_ports(n, num_threads):
    chunk_size = n // num_threads
    return [(i * chunk_size + 1, (i+1) * chunk_size) for i in range(num_threads)]

def scan_ports(num_threads):
    chunks = chunk_ports(args.end - args.start + 1, num_threads)
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=scan_range, args=(chunks[i][0], chunks[i][1]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

start_time = time.time()
scan_ports(args.threads)
print(f"Open ports on {args.host} ({len(open_ports)}): {open_ports}")
print(f"Time taken: {time.time() - start_time} seconds")