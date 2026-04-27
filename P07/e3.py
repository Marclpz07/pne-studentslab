import http.client
import json

server = "rest.ensembl.org"
gene_id = "ENSG00000207552"
endpoint = f"/sequence/id/{gene_id}?content-type=application/json"

print(f"Server: {server}")
print(f"URL: {server}{endpoint}")

conn = http.client.HTTPConnection(server)

try:
    conn.request("GET", endpoint)
    res = conn.getresponse()
    print(f"Response received!: {res.status} {res.reason}\n")

    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)

        gene_name = "MIR633"
        description = json_data.get('desc', 'No description available')
        bases = json_data.get('seq', 'No sequence found')

        print(f"Gene: {gene_name}")
        print(f"Description: {description}")
        print(f"Bases: {bases}")
    else:
        print(f"Error: {res.status}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()