#importing required modules for the project
import tkinter
import tkinter.messagebox
import smartmart
import mysql.connector

class Login:
    #Login class initializer
    def __init__(self):
        # database connection
        self.init_dbconnect()

        # Calling the windows initializer method for the creation of the windows
        self.initLoginWindow()

    #database connection
    def init_dbconnect(self):
        lines = (line.rstrip('\n') for line in open("dbconnect.txt"))
        dbList = []
        for values in lines:
            dbList.append(values)
        hostname = dbList[0].split("=")[1]
        username = dbList[1].split("=")[1]
        password = dbList[2].split("=")[1]
        database = dbList[3].split("=")[1]

        self.mydb = mysql.connector.connect(host=hostname,
                                       user=username,
                                       passwd=password,
                                       database=database)
        self.mycursor = self.mydb.cursor(buffered=True)
    #Initializing the windows
    def initLoginWindow(self):

        # Create the main window.
        self.main_window = tkinter.Tk(className='Login')
        # Initiliazing window size.
        self.main_window.geometry("1024x768")

        #create a Menu widget adding to main window
        self.filemenu = tkinter.Menu(self.main_window)
        #display the menu on main window
        self.main_window.config(menu=self.filemenu)

        #create menu widget adding to main menu widget created above
        self.fmenuWid = tkinter.Menu(self.filemenu, tearoff=0)
        self.fmenuWid2 = tkinter.Menu(self.filemenu, tearoff=0)

        # create a toplevel menu
        self.filemenu.add_cascade(label="File", menu=self.fmenuWid)
        self.filemenu.add_cascade(label="Help", menu=self.fmenuWid2)

        # create a  menu inside options
        self.fmenuWid.add_command(label="Exit(Application)", command=self.clientExit)
        self.fmenuWid2.add_command(label="About Us", command=self.aboutUs)

        #created frames for main window
        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)
        self.frame4 = tkinter.Frame(self.main_window)

        #created labels widgets for the frames
        self.label1 = tkinter.Label(self.frame1,text = "Welcome to Smart-Mart Store Application", font = ("",21),pady = 100)
        self.label2 = tkinter.Label(self.frame2, text="Username : ", font=("", 14),padx = 10)
        self.label3 = tkinter.Label(self.frame3, text="Password : ", font=("", 14),padx = 10)

        #created entry widgets
        self.entry1 = tkinter.Entry(self.frame2,width = 25)
        self.entry2 = tkinter.Entry(self.frame3,width = 25,show="*")

        #created button for login
        self.button = tkinter.Button(self.frame4,text = "Login", width = 14, command=self.login)

        #label packing
        self.label1.pack()
        self.label2.pack(side = "left")
        self.label3.pack(side = "left")

        #Entry Pack
        self.entry1.pack(side = "left")
        self.entry2.pack(side = "left")

        #Button Pack
        self.button.pack()

        #Frames Pack
        self.frame1.pack()
        self.frame2.pack(pady = 20)
        self.frame3.pack(pady = 20)
        self.frame4.pack(pady = 5)

        #tkinter mainloop to keep the window running
        tkinter.mainloop()

    #defined method for the menu exit option
    def clientExit(self):
        quit()

    # defined method for the menu About us option
    def aboutUs(self):
        tkinter.messagebox.showinfo('About Company',
                                    'Smart-Mart is a convenient store that is located in Toronto, Canada. This application is developed to use it in its daily business.')

    # defined method for verifying login details
    def login(self):
        self.mycursor.execute("select * from login")
        for i in self.mycursor:
            if(self.entry1.get() == i[0] and self.entry2.get() == i[1]):
                self.main_window.destroy()
                sm = smartmart.SmartMart()
                break

        else:
            tkinter.messagebox.showinfo('Invalid username/password', 'Invalid Username/Password! Please try Again.')


#main method
def main():
    login = Login()

#main method call
if __name__ == '__main__':
    main()