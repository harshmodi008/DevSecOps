// recon.go
// NOTE: This Go script is for domain-based recon.
// GitHub secrets scanning tools like TruffleHog, Gitleaks, etc., are added in a separate Bash script below.

package main

// [Go recon code remains unchanged here...]

/*
===========================
 GitHub Secrets Scanner Script
===========================

#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo -e "\033[93mUsage: $0 <github-repo-or-org>\033[0m"
  echo -e "\033[93mExample: $0 https://github.com/org/repo\033[0m"
  exit 1
fi

REPO=$1

GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
RESET="\033[0m"

mkdir -p github_secrets_output
cd github_secrets_output

# Clone repo
echo -e "${YELLOW}[+] Cloning $REPO${RESET}"
git clone --depth=1 $REPO repo 2>/dev/null
cd repo || exit

# TruffleHog
echo -e "${GREEN}[+] Running TruffleHog...${RESET}"
trufflehog filesystem . > ../trufflehog.txt

# Gitleaks
echo -e "${GREEN}[+] Running Gitleaks...${RESET}"
gitleaks detect --source=. --report-format=json --report-path=../gitleaks.json

# git-all-secrets
echo -e "${GREEN}[+] Running git-all-secrets...${RESET}"
git-all-secrets -r . -o ../gitallsecrets.txt --no-banner

# detect-secrets
echo -e "${GREEN}[+] Running detect-secrets...${RESET}"
detect-secrets scan > ../detect-secrets.json

cd ..

# Color-coded summary
for f in trufflehog.txt gitleaks.json gitallsecrets.txt detect-secrets.json; do
  echo -e "\n${YELLOW}[*] Showing results from: $f${RESET}"
  cat "$f" | head -n 20
  echo -e "${RED}...Output truncated... See full in github_secrets_output/$f${RESET}"
done

===========================
 Installation Instructions
===========================

# TruffleHog
pip install trufflehog

# Gitleaks
brew install gitleaks  # or
curl -s https://raw.githubusercontent.com/gitleaks/gitleaks/main/install.sh | bash

# git-all-secrets
pip install git+https://github.com/anshumanbh/git-all-secrets.git

# detect-secrets
pip install detect-secrets
*/
