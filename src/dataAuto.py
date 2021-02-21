# importing the requests library 
import requests
import random 
import datetime

# Endpoint al que haremos POST  
API_ENDPOINT = "http://localhost:8080/recipes"
  
# Aquí iría la api_key en caso de haberla 
#API_KEY = "XXXXXXXXXXXXXXXXX"
  
# data to be sent to api 

    # Aquí va el código que genera los diccionarios
source_ingredients = ["onion", "tomato", "rice", "beef", "chiken", "turkey", "pork", "partridge", "keema", "crab", "ham", "kidney meat", "mutton", "chops", "rocket leaves", "drumstick", "kaffir lime", "plantain", "cherry", "cherry tomatoes", "turnip", "gourd", "pimiento", "spinach", "onion", "mustard leaves", "radish", "amaranth", "flour", "oats", "jowar", "muesli", "tapioca", "semolina", "buckwheat", "green gram", "bengal gram", "kidney beans", "gruyere cheese", "gouda cheese", "milk", "feta cheese", "brie cheese", "cream cheese", "ricotta cheese", "parmesan cheese", "blue cheese", "cheedar cheese", "mascarpone cheese", "cream", "mozzarella cheese", "yogurt", "eggs", "salt", "sugar", "butter"]

for x in range (1,21): #el último número no se incluye en el For
    sample_list = random.choices(source_ingredients, k=random.choice(range(1, len(source_ingredients))))
    #sample_list= [1]
    #print(sample_list)
    z = datetime.datetime.now()  
    datab = {"description":"Random Description generated number "+str(x),
            "name":"Random Name of recipe number "+str(x),
            "instructions":"Some Random instructions generated number "+str(x),
            "tags":"tags will help to find recipe",
            "img_url":"https://picsum.photos/200/300",
            "ingredients":str(sample_list),
            "date_published":str(z.year)+"-"+str(z.strftime("%m"))+"-"+str(z.strftime("%d"))+"T"+str(z.strftime("%H"))+":"+str(z.strftime("%M"))
            } 
    print(datab)
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = datab) 
  
#extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url) 