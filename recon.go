// recon.go
package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

func runCommand(command string, args []string, title string) string {
	fmt.Printf("\033[95m[+] %s\033[0m\n", title)
	cmd := exec.Command(command, args...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Sprintf("\033[91mError running %s: %v\033[0m\n", title, err)
	}
	return string(output)
}

func saveOutput(filename, sectionTitle, content string) {
	f, err := os.OpenFile(filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Printf("Error opening file: %v\n", err)
		return
	}
	defer f.Close()
	f.WriteString("\n===== " + sectionTitle + " =====\n")
	f.WriteString(content + "\n")
}

func installTools() {
	fmt.Println("\033[92m[+] Installing required tools...\033[0m")
	tools := []string{
		"go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
		"go install github.com/owasp-amass/amass/v3/...@master",
		"go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest",
		"go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest",
		"go install github.com/sensepost/gowitness@latest",
		"go install github.com/tomnomnom/assetfinder@latest",
		"sudo apt install -y whois curl jq",
		"git clone https://github.com/aboul3la/Sublist3r && cd Sublist3r && sudo pip3 install -r requirements.txt",
	}
	for _, cmd := range tools {
		exec.Command("bash", "-c", cmd).Run()
	}
}

func runRecon(domain, outputFile string) {
	commands := map[string][]string{
		"Subfinder":    {"subfinder", []string{"-d", domain, "-silent"}},
		"Amass Passive": {"amass", []string{"enum", "-passive", "-d", domain}},
		"Assetfinder":  {"assetfinder", []string{"--su
