import json
import csv

# File paths
input_sbom = "sbom.json"  # Replace with your SBOM file
output_csv = "sbom_vulnerabilities.csv"

# Load SBOM JSON
with open(input_sbom, "r") as f:
    sbom_data = json.load(f)

# Extract components and vulnerabilities
components = sbom_data.get("components", [])

# Define CSV columns
csv_columns = ["Component Name", "Version", "Vulnerability ID", "Severity", "Description"]

# Process and write to CSV
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_columns)  # Write headers

    for component in components:
        name = component.get("name")
        version = component.get("version", "N/A")
        vulnerabilities = component.get("vulnerabilities", [])
        
        for vulnerability in vulnerabilities:
            vuln_id = vulnerability.get("id", "N/A")
            severity = vulnerability.get("severity", "N/A")
            description = vulnerability.get("description", "N/A")
            writer.writerow([name, version, vuln_id, severity, description])

print(f"SBOM converted to CSV: {output_csv}")
