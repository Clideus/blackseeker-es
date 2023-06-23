import argparse
import json
import signal
import sys
import time
from pickle import FALSE
import requests
from colorama import Fore, init

init()

def menu():
    print(Fore.LIGHTBLUE_EX + """

       ____  _        _    ____ _  __  ____  _____ _____ _  _______ ____       
      | __ )| |      / \  / ___| |/ / / ___|| ____| ____| |/ / ____|  _ \     
      |  _ \| |     / _ \| |   | ' /  \___ \|  _| |  _| | ' /|  _| | |_) |     
      | |_) | |___ / ___ \ |___| . \   ___) | |___| |___| . \| |___|  _ <    
      |____/|_____/_/   \_\____|_|\_\ |____/|_____|_____|_|\_\_____|_| \_\     
                                                                       
   BLACK SEEKER es una herramienta OSINT basada en solicitudes de URL creada por: @Clideus.                                       		                                                             
                                                                    """)


parser = argparse.ArgumentParser()
add_help = True
parser.add_argument("-u", "--username", type=str, metavar='USUARIO',
                    help="Busca un nombre de usuario en todos los sitios.")
parser.add_argument("-ip", type=str, metavar='IP',
                    help="Localiza una dirección IP")
parser.add_argument("-o", "--onlyok", action='store_true', default=FALSE,
                    help="Muestra solo las respuestas OK. Esto ocultará las respuestas no encontradas.")
parser.add_argument("-sn", "--socialnetworks", type=str, metavar='USERNAME',
                    help="Busca sóo redes sociales. No use: -sn -u [nombre de usuario].")


menu()
redesSociales = [
    "https://www.twitter.com/",
    "https://vsco.co/",
    "https://www.instagram.com/",
    "https://www.onlyfans.com/",
    "https://www.tiktok.com/",
    "https://www.snapchat.com/",
    "https://www.facebook.com/",
    "https://pinterest.com/",
    "https://reddit.com/",
    "https://vk.com/",
    "https://twitch.tv/",
    "https://discord.com/",
    "https://soundcloud.com/",
    "https://linkedin.com/"
]

noEncontrado = Fore.RED + "[-] NO ENCONTRADO: %s"
encontrado = Fore.LIGHTGREEN_EX + "[*] ¡GOL!: %s"
posible = Fore.YELLOW + "[?] POSIBLE CONEXIÓN: %s"
iperror = Fore.LIGHTRED_EX + "[-] ERROR: NO SE PUDO CONECTAR A LA API DEL RASTREADOR IP."


def buscar_usr():
    with open("sites.md", "r") as sitios:
        lineas = sitios.readlines()
        for sitio in lineas:
            usuarioURL = "%s%s" % (sitio.rstrip(), usuario)
            sesion = requests.Session()
            respuesta = sesion.get(usuarioURL, allow_redirects=True, verify=None)
            if respuesta.status_code == 200:
                print(posible % usuarioURL)
            else:
                if (respuesta.status_code == 404 or 504) and (args.onlyok == FALSE):
                    print(noEncontrado % usuarioURL)
        sitios.close()


def social():
    if (args.redesSociales):
        for social in redesSociales:
            usuarioURL = "%s%s" % (social, usuario)
            respuesta = requests.get(usuarioURL, allow_redirects=True)
            if respuesta.status_code == 200:
                print(posible % usuarioURL)
            elif (args.onlyok == FALSE):
                print(noEncontrado % usuarioURL)


def buscar_ip():
   url = ("http://ip-api.com/json/")
   stat = requests.get(url, allow_redirects=False)
   if (stat.status_code == 200):
      input_ip = requests.get(url + target_ip)
      data = input_ip.text
      api = json.loads(data)

      # Variables de resultados:
      ip = "IP: "+(target_ip)
      isp = "ISP: "+(api["isp"])
      pais = "PAÍS: "+(api["country"])
      zonaHoraria = "ZONA HORARIA: "+(api["timezone"])
      region = "REGION: "+(api["regionName"])+" - "+(api["zip"])
      ciudad = "CIUDAD: "+(api["city"])
      resultados_lista = [
          ip + "\n",
          isp + "\n \r",
          pais + "\n",
          zonaHoraria + "\n \r",
          region + "\n",
          ciudad + "\n \r"]
      def resultadosIP():
          print(Fore.LIGHTGREEN_EX + "[*] GOAL!:\n")
          print(f'{Fore.LIGHTCYAN_EX} + {ip}\n')
          print(f'{Fore.LIGHTCYAN_EX} + {isp}\n')
          print(f'{Fore.LIGHTCYAN_EX} + {pais}\n')
          print(f'{Fore.LIGHTCYAN_EX} + {zonaHoraria}\n')
          print(f'{Fore.LIGHTCYAN_EX} + {region}\n')
          print(f'{Fore.LIGHTCYAN_EX} + {ciudad}\n')
      resultadosIP()
      guardarIP = input("¿Desea crear un archivo de registro? (S/N)...")
      if guardarIP == "S" or guardarIP == "s":
          log = open(target_ip + " log.txt", "w")
          log.write("REGISTRO DE UBICACIÓN IP: \n \r")
          for lineas in resultados_lista:
             log.writelines(lineas)
          log.close()
      else:
          pass
   else:
        print(iperror)


def handler(signum, frame):
   salir = input("¿Realmente desea salir? S/N ")
   if salir == 'S' or salir == 's':
       print(Fore.LIGHTCYAN_EX + "¡Gracias por usar BLACK SEEKER!")
       time.sleep(1)
       sys.exit(1)
   else:
      pass
   


signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
   args = parser.parse_args()
   onlyok_bool = FALSE
usuario = args.username or args.redesSociales
target_ip = args.ip

if args.username:
   buscar_usr()
if args.ip:
   buscar_ip()
if args.redesSociales:
   social()
if len(sys.argv) == 1:
   parser.print_help()
