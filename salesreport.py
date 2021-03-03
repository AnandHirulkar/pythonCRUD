#importing required modules for the project
import tkinter
import tkinter.messagebox
import login, smartmart
import mysql.connector

#defined SalesReport class
class SalesReport:

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

    # defined initializer for SalesReport class
    def __init__(self):
        # calling db connection initializer
        self.init_dbconnect()
        # Calling the windows initializer method for the creation of the windows
        self.init_window()

    # defined method for creation of window
    def init_window(self):
        # Create the main window.
        self.main_window = tkinter.Tk(className=" Sales Report")

        # Initiliazing window size.
        self.main_window.geometry("1024x768")

        # closing the current windows on clicking X(close) button of window

        # create a Menu widget adding to main window
        self.filemenu = tkinter.Menu(self.main_window)
        # display the menu on main window
        self.main_window.config(menu=self.filemenu)

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

        # initialized variables to be used for dynamic report details generation
        self.value1 = tkinter.StringVar()
        self.value2 = tkinter.StringVar()
        self.value3 = tkinter.StringVar()
        self.value4 = tkinter.StringVar()
        self.value5 = tkinter.StringVar()

        #defined labels for report generation
        self.label1 = tkinter.Label(self.frame1, text="Sales Report", font=("", 16))
        self.label2 = tkinter.Label(self.frame2, text="Product Name", font=("", 12),padx = 40)
        self.label3 = tkinter.Label(self.frame2, text="Number of Units", font=("", 12),padx = 40)
        self.label6 = tkinter.Label(self.frame2, text="Subtotal", font=("", 12),padx = 40)
        self.label4 = tkinter.Label(self.frame2, text="Total", font=("", 12),padx = 30)

        #dynamic details generation labels
        self.prodNameLab = tkinter.Label(self.frame3, textvariable=self.value1, font=("", 12), padx = 60)
        self.numUnitLab = tkinter.Label(self.frame3, textvariable=self.value2, font=("", 12), padx = 60)
        self.subtotalPriceLab = tkinter.Label(self.frame3, textvariable=self.value5, font=("", 12), padx = 40)
        self.totalPriceLab = tkinter.Label(self.frame3, textvariable=self.value3, font=("", 12), padx = 40)

        #Label for getting the total amount
        self.label5 = tkinter.Label(self.frame4, text="Total Amount : ", font=("", 12),padx = 10)
        self.totalLab = tkinter.Label(self.frame4, textvariable=self.value4, font=("", 12))

        #Button to generate report
        self.button = tkinter.Button(self.frame5, text="Generate Report", command=self.repGenerate)

        # create button go back to main menu
        self.myButton = tkinter.Button(self.frame6, width=15, text='Back to main menu', command=self.clientExit)

        #Labels pack
        self.label1.pack()
        # self.label2.pack(side = "left")
        # self.label3.pack(side = "left")
        # self.label6.pack(side = "left")
        # self.label4.pack(side = "left")
        self.prodNameLab.pack(side = "left")
        self.numUnitLab.pack(side = "left")
        self.subtotalPriceLab.pack(side = "left")
        self.totalPriceLab.pack(side = "left")
        self.totalLab.pack(side="right")
        self.label5.pack(side="right")

        #button pack
        self.myButton.pack()
        self.button.pack()

        #frames pack
        self.frame6.pack(pady = 10)
        self.frame1.pack(pady = 50)
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
        self.frame5.pack(pady = 20)

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

    # defined to exit whole application
    def clientSystemExit(self):
        self.main_window.destroy()

    # defined method for the menu about us option
    def aboutUs(self):
        tkinter.messagebox.showinfo('About Company',
                                    'Smart-Mart is a convenient store that is located in Toronto, Canada. The store needs an application to use it in its daily business.')

    #method for generation of the report
    def repGenerate(self):
        self.tempUnits = "Number of Units" + "\n\n"
        self.tempProdName = "Product Name" + "\n\n"
        self.tempsubtotal = "Subtotal" + "\n\n"
        self.temptotal = "Total" + "\n\n"
        self.tempSum = 0
        self.mycursor.execute(
            "select sum(b.units) as 'units', p.prodname, sum(amount) as 'subtotal', (sum(amount)*(13/100)) + (sum(amount)) as 'total' from billingdetails b inner join (select prodnum, prodname from products)p on b.prodnum = p.prodnum group by p.prodnum")
        for values in self.mycursor:
            self.tempUnits = self.tempUnits + str(values[0]) + "\n"
            self.tempProdName = self.tempProdName + str(values[1]) + "\n"
            self.tempsubtotal = self.tempsubtotal + str(values[2]) + "\n"
            self.temptotal = self.temptotal + str(float("{:.2f}".format(values[3]))) + "\n"
            self.tempSum += values[3]


        self.tempSum = float("{:.2f}".format(self.tempSum))
        self.value1.set(self.tempProdName)
        self.value2.set(self.tempUnits)
        self.value5.set(self.tempsubtotal)
        self.value3.set(self.temptotal)

        # for items in range(len(list)):
        #     sum = sum + float(list[items])
        self.value4.set(self.tempSum)

