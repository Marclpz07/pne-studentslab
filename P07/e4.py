import http.client
import json

SERVER = "rest.ensembl.org"

genes_ids = {
    "FRAT1": "ENSG00000165879", "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060", "RNU6_269P": "ENSG00000212379",
    "MIR633": "ENSG00000207552", "TTTY4C": "ENSG00000228296",
    "RBMY2YP": "ENSG00000227633", "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052", "ANK2": "ENSG00000145362"
}

gene_name = input("Write the gene name: ").strip().upper()

if gene_name not in genes_ids:
    print(f"Error: Gene {gene_name} not found in our local database.")
    exit()

gene_id = genes_ids[gene_name]
endpoint = f"/sequence/id/{gene_id}?content-type=application/json"

print(f"\nServer: {SERVER}")
print(f"URL: {SERVER}{endpoint}")

conn = http.client.HTTPConnection(SERVER)
conn.request("GET", endpoint)
res = conn.getresponse()
print(f"Response received!: {res.status} {res.reason}\n")

if res.status == 200:
    data = json.loads(res.read().decode("utf-8"))
    description = data.get('desc', 'No description')
    sequence = data.get('seq', '')

    total_length = len(sequence)

    counts = {}
    for base in ['A', 'C', 'G', 'T']:
        count = sequence.count(base)
        percentage = (count / total_length) * 100 if total_length > 0 else 0
        counts[base] = (count, percentage)

    most_frequent_base = max(counts, key=lambda x: counts[x][0])


    print(f"Gene: {gene_name}")
    print(f"Description: {description}")
    print("New sequence created!")
    print(f"Total length: {total_length}")

    for base in ['A', 'C', 'G', 'T']:
        c, p = counts[base]
        print(f"{base}: {c} ({p:.1f}%)")

    print(f"Most frequent Base: {most_frequent_base}")

else:
    print("Failed to retrieve data.")

conn.close()