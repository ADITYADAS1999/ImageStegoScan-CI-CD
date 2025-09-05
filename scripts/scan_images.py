import os
import re
import subprocess
from PIL import Image
import exifread

IMG_FOLDER = "images"
REPORT_FOLDER = "reports"
REPORT_FILE = os.path.join(REPORT_FOLDER, "image_scan_report.md")

def check_exif_metadata(filepath):
    suspicious = []
    with open(filepath, "rb") as f:
        tags = exifread.process_file(f, details=False)
        for tag, value in tags.items():
            if len(str(value)) > 500:  # unusually long EXIF field
                suspicious.append(f"{tag}: suspicious length")
            if re.search(r"(powershell|cmd.exe|<script>|php)", str(value), re.IGNORECASE):
                suspicious.append(f"{tag}: contains code")
    return suspicious

def check_file_headers(filepath):
    with open(filepath, "rb") as f:
        header = f.read(16)
    if header.startswith(b"\xFF\xD8"): return "JPEG"
    if header.startswith(b"\x89PNG"): return "PNG"
    return "⚠️ Not a standard image header"

def scan_with_clamav(filepath):
    try:
        result = subprocess.run(["clamscan", filepath], capture_output=True, text=True)
        if "OK" in result.stdout:
            return "✅ Clean"
        elif "FOUND" in result.stdout:
            return "⚠️ Malicious"
        else:
            return f"❓ Unknown ({result.stdout.strip()})"
    except Exception as e:
        return f"Error running ClamAV: {e}"

def analyze_image(filepath):
    results = []
    try:
        img = Image.open(filepath)
        img.verify()  # verify integrity
    except Exception as e:
        results.append(f"⚠️ Not a valid image: {e}")
    suspicious_exif = check_exif_metadata(filepath)
    if suspicious_exif:
        results.extend(suspicious_exif)
    return results if results else ["✅ No obvious steganography"]

def main():
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write("# Image Security Scan Report\n\n")
        report.write("| File | Header | Metadata/Stego Check | ClamAV |\n")
        report.write("|------|--------|----------------------|--------|\n")

        for file in os.listdir(IMG_FOLDER):
            path = os.path.join(IMG_FOLDER, file)
            if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            header_status = check_file_headers(path)
            metadata_results = "; ".join(analyze_image(path))
            clamav_status = scan_with_clamav(path)

            report.write(f"| {file} | {header_status} | {metadata_results} | {clamav_status} |\n")

    print(f"✅ Report generated: {REPORT_FILE}")

if __name__ == "__main__":
    main()
