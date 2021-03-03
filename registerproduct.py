#importing required modules for the project
import tkinter
import tkinter.messagebox
import re
import smartmart, login
import mysql.connector

#defined RegisterProduct class
class RegisterProduct:

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

    # defined initializer for RegisterProduct class
    def __init__(self):
        #database connection
        self.init_dbconnect()
        # Calling the windows initializer method for the creation of the windows
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # Create the main window.
        self.main_window = tkinter.Tk(className=' Product Registeration')

        # Initiliazing window size.
        self.main_window.geometry("1024x768")

        #closing the current windows on clicking X(close) button of window
        # self.main_window.protocol("WM_DELETE_WINDOW", self.clientExit)

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
        self.frame7 = tkinter.Frame(self.main_window)

        #create label for frame1
        self.label1 = tkinter.Label(self.frame1,text = "Product Registeration", font=("",16),pady = 30)

        # create label for frame2
        self.label2 = tkinter.Label(self.frame2, text="Product Number ", font=("", 14),padx = 50)
        # create entry widget for frame1
        self.entry1 = tkinter.Entry(self.frame2,width = 25)

        # create label for frame3
        self.label3 = tkinter.Label(self.frame3, text="Product Name ", font=("", 14),padx = 58)
        # create entry widget for frame3
        self.entry2 = tkinter.Entry(self.frame3,width = 25)

        # create label for frame4
        self.label4 = tkinter.Label(self.frame4, text="Product Description ", font=("", 14),padx = 35)
        # create text box widget for frame4
        self.text1 = tkinter.Text(self.frame4,width = 19,height = 10)

        # create label for frame5
        self.label5 = tkinter.Label(self.frame5, text="Product Unit Price ($) ", font=("", 14),padx = 29)
        # create entry widget for frame5
        self.entry4 = tkinter.Entry(self.frame5, width = 25)

        # create button for registering product
        self.myButton1 = tkinter.Button(self.frame6, width=15, text='Register Product', command=self.registerCheck)
        #button created to clear input fields content
        self.myButton3 = tkinter.Button(self.frame6, width=15, text='Clear', command=self.clearContent)
        #create button go back to main menu
        self.myButton2 = tkinter.Button(self.frame7, width=15, text='Back to main menu', command=self.clientExit)


        #Label Pack
        self.label1.pack()
        self.label2.pack(side = "left")
        self.label3.pack(side = "left")
        self.label4.pack(side = "left")
        self.label5.pack(side = "left")

        #Entry Pack
        self.entry1.pack()
        self.entry2.pack()
        self.text1.pack()
        self.entry4.pack()

        #Button Pack
        self.myButton2.pack()
        self.myButton1.pack(side = "left")
        self.myButton3.pack(padx = 20)


        #Frame Pack
        self.frame7.pack(pady = 10)
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack(pady = 10)
        self.frame4.pack(pady = 10)
        self.frame5.pack(pady = 10)
        self.frame6.pack(pady = 30)

        # tkinter mainloop to keep the window running
        tkinter.mainloop()

    # defined method for the menu exit option
    def clientExit(self):
        self.main_window.destroy()
        smartmart.SmartMart()

    #defined to exit whole application
    def clientSystemExit(self):
        self.main_window.destroy()

    # defined method for the menu logout option
    def logout(self):
        self.main_window.destroy()
        login.Login()

    # defined method for the menu About us option
    def aboutUs(self):
        tkinter.messagebox.showinfo('About Company',
                                    'Smart-Mart is a convenient store that is located in Toronto, Canada. This application is developed to use it in its daily business.')

    # defined method for the Registering a new product button option
    def registerCheck(self):
        try :
            #validating input values
            checkProdValid = self.productValidation(self.entry1.get())
            checkProdName = self.productNameValidation(self.entry2.get())
            checkProdPrice = self.prodPriceValidation(self.entry4.get())

            if(checkProdValid == "lengthError"):
                raise CustomProdLengthException
            elif(checkProdValid == "invalidprod"):
                raise CustomProdException

            if(checkProdName == "invalidnamelength"):
                raise CustomProdNameLengthException
            elif(checkProdName == "nameError"):
                raise CustomProdNameException

            if(checkProdPrice == "priceException"):
                raise CustomPriceException
            elif(checkProdPrice == "priceLengthException"):
                raise CustomPriceLengthException

            #checking if all required values are entered
            if(self.entry1.get() == "" or self.entry2.get() == "" or self.entry4.get() == "" or self.text1.get(1.0,'end') == ""):
                tkinter.messagebox.showinfo('Message', 'Please provide all the required values to register a product')
            else:
                try:
                    # Insert many records using parameterized statements
                    sql = "INSERT INTO products VALUES (%s, %s, %s, %s)"
                    val = (checkProdValid,self.entry2.get(),self.text1.get(1.0,'end'),self.entry4.get())
                    self.mycursor.execute(sql,val)
                    self.mydb.commit()
                    self.clearContent()
                    tkinter.messagebox.showinfo('Message', 'Product Added')
                except mysql.connector.errors.IntegrityError:
                    tkinter.messagebox.showinfo('Error', 'Product already Registered! Try Adding another product')
        except CustomProdNameLengthException:
            tkinter.messagebox.showinfo('Error', "Product Name should not exceed 20 characters")
        except CustomPriceException:
            tkinter.messagebox.showinfo('Error', "Invalid Product Price should contain length(10,2)")
        except CustomProdException:
            tkinter.messagebox.showinfo('Error', "Product Number should only contain Alphanumeric Characters")
        except CustomProdNameException:
            tkinter.messagebox.showinfo('Error',"Product name should contain only alphabet character values")
        except CustomProdLengthException:
            tkinter.messagebox.showinfo('Error', "Product Number should not exceed 8 characters")
        except CustomPriceLengthException:
            tkinter.messagebox.showinfo('Error', "Product Price should not exceed 8 digits")
        except mysql.connector.errors.DataError:
            tkinter.messagebox.showinfo('Error',"Trying to insert invalid data! Please Check")
    #defined function to clear content
    def clearContent(self):
        self.entry1.delete(0, 'end')
        self.entry2.delete(0, 'end')
        self.text1.delete(1.0,'end')
        self.entry4.delete(0,'end')

    #method to validation product number
    def productValidation(self,productno):
        regex = '^[\w-]+$'
        try:
            #checking if length exceeds 8
            if(len(productno) > 8):
                raise  CustomProdLengthException
            #checking if productnum only contains alphanumeric value
            elif not re.match(regex,productno):
                raise CustomProdException
            else:
                return productno
        except CustomProdException:
            return "invalidprod"
        except CustomProdLengthException:
            return "lengthError"

    #product name validation
    def productNameValidation(self,prodName ):
        regex = '^[a-zA-Z0-9!@#$&() .+,/]+$'
        #regex = '^[a-zA-Z0-9!@#$&()\\-`.+,/\"]*$'
        #regex = '^[a-zA-Z0-9!@#$&()`.+,/"-]*$'
        try:
            if not re.match(regex,prodName):
                raise CustomProdNameException
            elif(len(prodName) > 20):
                raise CustomProdNameLengthException
            else:
                return prodName
        except mysql.connector.errors.DataError:
            return "invalidnamelength"
        except CustomProdNameException:
            return "nameError"
        except CustomProdNameLengthException:
            return "invalidnamelength"

    #checking product price validation
    def prodPriceValidation(self,checkPrice):
        #regex = '^\d(\.\d{1,4})?$'
        regex = '^\d+(,\d{3})*(\.\d{1,5})?$'
        try :
            if not re.match(regex,checkPrice):
                raise CustomPriceException
            elif(len(checkPrice) > 8):
                raise CustomPriceLengthException

            else :
                return checkPrice
        except CustomPriceException:
            return "priceException"
        except CustomPriceLengthException:
            return "priceLengthException"



#custom exception class created for prodnum exceptions
class CustomProdException(Exception):
    def __init__(self):
        super().__init__("Invalid Product Number")
#custom exception class created for prodnum exceptions
class CustomProdLengthException(Exception):
    def __init__(self):
        super().__init__("Invalid Product Length")
#custom exception class created for prod name exceptions
class CustomProdNameException(Exception):
    def __init__(self):
        super().__init__("Invalid Product Name")
#custom exception class created for prod name length exceptions
class CustomProdNameLengthException(Exception):
    def __init__(self):
        super().__init__("Invalid Product Length")

#custom exception class created for prod price exceptions
class CustomPriceException(Exception):
    def __init__(self):
        super().__init__("Invalid Price")
#custom exception class created for prod price length exceptions
class CustomPriceLengthException(Exception):
    def __init__(self):
        super().__init__("Invalid Price")
