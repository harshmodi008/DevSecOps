# recon.py
# NOTE: This Python script is for GitHub secrets scanning using popular open-source tools.

import os
import subprocess
import sys
import shutil

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

TOOLS = [
    ("trufflehog", ["trufflehog", "filesystem", "."], "trufflehog.txt"),
    ("gitleaks", ["gitleaks", "detect", "--source=.", "--report-format=json", "--report-path=../gitleaks.json"], "gitleaks.json"),
    ("git-all-secrets", ["git-all-secrets", "-r", ".", "-o", "../gitallsecrets.txt", "--no-banner"], "gitallsecrets.txt"),
    ("detect-secrets", ["detect-secrets", "scan"], "detect-secrets.json"),
]

def clone_repo(repo_url):
    print(f"{YELLOW}[+] Cloning {repo_url}{RESET}")
    os.makedirs("github_secrets_output", exist_ok=True)
    os.chdir("github_secrets_output")
    if os.path.exists("repo"):
        shutil.rmtree("repo")
    subprocess.run(["git", "clone", "--depth=1", repo_url, "repo"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists("repo"):
        print(f"{RED}Failed to clone repository.{RESET}")
        sys.exit(1)
    os.chdir("repo")

def run_tools():
    for name, cmd, outfile in TOOLS:
        print(f"{GREEN}[+] Running {name}...{RESET}")
        with open(f"../{outfile}", "w") as f:
            try:
                subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, text=True)
            except Exception as e:
                print(f"{RED}Error running {name}: {e}{RESET}")

def summarize_results():
    os.chdir("..")
    for filename in [x[2] for x in TOOLS]:
        print(f"\n{YELLOW}[*] Showing results from: {filename}{RESET}")
        try:
            with open(filename, "r") as f:
                lines = f.readlines()[:20]
                for line in lines:
                    print(line.strip())
                print(f"{RED}...Output truncated... See full in github_secrets_output/{filename}{RESET}")
        except FileNotFoundError:
            print(f"{RED}File not found: {filename}{RESET}")

def main():
    if len(sys.argv) != 2:
        print(f"{YELLOW}Usage: python3 recon.py <github-repo-url>{RESET}")
        print(f"{YELLOW}Example: python3 recon.py https://github.com/org/repo{RESET}")
        sys.exit(1)

    repo_url = sys.argv[1]
    clone_repo(repo_url)
    run_tools()
    summarize_results()

if __name__ == "__main__":
    main()

"""
Installation Instructions:

pip install trufflehog detect-secrets
brew install gitleaks   # or use curl install script
pip install git+https://github.com/anshumanbh/git-all-secrets.git
"""
