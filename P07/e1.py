# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server
import http.client

server = "rest.ensembl.org"
endpoint = "/info/ping"
parameters = "?content-type=application/json"
URL = server + endpoint + parameters

print()
print(f"server: {server}")
print(f"URL: {URL}")

# Connect with the server
conn = http.client.HTTPConnection(server)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)
try:
    conn.request("GET", "/info/ping?content-type=application/json")
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

# -- Read the response message from the server
r1 = conn.getresponse()

# -- Print the status line
print(f"Response received!: {r1.status} {r1.reason}\n")

# -- Print the received data
print("PING OK! The database is runing")