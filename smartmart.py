#importing required modules for the project
import tkinter
import tkinter.messagebox
import login
import registerproduct, individualbilling, salesreport, addtoinventory, stockingreport

#defined SmartMart class
class SmartMart:
    #defined initializer for SmartMart class
    def __init__(self):
        #Calling the windows initializer method for the creation of the windows
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # Create the main window.
        self.main_window = tkinter.Tk(className=' Smart Mart Application')

        # Initiliazing window size.
        self.main_window.geometry("1024x768")

        # create a Menu widget adding to main window
        self.filemenu = tkinter.Menu(self.main_window)
        # display the menu on main window
        self.main_window.config(menu=self.filemenu)

        # create menu widget adding to main menu widget created above
        self.fmenuWid = tkinter.Menu(self.filemenu,tearoff = 0)
        self.fmenuWid2 = tkinter.Menu(self.filemenu, tearoff=0)

        # create a toplevel menu
        self.filemenu.add_cascade(label="File", menu=self.fmenuWid)
        self.filemenu.add_cascade(label="Help", menu=self.fmenuWid2)

        # create a  menu inside options
        self.fmenuWid.add_command(label="Logout", command=self.logout)
        self.fmenuWid.add_command(label="Exit(Application)", command=self.clientExit)
        self.fmenuWid2.add_command(label="About Us", command=self.aboutUs)

        # created frames for main window
        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)

        # created labels widgets for the frames
        self.label1 = tkinter.Label(self.frame1,text='Smart Mart Application Home Page', font=("", 18), pady = 50)
        self.label2 = tkinter.Label(self.frame2,text='Select from below', font=("", 16),pady = 10)

        # created button for Different app options
        self.myButton1 = tkinter.Button(self.frame3,height= 1,width=26, text = 'Register Product', command = self.registerProduct)
        self.myButton2 = tkinter.Button(self.frame3,height= 1,width=26, text='Individual Billing', command=self.indBilling)
        self.myButton3 = tkinter.Button(self.frame3,height= 1,width=26, text='Sales Report', command=self.salesReport)
        self.myButton4 = tkinter.Button(self.frame3,height= 1,width=26, text='Add Product to store', command=self.shipProduct)
        self.myButton5 = tkinter.Button(self.frame3,height= 1,width=26, text='Stocking Report', command=self.stockReport)

        #Buttons pack
        self.myButton1.pack(pady = 10)
        self.myButton2.pack(pady = 10)
        self.myButton3.pack(pady = 10)
        self.myButton4.pack(pady = 10)
        self.myButton5.pack(pady = 10)

        #Label Pack
        self.label1.pack()
        self.label2.pack()

        #Frame Pack
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()

        #tkinter mainloop to keep the window running
        tkinter.mainloop()

    # defined method for the menu exit option
    def clientExit(self):
        self.main_window.destroy()

    # defined method for the menu logout option
    def logout(self):
        self.main_window.destroy()
        login.Login()

    # defined method for the menu About us option
    def aboutUs(self):
        tkinter.messagebox.showinfo('About Company', 'Smart-Mart is a convenient store that is located in Toronto, Canada. The store needs an application to use it in its daily business.')

    # defined method for the Registering a new product button option
    def registerProduct(self):
        self.main_window.destroy()
        registerproduct.RegisterProduct()

    # defined method for the IndividualBilling button option
    def indBilling(self):
        self.main_window.destroy()
        individualbilling.IndividualBilling()

    # defined method for the SalesReport button option
    def salesReport(self):
        self.main_window.destroy()
        salesreport.SalesReport()

    # defined method for the Received Product add to inventory button option
    def shipProduct(self):
        self.main_window.destroy()
        addtoinventory.AddProduct()

    # defined method for the Stocking Report button option
    def stockReport(self):
        self.main_window.destroy()
        stockingreport.StockingReport()
