#!/usr/bin/env python3
import subprocess
import os
import sys
from datetime import datetime

# ANSI color codes for console
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def run_command(command, title):
    print(f"{Colors.HEADER}[+] {title}{Colors.ENDC}")
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"{Colors.FAIL}Error running {title}: {e}{Colors.ENDC}\n"

def save_output(filename, section_title, content):
    with open(filename, "a") as f:
        f.write(f"\n===== {section_title} =====\n")
        f.write(content + "\n")

def run_tools(domain, output_file):
    tools = [
        (f"subfinder -d {domain} -silent", "Subfinder"),
        (f"amass enum -passive -d {domain}", "Amass Passive"),
        (f"assetfinder --subs-only {domain}", "Assetfinder"),
        (f"sublist3r -d {domain} -o sublist3r.txt && cat sublist3r.txt", "Sublist3r")
    ]
    
    all_subs = set()
    for cmd, name in tools:
        result = run_command(cmd, f"Running {name}")
        save_output(output_file, name, result)
        all_subs.update(result.splitlines())

    # Save all subs for DNSx and screenshots
    with open("all_subs.txt", "w") as f:
        for sub in sorted(all_subs):
            f.write(sub + "\n")

    # DNSx
    dnsx_cmd = "cat all_subs.txt | dnsx -silent"
    dnsx_result = run_command(dnsx_cmd, "Running DNSx")
    save_output(output_file, "DNSx", dnsx_result)

    # WHOIS
    whois_result = run_command(f"whois {domain}", "Running WHOIS")
    save_output(output_file, "WHOIS", whois_result)

    # GeoIP (using ipinfo.io)
    ipinfo_result = run_command(f"curl -s ipinfo.io/{domain}", "IPInfo Lookup")
    save_output(output_file, "IP Geolocation", ipinfo_result)

    # Screenshot using gowitness
    gowitness_cmd = "gowitness file -f all_subs.txt --timeout 10"
    screenshot_result = run_command(gowitness_cmd, "Capturing Screenshots with gowitness")
    save_output(output_file, "gowitness", screenshot_result)

    # Nuclei scan
    nuclei_cmd = "cat all_subs.txt | nuclei -silent"
    nuclei_result = run_command(nuclei_cmd, "Running Nuclei")
    save_output(output_file, "Nuclei", nuclei_result)

    # Optional: cleanup
    os.remove("all_subs.txt")
    if os.path.exists("sublist3r.txt"):
        os.remove("sublist3r.txt")

def main():
    if len(sys.argv) != 2:
        print(f"{Colors.WARNING}Usage: python3 recon_tool.py <domain.com>{Colors.ENDC}")
        sys.exit(1)

    domain = sys.argv[1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"recon_{domain}_{timestamp}.txt"

    banner = f"{Colors.OKGREEN}Reconnaissance Report for {domain} - {timestamp}{Colors.ENDC}\n"
    print(banner)
    save_output(output_file, "Recon Start", banner)

    run_tools(domain, output_file)

    print(f"{Colors.OKGREEN}Recon complete. Output saved to {output_file}{Colors.ENDC}")

if __name__ == "__main__":
    main()
