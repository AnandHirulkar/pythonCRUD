#importing required modules for the project
import tkinter
import tkinter.messagebox
import login, smartmart
import mysql.connector

#defined stocking report class
class StockingReport:

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

    #defined class initializer
    def __init__(self):
        #db connection establish
        self.init_dbconnect()
        #calling method to initialize the window
        self.init_window()

    #windows intializer method
    def init_window(self):

        #creating main window
        self.main_window = tkinter.Tk(className=" Stocking Report")
        #initializing size of window
        self.main_window.geometry("1024x768")

        # create a Menu widget adding to main window
        self.filemenu = tkinter.Menu(self.main_window)
        # display the menu on main window
        self.main_window.config(menu=self.filemenu)

        # closing the current windows on clicking X(close) button of window

        # create menu widget adding to main menu widget created above
        self.fmenuWid = tkinter.Menu(self.filemenu, tearoff=0)
        self.fmenuWid2 = tkinter.Menu(self.filemenu, tearoff=0)

        # create a toplevel menu
        self.filemenu.add_cascade(label="File", menu=self.fmenuWid)
        self.filemenu.add_cascade(label="Help", menu=self.fmenuWid2)

        # create a  menu inside options
        self.fmenuWid.add_command(label="Logout", command=self.logout)
        self.fmenuWid.add_command(label="Exit(Application)", command=self.clientSystemExit)
        self.fmenuWid2.add_command(label="About Us", command=self.aboutUs)

        # created frames for main window
        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)
        self.frame4 = tkinter.Frame(self.main_window)
        self.frame5 = tkinter.Frame(self.main_window)
        self.frame6 = tkinter.Frame(self.main_window)

        #defined labels for dynamic label content creation
        self.value1 = tkinter.StringVar()
        self.value2 = tkinter.StringVar()
        self.value3 = tkinter.StringVar()
        self.value4 = tkinter.StringVar()
        self.value5 = tkinter.StringVar()

        #creatign required labels
        self.label1 = tkinter.Label(self.frame1, text="Stocking Report", font=("", 16))
        self.label2 = tkinter.Label(self.frame2, text="Product Id", font=("", 12), padx=40)
        self.label3 = tkinter.Label(self.frame2, text="Product Name", font=("", 12), padx=40)
        self.label4 = tkinter.Label(self.frame2, text="Units in Stock", font=("", 12), padx=40)
        self.label6 = tkinter.Label(self.frame2, text="", font=("", 12), padx=40)

        #creating labels for dynamic stocking details
        self.prodIdLab = tkinter.Label(self.frame3, textvariable=self.value1, font=("", 12), padx=50)
        self.prodNameLab = tkinter.Label(self.frame3, textvariable=self.value2, font=("", 12), padx=50)
        self.unitsStockLab = tkinter.Label(self.frame3, textvariable=self.value3, font=("", 12), padx=50)
        self.unitsStatusLab = tkinter.Label(self.frame3, textvariable=self.value5, font=("", 12), padx=10)

        #creating label for status
        self.label5 = tkinter.Label(self.frame4, text="Status : ", font=("", 12), padx=50)

        #label for dynamic content generation for status
        self.statusStock = tkinter.Label(self.frame4, textvariable=self.value4, font=("", 12),pady = 20)

        #button for stock generation
        self.button = tkinter.Button(self.frame5, text="Generate Report", command=self.stockReport)

        # create button go back to main menu
        self.myButton2 = tkinter.Button(self.frame6, width=15, text='Back to main menu', command=self.clientExit)

        #label pack
        self.label1.pack()
        # self.label2.pack(side="left")
        # self.label3.pack(side="left")
        # self.label4.pack(side="left")
        # self.label6.pack(side="left")
        self.prodIdLab.pack(side="left")
        self.prodNameLab.pack(side="left")
        self.unitsStockLab.pack(side="left")
        self.unitsStatusLab.pack(side="left")
        self.statusStock.pack(side = "right")
        # self.label5.pack(side ="right")


        #button pack
        self.myButton2.pack()
        self.button.pack()

        #frames Pack
        self.frame6.pack(pady=10)
        self.frame1.pack(pady=50)
        self.frame2.pack()
        self.frame3.pack()
        # self.frame4.pack()
        self.frame5.pack()

        # tkinter mainloop to keep the window running
        tkinter.mainloop()

    # defined method for the menu exit option
    def clientExit(self):
        self.main_window.destroy()
        smartmart.SmartMart()

    # defined method for the menu logout option
    def logout(self):
        self.main_window.destroy()
        login.Login()

    # defined method for the menu about us option
    def aboutUs(self):
        tkinter.messagebox.showinfo('About Company',
                                    'Smart-Mart is a convenient store that is located in Toronto, Canada. The store needs an application to use it in its daily business.')

    #method for generation of stocking report
    def stockReport(self):
        self.tempProdNum = "Product Id" + "\n\n"
        self.tempProdName = "Product Name" + "\n\n"
        self.tempunits = "Units in Stock" + "\n\n"
        self.tempstatus = "Status" + "\n\n"
        self.mycursor.execute("select i.prodnum, p.prodname, sum(i.produnits) as 'units' from inventory i inner join (select prodnum,prodname from products)p on i.prodnum = p.prodnum group by i.prodnum,p.prodname")
        for values in self.mycursor:
            self.tempProdNum = self.tempProdNum + str(values[0]) + "\n"
            self.tempProdName = self.tempProdName + str(values[1]) + "\n"
            self.tempunits = self.tempunits + str(values[2]) + "\n"
            if(values[2] < 10):
                self.tempstatus = self.tempstatus + "Product added to order list" + "\n"
            else:
                self.tempstatus = self.tempstatus + "Available" + "\n"

        self.value1.set(self.tempProdNum)
        self.value2.set(self.tempProdName)
        self.value3.set(self.tempunits)
        self.value5.set(self.tempstatus)

    #defined to exit whole application
    def clientSystemExit(self):
        self.main_window.destroy()
