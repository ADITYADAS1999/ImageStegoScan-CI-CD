# 🔐 Automated Docker image Security Scanner  
StegoScan-CI-CD is a GitHub Actions workflow that scans images (.jpg, .png, .jpeg) for steganography payloads, hidden scripts, or malicious content. It automatically generates a security report during CI/CD to detect vulnerable or weaponized images before deployment.





![logo](https://github.com/user-attachments/assets/5ccf6f4b-6e3d-4472-be96-75ddda499fbd)




## 📌 Introduction  

In today’s digital landscape, images are widely used for communication, sharing, and storage. However, they can also be exploited to hide malicious payloads, scripts, or confidential data using steganography techniques. Such weaponized images pose serious threats when uploaded to corporate systems, shared across social platforms, or embedded in software releases.

To mitigate these risks, we developed ImageStegoScan-CI-CD, a GitHub Actions workflow that automatically:

Key Features:  
-  Scans `.jpg`, `.png`, and `.jpeg` images for **hidden payloads**.
-  Extracts and analyzes **metadata** for suspicious content.
-  Detects potential **steganography techniques** used by attackers.
-  Generates **JSON and PDF reports** with compliance mapping.
-   Runs automatically in **GitHub Actions** workflows.
  
---

## 📂 File Structure  



```bash
.
ImageStegoScan-CI-CD/
│
├── .github/workflows/
│   └── image_scan.yml         # GitHub Actions CI/CD pipeline
│
├── images/                    # Sample input images for scanning
│   ├── example-stegano.png
│   ├── img_01.jpg
│   ├── img_02.jpg
│   └── img_03.png
│
├── reports/                   # Output reports after scan
│   └── example.txt
│
├── scripts/
│   └── scan_images.py         # Main script for scanning images
│
├── LICENSE
├── README.md
└── requirements.txt           # Python dependencies

```

**Explanation of structure:**  
- **`.github/workflows`** → CI/CD pipeline definition (`image_scan.yml`) that automatically triggers the image scanning workflow on each commit or pull request.  
- **`images/`** → Stores input image files (`.jpg`, `.png`, `.jpeg`) that will be scanned for steganography or malicious payloads.  
- **`scripts/`** → Contains automation scripts (`scan_images.py`) responsible for scanning images and generating reports.  
- **`reports/`** → Stores the generated scan reports (e.g., text/JSON output). Can be extended to include consolidated PDF reports.  
- **`requirements.txt`** → Lists Python dependencies required for running the scanner (e.g., Pillow, ExifTool bindings, etc.).  
- **`LICENSE`** → License file for the project.  
- **`README.md`** → Documentation file describing the project, usage, and setup instructions.  


---

## 🛠️ Technology Used  

- **Backend:** Python (scripts for image scanning, metadata extraction, and report generation).  
- **Reports/Visualization:**  
  - ReportLab → To generate structured PDF reports (optional extension).  
  - Matplotlib → To generate severity charts and visual analysis (optional extension).  
- **Security Tools:**  
  - **ExifTool** → Extracts and analyzes image metadata for anomalies.  
  - **StegExpose / Steghide (optional)** → Detects steganography payloads in images.  
  - **Custom Python Scripts** → Implements detection logic and scanning automation.  
- **CI/CD:** GitHub Actions (automated scans integrated into the pipeline).  

---

## ⚙️ Workflow & Tools Used  

This project includes a **GitHub Actions workflow** (`.github/workflows/docker-scan.yml`) that automates the **DevSecOps security pipeline**.  
The workflow runs automatically on every push to the `main` branch and executes the following stages:  

---

### 🔹 1. Build Docker Image  
```yaml
- name: Build Docker Image
  run: docker build -t my-custom-app:latest ./docker
```
- Tool: Docker
- Purpose: Builds the application container image from the Dockerfile inside the ./docker directory.
- Output: A containerized application (my-custom-app:latest) that is ready for security scanning.


### 🔹 2. Trivy (Docker Image Vulnerability Scanner)

```
- name: Run Trivy Docker Scan
  run: trivy image --ignore-unfixed --exit-code 0 --format json --output reports/trivy.json my-custom-app:latest
```
- Tool: Trivy
- Purpose: Scans the built Docker image for known vulnerabilities (CVEs) in OS packages and dependencies.
- Output: reports/trivy.json → JSON report containing vulnerability details with severity levels.

### 🔹 3. Bandit (Python Source Code Analysis)

```
- name: Run Bandit Scan
  run: bandit -ll -ii -r . -f json -o reports/bandit.json || true
```
- Tool: Bandit
- Purpose: Performs Static Application Security Testing (SAST) for Python source code.
- Detects issues such as:
-Insecure function usage (eval, exec)
-Hardcoded credentials
-Insecure file permissions
- Output: reports/bandit.json → JSON report of security issues in code.


### 🔹 4. Docker Scout (Optional Dependency Scanner)

```
# docker scout quickview
# docker scout cves
```
- Tool: Docker Scout
- Purpose: Provides insights into container dependencies, image provenance, and supply chain vulnerabilities.
- Benefit: Complements Trivy by analyzing image layers and dependencies more deeply.

### 🔹 5. MITRE ATT&CK (Atomic Red Team Simulation)

```
- name: Run Atomic Red Team (MITRE ATT&CK)
  shell: pwsh
  run: |
    git clone https://github.com/redcanaryco/atomic-red-team.git
    git clone https://github.com/redcanaryco/invoke-atomicredteam.git
    Import-Module ./invoke-atomicredteam/Invoke-AtomicRedTeam.psd1 -Force
    Invoke-AtomicTest T1003 ...
```
- Tools:
-Atomic Red Team
-Invoke-AtomicRedTeam

- Purpose: Simulates MITRE ATT&CK techniques against the container or application.
- Example: T1003 – Credential Dumping test.
- Output: reports/mitre_T1003.json → JSON report mapping vulnerabilities to real-world adversarial behaviors.

### 🔹 6. NIST CSF Mapping

```
- name: Map Results to NIST CSF
  run: python scripts/mappings.py reports/ nist_report.json
```

- Purpose: Maps scan results from Trivy, Bandit, and MITRE ATT&CK into NIST Cybersecurity Framework (CSF) categories:
- Identify → Asset discovery issues
- Protect → Missing patches, insecure configs
- Detect → Intrusion detection gaps
- Respond/Recover → Response & recovery mechanisms

### 🔹 7. Report Generation (Charts + PDF)

```
- name: Generate Charts
  run: python scripts/gen_charts.py

- name: Generate PDF Report
  run: python scripts/generate_report.py
```
- Purpose: Produces a professional PDF report consolidating:
- Vulnerability details
- Severity breakdown (with charts)
- NIST CSF mapping
- MITRE ATT&CK mapping
- OWASP Top 10 mapping


### 🔹 8. Upload Artifacts

```
- name: Upload PDF Report
  uses: actions/upload-artifact@v4
  with:
    name: docker-vulnerability-report
    path: report.pdf
```

- Purpose: Uploads both the PDF report and raw JSON reports as GitHub build artifacts.
- Benefit: Results can be downloaded and reviewed by security teams after each workflow run.






---

## 🎯 Purpose  
The primary purpose of this project is to:  
- **Automate vulnerability management** for Dockerized applications.  
- Provide a **single, consolidated PDF report** instead of multiple scattered outputs.  
- Help developers, DevOps, and security teams **integrate security into CI/CD pipelines (DevSecOps)**.  
- Align findings with **compliance frameworks and attacker models**.  

---

## ✅ Advantages  

- **Automated** → Scans run automatically with every code push (via GitHub Actions).  
- **Comprehensive** → Covers Docker images, source code, and dependencies.  
- **Framework-Aware** → Maps to NIST CSF, MITRE ATT&CK, and OWASP Top 10.  
- **Professional Reports** → PDF reports with charts, severity analysis, and framework mappings.  
- **Open-Source & Extensible** → Easily add new scanners or frameworks.  

---

## ⚡ Challenges Faced  

1. **Data Normalization** → Different scanners produce JSON in different formats.  
2. **Framework Mapping** → Consistently mapping vulnerabilities across NIST, MITRE, and OWASP required custom logic (`mappings.py`).  
3. **PDF Reporting** → Ensuring the final report is clear, visual, and boardroom-ready.  
4. **Automation in CI/CD** → Ensuring scans work smoothly within GitHub Actions with minimal setup.  

---

## 🖼️ Sample Report Preview  

Below is a preview of the kind of report generated by the scanner:  

![Download Vulnerability Test Report](https://github.com/ADITYADAS1999/Automated-Docker-Security-Scanner/blob/main/vulnerability_report.pdf)  

The PDF includes:  
- Vulnerability summary tables.  
- Severity distribution charts.  
- NIST CSF, MITRE ATT&CK, OWASP Top 10 mappings.  
- Final consolidated recommendations.  

---

## 🔚 Conclusion  
The **Automated Docker Security Scanner** provides a **complete security assessment workflow** for containerized applications.  
By integrating scanning tools with industry-standard frameworks, it transforms raw scan data into **actionable insights** that can guide both developers and security teams.  

Future Work:  
- Add real-time **CVE database lookups**.  
- Build a **web dashboard** for interactive vulnerability tracking.  
- Extend support for more programming languages (Go, Java, etc.).  

---

## 📜 License  
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.  






