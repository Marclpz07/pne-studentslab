import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import requests
import os
import json
PORT = 8080


class GenomeRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)

        if path == "/" or path == "/index.html":
            self.show_main_page()
        elif path == "/listSpecies":
            self.show_list_species(params)
        elif path == "/karyotype":
            self.show_karyotype(params)
        elif path == "/chromosomeLength":
            self.show_chromosome_length(params)
        elif path == "/geneLookup":
            self.show_identifier(params)
        elif path == "/geneSeq":
            self.show_sequence(params)
        elif path == "/geneInfo":
            self.show_info(params)
        elif path == "/geneCalc":
            self.show_operations(params)
        else:
            self.error()


    def show_main_page(self):
        try:
            with open("Final-Project/html/index.html", "r", encoding="utf-8") as f:
                html_content = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error: index.html not found.")

    def error(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "html", "error.html")

        with open(file_path, "r", encoding="utf-8") as f:
            error_html = f.read()

        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes(error_html, "utf-8"))


    def show_list_species(self, params):
        limit_list = params.get("limit", [None])
        limit = limit_list[0] if limit_list else None

        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "html", "ListSpecies.html")

        with open(file_path, "r", encoding="utf-8") as f:
            html_template = f.read()

        url = "https://rest.ensembl.org/info/species"
        response = requests.get(url, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()
            species_data = data.get("species", [])

            total_count = len(species_data)
            species_names = [sp.get("display_name") for sp in species_data if sp.get("display_name")]
            species_names = sorted(species_names, key=str.lower)

            if not limit or not limit.isdigit() or int(limit) <= 0 or int(limit) > total_count:
                self.error()
                return

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            limit_num = int(limit)
            species_names = species_names[:limit_num]

            elements_list = ""
            for name in species_names:
                elements_list += f"<li>{name}</li>"

            final_html = html_template.replace("{total_species}", str(total_count))
            final_html = final_html.replace("{selected_lim}", limit)
            final_html = final_html.replace("{species_list}", elements_list)

            self.wfile.write(bytes(final_html, "utf-8"))
        else:
            self.error()

    def show_karyotype(self, params):
        species_list = params.get("species", [None])
        species = species_list[0] if species_list else None

        if not species:
            self.error()
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "html", "karyotype.html")

        with open(file_path, "r", encoding="utf-8") as f:
            html_template = f.read()

        url = f"https://rest.ensembl.org/info/assembly/{species}"
        response = requests.get(url, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()
            karyotype = data.get("karyotype", [])

            if not karyotype:
                self.error()
                return


            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            chrom_elements = ""
            for chrom in karyotype:
                chrom_elements += f"<li>{chrom}</li>\n"

            final_html = html_template.replace("{species_list2}", chrom_elements)

            self.wfile.write(bytes(final_html, "utf-8"))

        else:
            self.error()

    def show_chromosome_length(self, params):

        species_list = params.get("species", [None])
        species = species_list[0] if species_list else None

        chromo_list = params.get("chromo", [None])
        chromo = chromo_list[0] if chromo_list else None

        if not species or not chromo:
            self.error()
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "html", "chromosomeLength.html")

        with open(file_path, "r", encoding="utf-8") as f:
            html_template = f.read()

        # 3. Conectar con el endpoint de Ensembl
        url = f"https://rest.ensembl.org/info/assembly/{species}/{chromo}"
        response = requests.get(url, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()
            length = data.get("length")

            if not length:
                self.error()
                return

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            final_html = html_template.replace("{name}", species)
            final_html = final_html.replace("{length}", str(length))
            final_html = final_html.replace("{chromo}", chromo)

            self.wfile.write(bytes(final_html, "utf-8"))

        else:
            self.error()


    def show_identifier(self, params):

        gene_list = params.get("gene", [None])
        gene = gene_list[0] if gene_list else None

        if gene:
            server = "rest.ensembl.org"
            conn = http.client.HTTPConnection(server)

            endpoint = f"/lookup/symbol/homo_sapiens/{gene}?content-type=application/json"
            conn.request("GET", endpoint)
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                identifier = data.get("id", "ID no encontrado")

                base_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_dir, "html", "identifier.html")

                with open(file_path, "r", encoding="utf-8") as f:
                    html_template = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()

                final_html = html_template.replace("{gene}", gene)
                final_html = final_html.replace("{identifier}", identifier)

                self.wfile.write(bytes(final_html, "utf-8"))

            else:
                self.error()

            conn.close()
        else:
            self.error()


    def show_sequence(self, params):
        genes = params.get("genes", [None])
        gene = genes[0] if genes else None

        if gene and gene.strip() != "" and gene != "None":

            conn1 = http.client.HTTPConnection("rest.ensembl.org")
            lookup_endpoint = f"/lookup/symbol/homo_sapiens/{gene}?content-type=application/json"

            conn1.request("GET", lookup_endpoint)
            res1 = conn1.getresponse()

            if res1.status == 200:
                data1 = json.loads(res1.read().decode("utf-8"))
                gene_id = data1.get("id")
                conn1.close()

                if gene_id:
                    conn2 = http.client.HTTPConnection("rest.ensembl.org")
                    seq_endpoint = f"/sequence/id/{gene_id}?content-type=application/json"

                    conn2.request("GET", seq_endpoint)
                    res2 = conn2.getresponse()

                    if res2.status == 200:
                        data2 = json.loads(res2.read().decode("utf-8"))
                        dna_sequence = data2.get("seq", "No sequence found")
                        conn2.close()

                        base_dir = os.path.dirname(os.path.abspath(__file__))
                        file_path = os.path.join(base_dir, "html", "sequence.html")

                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                html_template = f.read()
                            response_html = html_template.replace("{genes}", gene).replace("{sequence}", dna_sequence)
                        except FileNotFoundError:
                            response_html = f"<html><body><h1>Sequence of {gene}</h1><p>{dna_sequence}</p></body></html>"

                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(bytes(response_html, "utf-8"))
                        return

                    else:
                        res2.read()
                        conn2.close()
                        self.error()
                        return
            else:
                res1.read()
                conn1.close()
                self.error()
                return


        self.error()



    def show_info(self, params):

        gene_list = params.get("gene", [None])
        gene = gene_list[0] if gene_list else None

        if gene:
            server = "rest.ensembl.org"
            conn = http.client.HTTPConnection(server)

            endpoint = f"/lookup/symbol/homo_sapiens/{gene}?content-type=application/json"
            conn.request("GET", endpoint)
            response = conn.getresponse()

            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                start = data.get("start")
                end = data.get("end")
                length = end - start + 1
                Id = data.get("id", "ID no encontrado")
                name_chromo = data.get("seq_region_name")

                base_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_dir, "html", "info.html")

                with open(file_path, "r", encoding="utf-8") as f:
                    html_template = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()

                final_html = html_template.replace("{start}", str(start))
                final_html = final_html.replace("{end}", str(end))
                final_html = final_html.replace("{length}", str(length))
                final_html = final_html.replace("{id}", str(Id))
                final_html = final_html.replace("{name}", str(name_chromo))
                final_html = final_html.replace("{gene}", gene)

                self.wfile.write(bytes(final_html, "utf-8"))

            else:
                self.error()

            conn.close()
        else:
            self.error()

    def show_operations(self, params):
        genes = params.get("gene", [None])
        gene = genes[0] if genes else None

        if gene and gene.strip() != "" and gene != "None":

            conn1 = http.client.HTTPConnection("rest.ensembl.org")
            lookup_endpoint = f"/lookup/symbol/homo_sapiens/{gene}?content-type=application/json"

            conn1.request("GET", lookup_endpoint)
            res1 = conn1.getresponse()

            if res1.status == 200:
                data1 = json.loads(res1.read().decode("utf-8"))
                gene_id = data1.get("id")
                conn1.close()
                if gene_id:
                    conn2 = http.client.HTTPConnection("rest.ensembl.org")
                    seq_endpoint = f"/sequence/id/{gene_id}?content-type=application/json"

                    conn2.request("GET", seq_endpoint)
                    res2 = conn2.getresponse()

                    if res2.status == 200:
                        data2 = json.loads(res2.read().decode("utf-8"))
                        dna_sequence = data2.get("seq", "No sequence found")
                        conn2.close()

                        dna_sequence = dna_sequence.upper()
                        total = len(dna_sequence)
                        if total > 0:

                            a = dna_sequence.count('A') / total * 100
                            c = dna_sequence.count('C') / total * 100
                            g = dna_sequence.count('G') / total * 100
                            t = dna_sequence.count('T') / total * 100

                            base_dir = os.path.dirname(os.path.abspath(__file__))
                            file_path = os.path.join(base_dir, "html", "operations.html")

                            with open(file_path, "r", encoding="utf-8") as f:
                                html_template = f.read()

                            self.send_response(200)
                            self.send_header("Content-Type", "text/html; charset=utf-8")
                            self.end_headers()

                            final_html = html_template.replace("{T}", str(round(t, 2)))
                            final_html = final_html.replace("{A}", str(round(a, 2)))
                            final_html = final_html.replace("{C}", str(round(c, 2)))
                            final_html = final_html.replace("{G}", str(round(g, 2)))
                            final_html = final_html.replace("{gene}", str(gene))
                            final_html = final_html.replace("{length}", str(total))

                            self.wfile.write(bytes(final_html, "utf-8"))
                            return
                        else:
                            self.error()
                            return

                    else:
                        res2.read()
                        conn2.close()
                        self.error()
                        return

                else:
                    self.error()
                    return

            else:
                res1.read()
                conn1.close()
                self.error()
                return

        else:
            self.error()








with socketserver.TCPServer(("", PORT), GenomeRequestHandler) as httpd:
    print(f"Servidor corriendo en el puerto {PORT}...")
    httpd.serve_forever()