import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "b685095b-edd3-4ce1-8d8d-5cb767e2e288"

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""
        
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + state
        else:
            new_loc = name
        
    else:
        lat = "null"
        lng = "null"
        new_loc = location
    return json_status, lat, lng, new_loc

def get_route(origin_lat, origin_lng, dest_lat, dest_lng, key):
    params = {
        "point": [f"{origin_lat},{origin_lng}", f"{dest_lat},{dest_lng}"],
        "vehicle": "car",
        "locale": "es",  # 👈 Añadido: instrucciones en español
        "key": key
    }
    
    url = route_url + urllib.parse.urlencode(params, doseq=True)
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            distance = data['paths'][0]['distance']
            time = data['paths'][0]['time']
            instructions = data['paths'][0]['instructions']
            return distance, time, instructions
        else:
            print(f"Error en la solicitud de ruta: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return None

while True:
    loc1 = input("Ubicación de inicio: ")
    if loc1.lower() == "salir" or loc1.lower() == "s":
        break
    orig = geocoding(loc1, key)
    print(f"Origen: {orig}")
    
    if orig[1] != "null" and orig[2] != "null":
        loc2 = input("Destino: ")
        if loc2.lower() == "salir" or loc2.lower() == "s":
            break
        dest = geocoding(loc2, key)
        print(f"Destino: {dest}")
        
        if dest[1] != "null" and dest[2] != "null":
            route_info = get_route(orig[1], orig[2], dest[1], dest[2], key)
            if route_info:
                distance, time, instructions = route_info
                print(f"Ruta calculada: Distancia aproximada: {distance:.2f} metros, Tiempo estimado: {time:.2f} milisegundos")
                
                print("Instrucciones del viaje:")
                for i, instruction in enumerate(instructions, start=1):
                    print(f"Paso {i}: {instruction['text']} - {instruction['distance']:.2f} metros")
            else:
                print("No se pudo calcular la ruta. Verifica las coordenadas o la clave API.")
        else:
            print("La geocodificación del destino falló.")
    else:
        print("La geocodificación del origen falló.")
