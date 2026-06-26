import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from Seq1 import Seq
import jinja2 as j
from ensembl import ensembl

e = ensembl()
s = Seq()
path_list = ["/listSpecies", "/karyotype", "/chromosomeLength", "/"]
# Define the Server's port
PORT = 8080


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""
        url_path = urlparse(self.path)
        path = url_path.path  # we get it from here
        arguments = parse_qs(url_path.query)
        print(arguments)
        print(path)
        contents = Path('html/main.html').read_text()
        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        if path == "/":
            contents = Path('html/main.html').read_text()

        elif path == "/listSpecies":
            if 'limit' in arguments:
                try:
                    int(arguments['limit'][0])
                    valid = True
                except ValueError:
                    valid = False
                if valid == True:
                    limit = int(arguments['limit'][0])
                    contents = read_html_file("list.html").render(context={"list": e.list(limit), "limit": limit})
                else:
                    contents = Path('html/Error.html').read_text()
            else:
                contents = read_html_file("list.html").render(context={"list": e.list(), "limit": "not defined by the user"})

        elif path == "/karyotype":
            if ('species' in arguments
                    and e.check_specie(arguments['species'][0]) == True):

                contents = read_html_file("karyotype.html").render(context=
                {
                    "karyotype": e.karyo(arguments['species'][0]),
                    "specie": arguments['species'][0]
                })
            else:
                contents = Path('html/Error.html').read_text()

        elif path == "/chromosomeLength":
            if (('species' in arguments)
                    and ('chromo' in arguments)
                    and e.check_specie(arguments['species'][0]) == True
                    and e.check_specie(arguments['species'][0]) == True
                    and e.check_chromosome(arguments['species'][0], arguments['chromo'][0]) == True):
                        contents = read_html_file("chromosome.html").render(context=
                        {
                            "length": e.chrom_length(arguments['species'][0], arguments['chromo'][0])
                        })
            else:
                contents = Path('html/Error.html').read_text()

        #
        #
        #This section further on corresponds to the intermediate level:
        #Human gene browsing
        #
        #

        elif path == "/geneLookup":
            if ('gene' in arguments
                    and e.check_gene(arguments['gene'][0]) == True
                    and e.check_human(arguments['gene'][0]) == True):
                contents = read_html_file("gene_id.html").render(context={"id": e.get_gene_id(arguments['gene'][0]) })

            else:
                contents = Path('html/Error.html').read_text()

        elif path == "/geneSeq":
            if ('gene' in arguments
                    and e.check_gene(arguments['gene'][0]) == True
                    and e.check_human(arguments['gene'][0]) == True):
                contents = read_html_file("gene_seq.html").render(context={"seq":  e.get_gene_seq(arguments['gene'][0]) })
            else:
                contents = Path('html/Error.html').read_text()

        elif path == "/geneInfo":
            if ('gene' in arguments
                    and e.check_gene(arguments['gene'][0]) == True
                    and e.check_human(arguments['gene'][0]) == True):
                info = e.get_gene_info(arguments['gene'][0])
                contents = read_html_file("gene_seq.html").render(context={
                    "start":  info["start"],
                    "end": info["end"],
                    "len": info["length"],
                })
            else:
                contents = Path('html/Error.html').read_text()

        elif path == "/geneCalc":
            if ('gene' in arguments
                    and e.check_gene(arguments['gene'][0]) == True
                    and e.check_human(arguments['gene'][0]) == True):
                calcs = e.get_gene_calcs(arguments['gene'][0])
                contents = read_html_file("gene_calc.html").render(context={"calcs":  calcs,})
            else:
                contents = Path('html/Error.html').read_text()

        elif path == "/geneList":
            if ('chromo' in arguments
                    and 'start' in arguments
                    and 'end' in arguments
                    and e.check_gene(arguments['gene'][0]) == True
                    and e.check_human(arguments['gene'][0]) == True):
                genes = e.get_genes_from_chromosome(arguments['chromo'][0],arguments['start'][0],arguments['end'][0])
                contents = read_html_file("gene_chrom_region.html").render(context={"genes":  genes,})
            else:
                contents = Path('html/Error.html').read_text()

        else:
            contents = Path('html/Error.html').read_text()


        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
