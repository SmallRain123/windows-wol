import argparse
import os
import socket
import subprocess
import time
from dotenv import load_dotenv

load_dotenv()
MAC_ENV = os.getenv("P3_MAC")
BROADCAST = os.getenv("BROADCAST", "255.255.255.255")
TARGET_IP_ENV = os.getenv("P3_IP")
MCP_PORT = int(os.getenv("MCP_PORT", "8090"))

def send_wol(mac_addr: str):
    mac_clean = mac_addr.replace(":", "").replace("-", "")
    mac_bytes = bytes.fromhex(mac_clean)
    magic_packet = b"\xff" * 6 + mac_bytes * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(magic_packet, (BROADCAST, 9))
    print(f"✅ WOL魔术包已发送, MAC: {mac_addr}")

def ping_host(ip: str) -> bool:
    try:
        subprocess.check_output(
            ["ping", "-c", "1", "-W", "1", ip],
            stderr=subprocess.STDOUT,
            text=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def check_port(ip:str, port:int, timeout=1) -> bool:
    try:
        with socket.socket() as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except Exception:
        return False

def wait_mcp_ready(target_ip, max_wait=120):
    print(f"⏳ 等待主机 {target_ip} 开机与windows-mcp就绪，最长等待{max_wait}秒")
    start = time.time()
    while time.time() - start < max_wait:
        if ping_host(target_ip):
            print(f"🟢 Ping {target_ip} 成功，检测MCP端口8090...")
            if check_port(target_ip, MCP_PORT):
                print("✅ windows-mcp 8090端口就绪！")
                return True
        time.sleep(3)
    print("❌ 超时，MCP服务未就绪")
    return False

def main():
    parser = argparse.ArgumentParser(description="WOL工具 for P3784 Windows")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # wake子命令：--mac
    parser_wake = sub.add_parser("wake", help="发送WOL魔术包唤醒主机")
    parser_wake.add_argument("--mac", type=str, help="MAC地址，例 BC:38:98:A5:F0:00，不传读取.env")

    # status子命令：--ip
    parser_status = sub.add_parser("status", help="Ping检测主机在线状态")
    parser_status.add_argument("--ip", type=str, help="目标主机IP，不传读取.env")

    # wait子命令：--ip
    parser_wait = sub.add_parser("wait", help="等待windows-mcp 8090端口就绪")
    parser_wait.add_argument("--ip", type=str, help="目标主机IP，不传读取.env")

    args = parser.parse_args()

    if args.cmd == "wake":
        mac = args.mac or MAC_ENV
        if not mac:
            print("❌ 缺少MAC：要么--mac指定，要么.env配置P3_MAC")
            return
        send_wol(mac)

    elif args.cmd == "status":
        ip = args.ip or TARGET_IP_ENV
        if not ip:
            print("❌ 缺少IP：要么--ip指定，要么.env配置P3_IP")
            return
        online = ping_host(ip)
        print(f"主机 {ip} {'🟢在线' if online else '🔴离线'}")

    elif args.cmd == "wait":
        ip = args.ip or TARGET_IP_ENV
        if not ip:
            print("❌ 缺少IP：要么--ip指定，要么.env配置P3_IP")
            return
        wait_mcp_ready(ip)

if __name__ == "__main__":
    main()

