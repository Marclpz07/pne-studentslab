import http.client
import json

GENES = {
    "FRAT1": "ENSG00000165879", "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060", "RNU6_269P": "ENSG00000212379",
    "MIR633": "ENSG00000207552", "TTTY4C": "ENSG00000228296",
    "RBMY2YP": "ENSG00000227633", "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052", "ANK2": "ENSG00000145362"
}

SERVER = "rest.ensembl.org"
conn = http.client.HTTPConnection(SERVER)

for gene_name, gene_id in GENES.items():
    endpoint = f"/sequence/id/{gene_id}?content-type=application/json"

    conn.request("GET", endpoint)
    res = conn.getresponse()

    if res.status == 200:
        data = json.loads(res.read().decode("utf-8"))
        description = data.get('desc', 'No description')
        sequence = data.get('seq', '')

        total_length = len(sequence)

        counts = {}
        for base in ['A', 'C', 'G', 'T']:
            counts[base] = sequence.count(base)

        most_frequent_base = max(counts, key=counts.get)

        print(f"Gene: {gene_name}")
        print(f"Description: {description}")
        print(f"Total length: {total_length}")

        for base in ['A', 'C', 'G', 'T']:
            num = counts[base]
            per = (num / total_length) * 100 if total_length > 0 else 0
            print(f"  {base}: {num} ({per:.1f}%)")

        print(f"Most frequent Base: {most_frequent_base}")
        print(" ")

    else:
        print(f"Error en {gene_name}: {res.status}")
        res.read()

conn.close()