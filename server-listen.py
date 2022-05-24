# Echo server program
import socket
import time
import threading
import queue

q = queue.Queue()

def rebre(con, ad):
    a = ""

    #demanar nom
    con.send("Indtrodueix el teu nom: \n".encode())
    nom = con.recv(2000)
    nom = nom.decode()

    #passo el nom a format correcte
    nomCorrecte = ""
    for i in range(len(nom)-1):
        nomCorrecte = nomCorrecte +  nom[i]

    #notificar els altres usuaris que m'he connectat
    for i in llistaCon:
            if ad == i[1]:
                pass
            else:
                missatgeAvis = nomCorrecte + " s'ha connectat. \n"
                i[0].sendto(missatgeAvis.encode(), i[1])

    #començem bucle
    while True:
        a = con.recv(2000)
        a = a.decode()


        #enviar missatge a la resta
        msg = nomCorrecte + ": " + a
        envia(msg, con, ad)


        #fromat correcte del text, utilitzo aixo per saber si s'ha enviat bye
        text = ""
        totalLletres = 0
        for lletra in a:
            totalLletres = totalLletres + 1
        if totalLletres >= 3:
            for i in range(3):
                text = text + a[i]

        #borro la conexio de la llista i finlitzo el thread
        if text == "bye":
            llistaCon.remove((con,ad))

            #aviso els altres que s'ha desconectat
            for i in llistaCon:
                    if ad == i[1]:
                        pass
                    else:
                        missatgeAvis = nomCorrecte + " s'ha desconectat. \n"
                        i[0].sendto(missatgeAvis.encode(), i[1])

            break


def envia(msg, con, ad):
    if len(llistaCon) != 0:
        for i in llistaCon:
            if ad == i[1]:
                pass
            else:
                i[0].sendto(msg.encode(), i[1])

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 8036            # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(10)
a = ""
b = ""
llistaCon = []


while True:
    conexio, adr = s.accept()
    llistaCon.append((conexio,adr))
    r = threading.Thread(target=rebre, args=(conexio,adr))
    r.start()

conexio.close()
s.close()
