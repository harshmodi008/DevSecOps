# alpine, nginx, apache (httpd), mysql, node, python, ubuntu

#!/bin/bash
images=( \
  "alpine" \
  "nginx" \
  "httpd" \
  "mysql" \
  "node" \
  "python" \
  "ubuntu" \
)

for image in "${images[@]}"; do
  echo "[+] Scanning $image"
  trivy image --severity CRITICAL,HIGH --skip-dirs /var/cache $image
done

===========================
 Trivy CLI Cheatsheet
===========================

1. Basic Scan (Local Image)
   trivy image nginx:latest

2. Scan Remote Image
   trivy image docker.io/library/nginx:latest

3. Scan Filesystem/Directory
   trivy fs ./myapp

4. Scan SBOM File
   trivy sbom --format cyclonedx ./sbom.json

5. Output Format Options:
   -f json, table, template, sarif, cyclonedx

6. Filter by Severity:
   trivy image --severity CRITICAL,HIGH nginx

7. Ignore Specific CVEs:
   trivy image --ignore-unfixed --ignorefile .trivyignore nginx

8. Scan for Secrets:
   trivy image --scanners secret node

9. Scan Git Repos:
   trivy repo https://github.com/user/project

10. Save Output to File:
    trivy image -f json -o result.json nginx

*/
