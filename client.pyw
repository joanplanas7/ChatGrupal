from threading import Thread
import threading
from ChatFns import *
from tkinter import *

#---------------------------------------------------#
#---------INITIALIZE CONNECTION VARIABLES-----------#
#---------------------------------------------------#
WindowTitle = 'JChat v0.1 - Client'
HOST = 'localhost'
PORT = 8036
s = socket(AF_INET, SOCK_STREAM)
actiu = True



#---------------------------------------------------#
#------------------ MOUSE EVENTS -------------------#
#---------------------------------------------------#
def ClickAction():
    #Write message to chat window
    EntryText = FilteredMessage(EntryBox.get("0.0",END))

    LoadMyEntry(ChatLog, EntryText)

    #Scroll to the bottom of chat windows
    ChatLog.yview(END)

    #Erace previous message in Entry Box
    EntryBox.delete("0.0",END)



    text = ""
    totalLletres = 0
    for lletra in EntryText:
        totalLletres = totalLletres + 1
    if totalLletres >= 3:
        for i in range(3):
            text = text + EntryText[i]
        print(text)

    if text == "bye":
        #print("entra")
         base.destroy()

    #Send my mesage to all others
    s.sendall(EntryText.encode())




#---------------------------------------------------#
#----------------- KEYBOARD EVENTS -----------------#
#---------------------------------------------------#
def PressAction(event):
	EntryBox.config(state=NORMAL)
	ClickAction()
def DisableEntry(event):
	EntryBox.config(state=DISABLED)


#---------------------------------------------------#
#-----------------GRAPHICS MANAGEMENT---------------#
#---------------------------------------------------#

#Create a window
base = Tk()
base.title(WindowTitle)
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create a Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.insert(END, "Connecting to your partner..\n")
ChatLog.config(state=DISABLED)

#Bind a scrollbar to the Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create the Button to send message
SendButton = Button(base, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E",
                    command=ClickAction)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.focus_set()
EntryBox.bind("<Return>", DisableEntry)
EntryBox.bind("<KeyRelease-Return>", PressAction)

#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)


#---------------------------------------------------#
#----------------CONNECTION MANAGEMENT--------------#
#---------------------------------------------------#

def ReceiveData():
    try:
        s.connect((HOST, PORT))
        LoadConnectionInfo(ChatLog, '[ Succesfully connected ]\n---------------------------------------------------------------')
    except:
        LoadConnectionInfo(ChatLog, '[ Unable to connect ]')
        return

    while 1:
        try:
            data = s.recv(1024)
            print(data)
        except:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
        if data != '':
            LoadOtherEntry(ChatLog, data.decode())
            if base.focus_get() == None:
                FlashMyWindow(WindowTitle)
                playsound('notif.wav')

        else:
            LoadConnectionInfo(ChatLog, '\n [ Your partner has disconnected ] \n')
            break
    #s.close()



t = threading.Thread(target=ReceiveData, daemon=True)
t.start()


base.mainloop()


#EntryBox.focus_set()
