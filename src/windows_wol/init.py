import argparse
import os
import socket
import subprocess
from dotenv import load_dotenv

load_dotenv()
MAC = os.getenv("P3_MAC")
BROADCAST = os.getenv("BROADCAST", "255.255.255.255")
TARGET_IP = os.getenv("P3_IP")

def send_wol(mac_addr: str):
    """发送WOL魔术包"""
    mac_bytes = bytes.fromhex(mac_addr.replace(":", "").replace("-", ""))
    magic_packet = b"\xff" * 6 + mac_bytes * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(magic_packet, (BROADCAST, 9))
    print(f"✅ WOL魔术包已发送 MAC:{mac_addr}")

def ping_host(ip: str) -> bool:
    """ping检测主机是否在线"""
    try:
        subprocess.check_output(
            ["ping", "-c", "1", "-W", "1", ip],
            stderr=subprocess.STDOUT,
            text=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    parser = argparse.ArgumentParser(description="WOL工具 for P3784 Windows")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # wake 开机
    sub.add_parser("wake", help="发送WOL唤醒P3784")
    # status 状态探测
    sub.add_parser("status", help="Ping检测P3784在线状态")

    args = parser.parse_args()
    if args.cmd == "wake":
        send_wol(MAC)
    elif args.cmd == "status":
        online = ping_host(TARGET_IP)
        print(f"P3784 {'🟢在线' if online else '🔴离线'}")

if __name__ == "__main__":
    main()
