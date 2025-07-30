import requests
from bs4 import BeautifulSoup

def get_agrofit_cropid(crop):
    agrofit_crops = {
        "soja": "606",
        "milho": "579",
        "trigo": "611",
        "sorgo": "607",
        "mandioca": "569",
        "cafe": "500",
        "feijao": "536",
        "pastagem": "589"
    }
    return agrofit_crops[crop]

def get_agrofit_prodtid(product):
    agrofit_products = {
        "herbicidas": "8",
        "fungicidas": "7",
        "inseticidas": "9",
        "nematicidas": "11",
    }
    return agrofit_products[product]

def html_to_dict(html):
    data = []
    html = BeautifulSoup(html,'html.parser').find('table',class_ = 'P')
    try:
        rows= html.find_all('tr')[1:]
        for row in rows:                                
            columns = row.find_all('td')                
            data.append( {                              
                "Principio Ativo": columns[0].getText(),
                "Grupo Quimico": columns [1].getText(), 
                "Classe": columns[2].getText()          
                })                                      
        return data                                     
    except:
        print("MEU IRMAO ALGO DEU ERRADO AI, SE VIRA.")
        pass                                       
    
    
    
    
    
    
    
    

def agrofit_request(crop,product): 
    product_id = get_agrofit_prodtid(product)
    crop_id = get_agrofit_cropid(crop)
    html_dict = {}
    url = "https://agrofit.agricultura.gov.br/agrofit_cons/!ap_ing_ativo_lista_cons"
    headers = {
        "Referer": "https://agrofit.agricultura.gov.br/agrofit_cons/!ap_ing_ativo_consulta_cons",
        "Origin": "https://agrofit.agricultura.gov.br",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        }
    with requests.Session() as s:
        s.headers.update(headers)
        for i in range(0,10):
            payload = {
                "p_id_ingrediente_ativo": "",
                "p_nm_comum_port": "",
                "p_id_grupo_quimico": "",
                "p_id_classe": product_id,
                "p_id_cultura": crop_id,
                "p_nm_sort": "nm_comum_portugues",
                "p_linha_inicial": f"{i*10}" 
            }
            response = s.post(url, 
                              data=payload).text
            html_dict[f"{i}"] = html_to_dict(response)
    return html_dict


test = agrofit_request("mandioca","herbicidas")
print(test)
