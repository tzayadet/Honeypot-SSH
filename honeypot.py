import paramiko, logging, json, time, os
from datetime import datetime

logging.basicConfig(filename="hp.log", level=logging.INFO, format="%(asctime)s | %(message)s")

class Handler(paramiko.ServerInterface):
    def __init__(self, ip): self.ip = ip
    def check_auth_password(self, u, p):
        logging.info(f"AUTH | u:{u} p:{p} ip:{self.ip}")
        return paramiko.AUTH_SUCCESSFUL
    def check_channel_exec_request(self, ch, cmd):
        logging.info(f"CMD | {cmd.decode()} ip:{self.ip}")
        ch.send(f"Permission denied.\n")
        ch.close()
        return True

if __name__ == "__main__":
    t = paramiko.Transport(("0.0.0.0", int(os.getenv("HP_PORT", "2222"))))
    t.set_gss_host_key(paramiko.RSAKey.generate(2048))
    t.start_server(server=Handler("0.0.0.0"))
    print("[+] Honeypot active")
    while True: time.sleep(1)
