import http.client
import json

genes_to_find = ["FRAT1", "ADA", "FXN", "RNU6-269P", "MIR633", "TTTY4C", "RBMY2YP", "FGFR3", "KDR", "ANK2"]

server = "rest.ensembl.org"
conn = http.client.HTTPConnection(server)
genes_dict = {}

print("Buscando identificadores en Ensembl...")

for gene in genes_to_find:
    endpoint = f"/lookup/symbol/homo_sapiens/{gene}?content-type=application/json"

    conn.request("GET", endpoint)
    response = conn.getresponse()

    if response.status == 200:
        data = json.loads(response.read().decode("utf-8"))
        genes_dict[gene] = data['id']
    else:
        genes_dict[gene] = "Not Found"

conn.close()


print("\nDictionary of Genes!")
print(f"There are {len(genes_dict)} genes in the dictionary:\n")

for name, identifier in genes_dict.items():
    print(f"{name}: --> {identifier}")