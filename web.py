import http.server
import http.client
import json
import socketserver
#COMUNICACION CON OPENFDA.
class OpenFDAClient():
    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_EVENT="/drug/event.json"
    OPENFDA_API_FOOD="/food/event.json"
    def get_event(self,limit):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET",self.OPENFDA_API_EVENT + "?limit=" + limit)
        r1 = conn.getresponse()
        data1=r1.read()
        data=data1.decode("utf8")
        return data
    def search_drug(self,drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET",self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+drug+'&limit=10')
        r1 = conn.getresponse()
        data1=r1.read()
        data=data1.decode("utf8")
        searched_drug=data
        return searched_drug
    def search_company(self,company):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET",self.OPENFDA_API_EVENT + '?search='+company+'&limit=10')
        r1 = conn.getresponse()
        data1=r1.read()
        data=data1.decode("utf8")
        searched_company=data
        return searched_company
    def get_food_event(self,limit):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET",self.OPENFDA_API_FOOD + "?limit=" + limit)
        r1 = conn.getresponse()
        data1=r1.read()
        data=data1.decode("utf8")
        return data
    def search_reaction(self,food):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET",self.OPENFDA_API_FOOD + '?search=products.namebrand:'+food+'&limit=10')
        r1 = conn.getresponse()
        data1=r1.read()
        data=data1.decode("utf8")
        searched_food=data
        return searched_food
#EXTRACCION DE DATOS.
class OpenFDAParser():
    def get_list_drugs(self,data):
        list_drugs=[]
        events_str=data
        events=json.loads(events_str)
        events=events["results"]
        for event in events:
            list_drugs.append(event["patient"]["drug"][0]["medicinalproduct"])
        return list_drugs
    def get_drug_companies(self,searched_drug):
        drug_companies=[]
        events_str=searched_drug
        events=json.loads(events_str)
        events=events["results"]
        for event in events:
            drug_companies.append(event["companynumb"])
        return drug_companies
    def get_companies(self,data):
        companies=[]
        events_str=data
        events=json.loads(events_str)
        events=events["results"]
        for event in events:
            companies.append(event["companynumb"])
        return companies
    def get_company_drugs(self,searched_company):
        company_drugs=[]
        events_str=searched_company
        events=json.loads(events_str)
        events=events["results"]
        for event in events:
            company_drugs.append(event["patient"]["drug"][0]["medicinalproduct"])
        return company_drugs
    def get_gender(self,data):
        genders=[]
        events_str=data
        events=json.loads(events_str)
        events=events["results"]
        for event in events:
            genders.append(event["patient"]["patientsex"])
        return genders
    def get_list_food(self,data):
        list_food=[]
        events_str=data
        events=json.loads(events_str)
        events=events["results"]
        for event in events:
            list_food.append(event["products"][0]["name_brand"])
        return list_food
    def get_reactions(self,searched_food):
        reactions=[]
        events_str=searched_food
        events=json.loads(events_str)
        events=events["results"]
        for event in events:
            reactions.append(event["reactions"][0])
        return reactions
    def get_industries (self,data):
        industries=[]
        events_str=data
        events=json.loads(events_str)
        events=events["results"]
        for event in events:
            industries.append(event["products"][0]["industry_name"])
        return industries

#VISUALIZACION DE DATOS.
class OpenFDAHTML():
    def get_mainpage(self):
        html="""
        <html>
        <head>
            <title> OpenFDA Cool </title>
        </head>
         <BODY BGCOLOR="CEF6EC" TEXT="black">
            <h1> <font face="Comic Sans MS,arial,verdana"> <u>OpenFDA Drugs </u></font>  </h1>
            <form method="get" action="listDrugs">
                <body>Numero de eventos</body>
                <input type="text" size="2" maxlength="2" name="limit"></input>
                <input type="submit" style="background:#BCF5A9" value= "Drug List: Send to OpenFDA">
            </form>
            <form method="get" action="listCompanies">
                <body>Numero de eventos</body>
                <input type="text" size="2" maxlength="2" name="limit"></input>
                <input type="submit" style="background:#F5F6CE" value= "Company List: Send to OpenFDA">
            </form>
            <form method="get" action="searchDrug">
                <body>Nombre del medicamento:     </body>
                <input type="text" name="drug" ></input>
                <input type="submit" style="background:#BCF5A9" value= "Drug Search : Send to OpenFDA">
            </form>
            <form method="get" action="searchCompany">
                <body>Nombre de la empresa</body>
                <input type="text" name="company"></input>
                <input type="submit" style="background:#F5F6CE" value= "Company Search : Send to OpenFDA">
            </form>
            <form method="get" action="listGender">
                <body>Numero de eventos</body>
                <input type="text" size="2" maxlength="2" name="limit"></input>
                <input type="submit" style="background:#DDA0DD" value= "Gender List: Send to OpenFDA">
            </form>

        </body>
        </html>
        """
        return html
    def get_mainpage_add(self):
        html="""
        <html>
        <head>
            <title> OpenFDA Cool </title>
        </head>
            <BODY BGCOLOR="CEF6EC" TEXT="black">
            <h1> <font face="Comic Sans MS,arial,verdana"> <u>OpenFDA Drugs </u></font>  </h1>
            <form method="get" action="searchGender">
                <body>Nombre del medicamento:     </body>
                <input type="text" name="drug" ></input>
                <input type="submit" style="background:#DDA0DD" value= "Gender Search : Send to OpenFDA">
            </form>
            <h1> <font face="Comic Sans MS,arial,verdana"> <u>OpenFDA Food </u></font>  </h1>
            <form method="get" action="listFoods">
                <body>Numero de eventos</body>
                <input type="text" size="2" maxlength="2" name="limit"></input>
                <input type="submit" style="background:#BCF5A9" value= "Food List: Send to OpenFDA"></input>
            </form>
            <form method="get" action="listIndustries">
                <body>Numero de eventos</body>
                <input type="text" size="2" maxlength="2" name="limit"></input>
                <input type="submit" style="background:#BCF5A9" value= "Industry List: Send to OpenFDA"></input>
            </form>
            <form method="get" action="searchReaction">
                <body>Nombre del producto:     </body>
                <input type="text" name="food" ></input>
                <input type="submit" style="background:#BCF5A9" value= "Reaction Search : Send to OpenFDA">
            </form>
            <form method="link" action="https://open.fda.gov/"> <input type="submit" VALUE="Dirigirse a OpenFDA" > </form>
        </body>
        </html>
        """
        return html
    def get_html_drugs(self,elements):
        number_elements= len(elements)
        html= """
        <html>
            <h1> <font face="Comic Sans MS,arial,verdana"> <u>OpenFDA Drugs </u></font>  </h1>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
             <BODY  BGCOLOR="BCF5A9" TEXT="black">
                <ol>
        """
        html+= "<h3> El numero de medicamentos es:" + str(number_elements) + "</h3>"
        for element in elements:
            html += "<li>" + element + "</li>\n"
        html += """
                </ol>
            </body>
        </html>
        """
        return html
    def get_html_companies(self,elements):
        number_elements= len(elements)
        html= """
        <html>
            <h1> <font face="Comic Sans MS,arial,verdana"> <u>OpenFDA Companies </u></font>  </h1>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
             <BODY BGCOLOR="F5F6CE" TEXT="black">
                <ol>
        """
        html+= "<h3> El numero de empresas es:" + str(number_elements) + "</h3>"
        for element in elements:
            html += "<li>" + element + "</li>\n"
        html += """
                </ol>
            </body>
        </html>
        """
        return html
    def get_html_genders(self,elements):
        varones=0
        mujeres=0
        number_elements= len(elements)
        html= """
        <html>
            <h1> <font face="Comic Sans MS,arial,verdana"> <u>OpenFDA Genders </u></font>  </h1>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
             <BODY BGCOLOR="DDA0DD" TEXT="black">
                <ol>
        """
        html+= "<h3> El numero de pacientes es:" + str(number_elements) + "</h3>"
        for element in elements:
            html += "<li>" + element + "</li>\n"
            if element == "1":
                varones=varones+1
            else:
                mujeres=mujeres+1
        html+= "<h4> El numero de varones es:" + str(varones) + "</h4>"
        html+= "<h4> El numero de mujeres es:" + str(mujeres) + "</h4>"
        html += """
                </ol>
            </body>
        </html>
        """
        return html
    def get_html_error(self):
        html="""
        <html>
            <h1> ERROR 404 Not Found </h1>
            <BODY  BGCOLOR="F6CECE" TEXT="black">
        </html>
        """
        return html
    def get_html_error_wrong_limit(self):
        html="""
        <html>
            <h1> ERROR </h1>
            <h3> El numero de eventos introducido no es un numero. </h3>
            <BODY  BGCOLOR="F6CECE" TEXT="black">
        </html>
        """
        return html
    def get_html_food(self,elements):
        number_elements= len(elements)
        html= """
        <html>
            <h1> <font face="Comic Sans MS,arial,verdana"> <u>OpenFDA Foods </u></font>  </h1>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
             <BODY  BGCOLOR="BCF5A9" TEXT="black">
                <ol>
        """
        html+= "<h3> El numero de elementos es:" + str(number_elements) + "</h3>"
        for element in elements:
            html += "<li>" + element + "</li>\n"
        html += """
                </ol>
            </body>
        </html>
        """
        return html

class testHTTPRequestHandler (http.server.BaseHTTPRequestHandler):
    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_EVENT="/drug/event.json"
    OPENFDA_API_FOOD="/food/event.json"


    def do_GET(self):

        client= OpenFDAClient()
        parser= OpenFDAParser()
        HTML= OpenFDAHTML()
        url=self.path
        url_list= url.split("=")
        main_page=False
        main_page_add=False
        drug_event=False
        search_drug=False
        company_event=False
        search_company=False
        gender_event=False
        search_gender=False
        food_event=False
        industry_event=False
        search_reaction=False
        secret=False
        redirect=False
        header1='Content-type'
        header2='text/html'
        response=200
        if self.path== "/" :
            main_page= True
        if self.path== "/add" :
            main_page_add= True
        elif "listDrugs" in self.path:
            drug_event= True
        elif "searchDrug" in self.path:
            search_drug=True
        elif "listCompanies" in self.path:
            company_event=True
        elif "searchCompany" in self.path:
            search_company=True
        elif "listGender" in self.path:
            gender_event=True
        elif 'searchGender' in self.path:
            search_gender=True
        elif 'listFoods?' in self.path:
            food_event=True
        elif 'listIndustries' in self.path:
            industry_event=True
        elif 'searchReaction' in self.path:
            search_reaction=True
        elif 'secret' in self.path:
            secret=True
        elif 'redirect' in self.path:
            redirect=True
        # Send response status code

        # Send headers

        # Send message back to client
        # message = "Hello world! " + self.path
        # Write content as utf-8 data
        if main_page:
            html= HTML.get_mainpage()
        elif main_page_add:
            html= HTML.get_mainpage_add()
        elif drug_event:
            url= self.path
            url_list=url.split("=")
            limit= url_list[1]
            if limit == "":
                limit = "10"
            limit_entero=False
            try :
                int(limit)
                limit_entero=True
            except ValueError:
                limit_entero=False
            if limit_entero:
                data= client.get_event(limit)
                drugs = parser.get_list_drugs(data)
                html=HTML.get_html_drugs(drugs)

            else:
                html=HTML.get_html_error_wrong_limit()

        elif search_drug:
            url= self.path
            url_list=url.split("=")
            drug= url_list[1]
            drug= client.search_drug(drug)
            drug_companies = parser.get_drug_companies(drug)
            html=HTML.get_html_drugs(drug_companies)

        elif company_event:
            url= self.path
            url_list=url.split("=")
            limit= url_list[1]
            if limit == "":
                limit = "10"
            limit_entero=False
            try :
                int(limit)
                limit_entero=True
            except ValueError:
                limit_entero=False
            if limit_entero:
                data=client.get_event(limit)
                companies=parser.get_companies(data)
                html=HTML.get_html_companies(companies)

            else:
                html=HTML.get_html_error_wrong_limit()


        elif search_company:
            url= self.path
            url_list=url.split("=")
            company= url_list[1]
            searched_company= client.search_company(company)
            company_drugs = parser.get_company_drugs(searched_company)
            html=HTML.get_html_companies(company_drugs)

        elif gender_event:
            url= self.path
            url_list=url.split("=")
            limit= url_list[1]
            if limit == "":
                limit ="10"
            limit_entero=False
            try :
                int(limit)
                limit_entero=True
            except ValueError:
                limit_entero=False
            if limit_entero:
                data= client.get_event(limit)
                genders = parser.get_gender(data)
                html=HTML.get_html_genders(genders)
            else:
                html=HTML.get_html_error()
        elif search_gender :
            url= self.path
            url_list=url.split("=")
            drug= url_list[1]
            searched_drug= client.search_drug(drug)
            genders = parser.get_gender(searched_drug)
            html=HTML.get_html_genders(genders)
        elif food_event:
            url= self.path
            url_list=url.split("=")
            limit= url_list[1]
            if limit == "":
                limit = "10"
            limit_entero=False
            try :
                int(limit)
                limit_entero=True
            except ValueError:
                limit_entero=False
            if limit_entero:
                data= client.get_food_event(limit)
                list_food= parser.get_list_food(data)
                html=HTML.get_html_food(list_food)

            else:
                html=HTML.get_html_error_wrong_limit()

        elif industry_event:
            url= self.path
            url_list=url.split("=")
            limit= url_list[1]
            if limit == "":
                limit ="10"
            limit_entero=False
            try :
                int(limit)
                limit_entero=True
            except ValueError:
                limit_entero=False
            if limit_entero:
                data= client.get_food_event(limit)
                list_industries= parser.get_industries(data)
                html=HTML.get_html_food(list_industries)
            else:
                html=HTML.get_html_error()

        elif search_reaction:
            url= self.path
            url_list=url.split("=")
            food= url_list[1]
            data = client.search_reaction(food)
            reactions = parser.get_reactions(data)
            html=HTML.get_html_food(reactions)
        elif secret:
            response=401
            header1='WWW-Authenticate'
            header2= 'Basic realm="My Realm"'
        elif redirect:
            response=302
            header1="Location"
            header2='http://localhost:8000/'
        else:
            response=404
            html=HTML.get_html_error()

        self.send_response(response)
        self.send_header(header1,header2)
        self.end_headers()

        if response==200 or response==404:
            self.wfile.write(bytes(html, "utf8"))
