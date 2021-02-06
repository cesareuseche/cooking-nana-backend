  
import threading, requests

#base_url="https://3000-a36fb042-3935-4d02-805d-4fb354c87a20.ws-us02.gitpod.io/" 
base_url="http://0.0.0.1:8080/"

def fetcher():

    response = requests.get(f"{base_url}/check")
    print(response.status_code)
    if(response.status_code == 200):
        print(response.json())

    threading.Timer(1, fetcher).start()


print("test")
fetcher()