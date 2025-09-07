# 🔐 ImageStegoScan-CI-CD Security Scanner  
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

This project includes a **GitHub Actions workflow** (`.github/workflows/image_scan.yml`) that automates the **image steganography security pipeline**.  
The workflow runs automatically on every push to the `main` branch and executes the following stages:  

---

### 🔹 1. Checkout Repository  
```yaml
- name: Checkout Repository
  uses: actions/checkout@v3
```
- Tool: GitHub Actions
- Purpose: Fetches the repository contents so that images and scripts can be scanned.
- Output: Repository files available in the workflow environment.


### 🔹 2. Set Up Python Environment

```
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.x'

```
- Tool: Python
- Purpose: Configures the Python runtime to execute scanning scripts.
- Output: Python environment ready with required dependencies.

### 🔹 3. Install Dependencies
```
- name: Install Dependencies
  run: pip install -r requirements.txt

```
- Tool: pip
- Purpose: Installs Python dependencies (e.g., Pillow, ExifTool bindings, custom modules).
- Output: All libraries installed for scanning and reporting.


### 🔹 4. Run Image Steganography Scan

```
- name: Run Image Stego Scanner
  run: python scripts/scan_images.py --input ./images --output ./reports

```
- Tool: `scan_images.py` (custom Python script)
- Purpose: Scans images in the `images/` directory for:
- Hidden steganographic payloads
- Suspicious metadata (via ExifTool)
- Embedded scripts or hidden data
- Output: `reports/scan_results.txt` (or JSON) with findings.

### 🔹 5. Metadata Analysis (ExifTool)

```
- name: Run ExifTool Metadata Scan
  run: exiftool ./images > reports/metadata_report.txt

```
- Tool: ExifTool
- Purpose: Extracts metadata (EXIF, IPTC, XMP) to detect anomalies such as hidden comments, suspicious attributes, or embedded payloads.
- Output: `reports/metadata_report.txt`


### 🔹 6. Report Generation (Charts + PDF)

```
- name: Generate PDF Report
  run: python scripts/generate_report.py

```

- Tools: ReportLab, Matplotlib
- Purpose: Produces a professional PDF report consolidating:
- Findings from image scans
- Metadata anomalies
- Severity breakdown (charts)
- Compliance mappings (NIST, MITRE, OWASP)
- Output: reports/final_report.pdf



### 🔹 7. Upload Artifacts

```
- name: Upload PDF Report
  uses: actions/upload-artifact@v4
  with:
    name: docker-vulnerability-report
    path: report.pdf
```

- Purpose: Uploads scan results (`.txt`, `.json`, `.pdf`) as GitHub workflow artifacts.
- Benefit: Security teams can download and review reports after each workflow run.






---

## 🎯 Purpose  
The primary purpose of this project is to:  
- **Automate security scanning of images** to detect hidden steganography payloads and malicious metadata.  
- Provide a **single, consolidated report** instead of scattered outputs.  
- Help developers, DevOps, and security teams **integrate image security into CI/CD pipelines (DevSecOps)**.  
 

---

## ✅ Advantages  

- **Automated** → Scans run automatically with every code push (via GitHub Actions).  
- **Comprehensive** → Covers hidden payloads, suspicious metadata, and steganographic techniques.  
- **Professional Reports** → Reports can be generated in text, JSON, or PDF format with severity analysis and compliance mapping.  
- **Open-Source & Extensible** → Easily add new detection modules or integrate other security frameworks.  

---

## ⚡ Challenges Faced  

1. **Steganography Detection** → Detecting hidden payloads is more complex than traditional vulnerability scanning, requiring both metadata analysis and pixel-level inspection.  
2. **Data Normalization** → Metadata and stego detection tools (e.g., ExifTool, StegExpose) produce outputs in different formats that need to be unified.  
3. **Automation in CI/CD** → Ensuring lightweight execution of image scans within GitHub Actions without slowing down the pipeline.  

---

## 🖼️ Sample Report Preview  

Below is an example of the kind of report generated by the scanner:  

![Image Security Report](https://github.com/ADITYADAS1999/StegoGuard-CI-CD/actions/runs/17509351227/artifacts/3942546239)  

The PDF includes:  
- Image scan summaries and metadata anomalies.  
- Detection of possible hidden steganographic payloads.  
- Severity distribution charts.  
- NIST CSF, MITRE ATT&CK, OWASP Top 10 mappings.  
- Final consolidated recommendations.  

---

## 🔚 Conclusion  
The **ImageStegoScan-CI-CD** project provides a **complete security assessment workflow for image files**.  
By integrating steganography detection tools and compliance frameworks into CI/CD pipelines, it transforms raw scan data into **actionable insights** that help prevent malicious image uploads.  

**Future Work:**  
- Add advanced **AI/ML-based steganography detection**.  
- Support for **additional image formats** (e.g., GIF, BMP, TIFF).  
- Extend reporting to include **real-time dashboards** for security monitoring.  


---

## 📜 License  
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.  






