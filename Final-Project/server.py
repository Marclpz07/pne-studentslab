import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import requests  # La usaremos para conectar con la API de Ensembl
import os
import json
PORT = 8080


class GenomeRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parseamos la URL para saber qué ruta está pidiendo el usuario
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)

        # Enrutamiento básico
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
        else:
            self.error()


    def show_main_page(self):
        """Sirve el menú principal leyendo tu archivo index.html"""
        try:
            with open("Final-Project/html/index.html", "r", encoding="utf-8") as f:
                html_content = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))
        except FileNotFoundError:
            # Por si acaso el archivo no está en la misma carpeta raíz
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error: index.html not found.")

    def error(self):
        """Muestra la pantalla roja limpia sin textos del sistema"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "html", "error.html")

        with open(file_path, "r", encoding="utf-8") as f:
            error_html = f.read()

        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes(error_html, "utf-8"))


# Lanzar el servidor

    def show_list_species(self, params):
        """Genera la lista clonando la interfaz del enunciado y validando errores"""

        # 1. Leer los parámetros enviados desde el index amarillo (¡QUITA LAS CABECERAS DE AQUÍ!)
        limit_list = params.get("limit", [None])
        limit = limit_list[0] if limit_list else None

        # 2. Cargar tu plantilla HTML física
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "html", "ListSpecies.html")

        with open(file_path, "r", encoding="utf-8") as f:
            html_template = f.read()

        # 3. Conectar con el servidor web de Ensembl
        url = "https://rest.ensembl.org/info/species"
        response = requests.get(url, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()
            species_data = data.get("species", [])

            total_count = len(species_data)
            species_names = [sp.get("display_name") for sp in species_data if sp.get("display_name")]
            species_names = sorted(species_names, key=str.lower)


            # --- CONTROL DE ERRORES CRÍTICO ---
            if not limit or not limit.isdigit() or int(limit) <= 0 or int(limit) > total_count:
                self.error()  # Llama a tu función de error (pantalla roja)
                return  # Detiene la función por completo. No enviará ningún 200 OK.
            # ----------------------------------

            # ¡AQUÍ ES DONDE DEBEN IR LAS CABECERAS SINO HAY ERROR!
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Si pasa los filtros, convertimos y recortamos de forma segura
            limit_num = int(limit)
            species_names = species_names[:limit_num]

            # Creamos las viñetas HTML (<li>)
            elementos_lista = ""
            for name in species_names:
                elementos_lista += f"<li>{name}</li>"

            # Reemplazo simultáneo en tu archivo html
            final_html = html_template.replace("{total_species}", str(total_count))
            final_html = final_html.replace("{selected_lim}", limit)
            final_html = final_html.replace("{species_list}", elementos_lista)

            # Enviamos el HTML definitivo al navegador
            self.wfile.write(bytes(final_html, "utf-8"))
        else:
            self.error()

    def show_karyotype(self, params):
        """Abre karyotype.html y genera la lista de cromosomas sin puntos"""

        # 1. Extraer el nombre de la especie
        species_list = params.get("species", [None])
        species = species_list[0] if species_list else None

        # --- VALIDACIÓN INICIAL ---
        if not species:
            self.error()
            return
        # --------------------------

        # 2. Leer tu plantilla física karyotype.html
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "html", "karyotype.html")

        with open(file_path, "r", encoding="utf-8") as f:
            html_template = f.read()

        # 3. Consultar a la API de Ensembl
        url = f"https://rest.ensembl.org/info/assembly/{species}"
        response = requests.get(url, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            data = response.json()
            karyotype = data.get("karyotype", [])

            # --- VALIDACIÓN DE CARIOTIPO VACÍO ---
            if not karyotype:
                self.error()
                return
            # -------------------------------------


            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 4. Construimos las filas de la columna sin viñetas
            chrom_elements = ""
            for chrom in karyotype:
                chrom_elements += f"<li>{chrom}</li>\n"

            # 5. Inyectamos los elementos en el hueco de tu HTML
            final_html = html_template.replace("{species_list2}", chrom_elements)

            # 6. Mandamos la respuesta final al navegador
            self.wfile.write(bytes(final_html, "utf-8"))

        else:
            # Si la especie está mal escrita o no existe, salta tu pantalla roja limpia
            self.error()

    def show_chromosome_length(self, params):
        """Busca el tamaño de un cromosoma en Ensembl y abre tu chromosomeLength.html"""

        # 1. Extraer los dos parámetros del formulario (?species=...&chromo=...)
        species_list = params.get("species", [None])
        species = species_list[0] if species_list else None

        chromo_list = params.get("chromo", [None])
        chromo = chromo_list[0] if chromo_list else None

        # --- VALIDACIÓN INICIAL ---
        if not species or not chromo:
            self.error()
            return
        # --------------------------

        # 2. CARGAR TU ARCHIVO HTML REAL (Fíjate en el nombre exacto de tu archivo)
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

            # --- VALIDACIÓN POR SI NO DEVUELVE LONGITUD ---
            if not length:
                self.error()
                return
            # ----------------------------------------------

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # 4. REEMPLAZO EXACTO: Usamos tus llaves {name} y {length} del archivo
            final_html = html_template.replace("{name}", species)
            final_html = final_html.replace("{length}", str(length))
            final_html = final_html.replace("{chromo}", chromo)

            # 5. Enviamos tu propio archivo modificado al navegador
            self.wfile.write(bytes(final_html, "utf-8"))

        else:
            # Si el cromosoma no existe en la base de datos, salta la pantalla roja limpia
            self.error()


    def show_identifier(self, params):

        gene_list = params.get("gene", [None])
        gene = gene_list[0] if gene_list else None

        if gene:
            # 2. Conectamos con el servidor REST de Ensembl
            server = "rest.ensembl.org"
            conn = http.client.HTTPConnection(server)

            # Construimos la URL dinámica usando f-string con el gen introducido
            endpoint = f"/lookup/symbol/homo_sapiens/{gene}?content-type=application/json"
            conn.request("GET", endpoint)
            response = conn.getresponse()

            # 3. Si Ensembl encuentra el gen (Status 200 OK)
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                identifier = data.get("id", "ID no encontrado")

                base_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_dir, "html", "identifier.html")

                with open(file_path, "r", encoding="utf-8") as f:
                    html_template = f.read()

                # Enviamos las cabeceras HTTP reglamentarias al cliente
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()

                final_html = html_template.replace("{gene}", gene)
                final_html = final_html.replace("{identifier}", identifier)


                # Escribimos el cuerpo (el HTML) en el socket del navegador
                self.wfile.write(bytes(final_html, "utf-8"))

            # 4. Si Ensembl no encuentra el gen (por ejemplo, error 400 o 404)
            else:
                self.error()

            conn.close()
        else:
            self.error()


    def show_sequence(self, params):
        """Servicio 2: Obtiene la secuencia de ADN de un gen (geneSeq) en 2 pasos reales"""
        # 1. Extraemos el gen que el usuario metió en el cuadro de texto
        genes = params.get("genes", [None])
        gene = genes[0] if genes else None

        # Evaluamos el string (singular) y comprobamos que no esté vacío
        if gene and gene.strip() != "" and gene != "None":

            # --- PASO 1: CONSEGUIR EL ID ESTABLE (ENSG...) ---
            conn1 = http.client.HTTPConnection("rest.ensembl.org")
            lookup_endpoint = f"/lookup/symbol/homo_sapiens/{gene}?content-type=application/json"

            conn1.request("GET", lookup_endpoint)
            res1 = conn1.getresponse()

            if res1.status == 200:
                data1 = json.loads(res1.read().decode("utf-8"))
                gene_id = data1.get("id")  # Guardamos el ID único (ej: ENSG00000165879)
                conn1.close()  # Cerramos la primera conexión limpiamente

                if gene_id:
                    # --- PASO 2: CONSEGUIR LA SECUENCIA CON ESE ID ---
                    conn2 = http.client.HTTPConnection("rest.ensembl.org")
                    seq_endpoint = f"/sequence/id/{gene_id}?content-type=application/json"

                    conn2.request("GET", seq_endpoint)
                    res2 = conn2.getresponse()

                    if res2.status == 200:
                        data2 = json.loads(res2.read().decode("utf-8"))
                        dna_sequence = data2.get("seq", "No sequence found")
                        conn2.close()  # Cerramos la segunda conexión

                        # --- PASO 3: CARGAR TU PLANTILLA HTML Y PINTAR ---
                        base_dir = os.path.dirname(os.path.abspath(__file__))
                        file_path = os.path.join(base_dir, "html", "sequence.html")

                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                html_template = f.read()
                            # Reemplazamos los marcadores de tu archivo HTML
                            response_html = html_template.replace("{genes}", gene).replace("{sequence}", dna_sequence)
                        except FileNotFoundError:
                            # Plan B de emergencia por si el archivo no existiera
                            response_html = f"<html><body><h1>Sequence of {gene}</h1><p>{dna_sequence}</p></body></html>"

                        # Enviamos la respuesta HTTP correcta (200 OK) al navegador
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(bytes(response_html, "utf-8"))
                        return  # Salimos con éxito absoluto

                    else:
                        # Si falla la petición de la secuencia
                        res2.read()
                        conn2.close()
                        self.error()
                        return
            else:
                # Si falla el lookup (el gen no existe en la base de datos)
                res1.read()
                conn1.close()
                self.error()
                return

        # Si el usuario mandó el formulario vacío o fallaron los 'if'
        self.error()



    def show_info(self, params):

        gene_list = params.get("gene", [None])
        gene = gene_list[0] if gene_list else None

        if gene:
            # 2. Conectamos con el servidor REST de Ensembl
            server = "rest.ensembl.org"
            conn = http.client.HTTPConnection(server)

            # Construimos la URL dinámica usando f-string con el gen introducido
            endpoint = f"/lookup/symbol/homo_sapiens/{gene}?content-type=application/json"
            conn.request("GET", endpoint)
            response = conn.getresponse()

            # 3. Si Ensembl encuentra el gen (Status 200 OK)
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

                # Enviamos las cabeceras HTTP reglamentarias al cliente
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()

                final_html = html_template.replace("{start}", str(start))
                final_html = final_html.replace("{end}", str(end))
                final_html = final_html.replace("{length}", str(length))
                final_html = final_html.replace("{id}", str(Id))
                final_html = final_html.replace("{name}", str(name_chromo))
                final_html = final_html.replace("{gene}", gene)


                # Escribimos el cuerpo (el HTML) en el socket del navegador
                self.wfile.write(bytes(final_html, "utf-8"))

            # 4. Si Ensembl no encuentra el gen (por ejemplo, error 400 o 404)
            else:
                self.error()

            conn.close()
        else:
            self.error()



with socketserver.TCPServer(("", PORT), GenomeRequestHandler) as httpd:
    print(f"Servidor corriendo en el puerto {PORT}...")
    httpd.serve_forever()