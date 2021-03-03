#importing required modules for the project
import tkinter
import tkinter.messagebox
import datetime
import re
import login, smartmart
import mysql.connector

#defined addproductclass
class AddProduct:

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

    #defined initializer for AddProduct class
    def __init__(self):
        #calling db connection initializer
        self.init_dbconnect()
        # Calling the windows initializer method for the creation of the windows
        self.init_windows()

    # defined method for creation of window
    def init_windows(self):
        # Create the main window.
        self.main_window = tkinter.Tk(className=' Add Product to Store')
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
        self.frame7 = tkinter.Frame(self.main_window)

        #deined label for page heading
        self.label1 = tkinter.Label(self.frame1, text="Product Add to Inventory", font=("", 16), pady=80)

        #defined label for product number
        self.label2 = tkinter.Label(self.frame2, text="Product Number* ", font=("", 14), padx=75)
        #defined entry widget for product number
        self.entry1 = tkinter.Entry(self.frame2, width=25)

        # defined label for product Units
        self.label3 = tkinter.Label(self.frame3, text="Product Units Received* ", font=("", 14), padx=45)
        # defined entry widget for product units
        self.entry2 = tkinter.Entry(self.frame3, width=25)

        # defined label for product price
        self.label4 = tkinter.Label(self.frame4, text="Product Wholesale Price($)* ", font=("", 14), padx=28)
        # defined entry widget for product price
        self.entry3 = tkinter.Entry(self.frame4, width=25)

        #defined label for product expiry
        self.label5 = tkinter.Label(self.frame5, text="Expiry Date(yyyy-mm-dd) ", font=("", 14), padx=34)
        #defined entry widget for product expiry details
        self.entry4 = tkinter.Entry(self.frame5,validate="key", width=25)

        #button to add product to inventory
        self.myButton1 = tkinter.Button(self.frame6, width=15, text='Add To Inventory', command=self.addProductInventory)
        #button added to clear input fields content
        self.myButton3 = tkinter.Button(self.frame6, width=15, text='Clear', command=self.clearContent)

        # create button go back to main menu
        self.myButton2 = tkinter.Button(self.frame7, width=15, text='Back to main menu', command=self.clientExit)

        #labels pack
        self.label1.pack()
        self.label2.pack(side="left")
        self.label3.pack(side="left")
        self.label4.pack(side="left")
        self.label5.pack(side="left")


        #entry pack
        self.entry1.pack()
        self.entry2.pack()
        self.entry3.pack()
        self.entry4.pack()

        #button pack
        self.myButton2.pack()
        self.myButton1.pack(padx = 20,side = "left")
        self.myButton3.pack()


        #frames pack
        self.frame7.pack(pady=10)
        self.frame1.pack()
        self.frame2.pack(pady=10)
        self.frame3.pack(pady=10)
        self.frame4.pack(pady=10)
        self.frame5.pack(pady=10)
        self.frame6.pack(pady=30)

        # tkinter mainloop to keep the window running
        tkinter.mainloop()

    #method for adding product to inventory
    def addProductInventory(self):
        if(self.entry1.get() == "" or self.entry2.get() == "" or self.entry3.get() == ""):
            tkinter.messagebox.showinfo('Product Status', "Please enter all the required details")
        else:
            try:
                checkProdValid = self.productValidation(self.entry1.get())
                expDate = self.validateExpDate(self.entry4.get())
                checkProdPrice = self.prodPriceValidation(self.entry3.get())
                if expDate == False:
                    raise CustomDateException
                elif (str(expDate) < str(datetime.date.today()) ):
                    raise CustomException

                if (checkProdValid == "lengthError"):
                    raise CustomProdLengthException
                elif (checkProdValid == "invalidprod"):
                    raise CustomProdException

                if (checkProdPrice == "priceException"):
                    raise CustomPriceException
                elif (checkProdPrice == "priceLengthException"):
                    raise CustomPriceLengthException


                self.mycursor.execute("select prodnum, prodwholpric, produnits from inventory")
                for x in self.mycursor:
                    if(str(self.entry1.get()) == str(x[0])):
                        prodSalePrice = 0
                        sqlProdSalePric = "select prodpric from products where prodnum = %s"
                        valProdPrice = (self.entry1.get(),)
                        self.mycursor.execute(sqlProdSalePric,valProdPrice)
                        prodSalePrice = ''.join(str(i) for i in self.mycursor.fetchone())
                        if (float(prodSalePrice) < float(self.entry3.get())):
                            raise CustomWholePriceException
                        prodWholePriceOld = x[1]
                        prodWholePriceNew = ((float(x[2]) * float(prodWholePriceOld)) + (float(self.entry3.get()) * float(self.entry2.get())))/(float(x[2]) + float(self.entry2.get()))
                        sql = "update inventory set produnits = produnits + %s, prodwholpric = %s, prodexpdate = %s where prodnum = %s"
                        val = (self.entry2.get(),prodWholePriceNew,expDate,self.entry1.get())
                        self.mycursor.execute(sql, val)
                        self.mydb.commit()
                        self.clearContent()
                        tkinter.messagebox.showinfo('Product Status', "Product Available Units Updated")
                        break
                else:
                    sqlProdSalePric = "select prodpric from products where prodnum = %s"
                    valProdPrice = (self.entry1.get(),)
                    self.mycursor.execute(sqlProdSalePric, valProdPrice)
                    try:
                        prodSalePrice = ''.join(str(i) for i in self.mycursor.fetchone())
                    except:
                        raise mysql.connector.errors.IntegrityError
                    if (float(prodSalePrice) < float(self.entry3.get())):
                        raise CustomWholePriceException
                    sql = "INSERT INTO inventory VALUES (%s, %s, %s, %s, %s)"
                    val = ("1",self.entry1.get(), self.entry2.get(), self.entry3.get(), expDate)
                    self.mycursor.execute(sql, val)
                    self.clearContent()
                    tkinter.messagebox.showinfo('Product Status', "Product Added to Inventory")
                    self.mydb.commit()
            except CustomProdException:
                tkinter.messagebox.showinfo('Error', "Product Number should only contain Alphanumeric Characters")
            except CustomPriceException:
                tkinter.messagebox.showinfo('Error', "Invalid Product Price should contain length(10,2)")
            except CustomPriceLengthException:
                tkinter.messagebox.showinfo('Error', "Product Price should not exceed 8 digits")
            except CustomProdLengthException:
                tkinter.messagebox.showinfo('Error', "Product Number should not exceed 8 characters")
            except CustomException:
                tkinter.messagebox.showinfo("Date Error", "Product seems already expired, please enter a future/today's date")
            except CustomDateException:
                tkinter.messagebox.showinfo("Date Format Error", "Incorrect data format, should be YYYY-MM-DD")
            except CustomWholePriceException:
                tkinter.messagebox.showinfo("Error", "WholeSale price is more than the Sale price")
            except mysql.connector.errors.IntegrityError:
                tkinter.messagebox.showinfo('Error', 'No Such Product Register! If adding a new product, Please register the product first.')
            except ValueError:
                tkinter.messagebox.showinfo("Error","Invalid Values Entered")
    #method to validate exp date
    def validateExpDate(self,expDate):
        if(expDate == ""):
            return None
        else:
            format = '%Y-%m-%d'
            try:
                datetime.datetime.strptime(str(expDate), format)
                return expDate
            except ValueError:
                return False
    #Product Number Validation
    def productValidation(self,productno):
        regex = '^[\w-]+$'
        try:
            if(len(productno) > 8):
                raise  CustomProdLengthException
            elif not re.match(regex,productno):
                raise CustomProdException
            else:
                return productno
        except CustomProdException:
            return "invalidprod"
        except CustomProdLengthException:
            return "lengthError"

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

    # defined method for the menu about us option
    def aboutUs(self):
        tkinter.messagebox.showinfo('About Company',
                                    'Smart-Mart is a convenient store that is located in Toronto, Canada. This application is developed to use it in its daily business.')

    #defined function to clear content
    def clearContent(self):
        self.entry1.delete(0, 'end')
        self.entry2.delete(0, 'end')
        self.entry3.delete(0,'end')
        self.entry4.delete(0,'end')

class CustomException(Exception):
    def __init__(self):
        super().__init__("Custom Exception")

class CustomDateException(Exception):
    def __init__(self):
        super().__init__("Invalid Date")

class CustomProdException(Exception):
    def __init__(self):
        super().__init__("Invalid Product Number")

class CustomProdLengthException(Exception):
    def __init__(self):
        super().__init__("Invalid Product Length")
class CustomPriceException(Exception):
    def __init__(self):
        super().__init__("Invalid Price")
class CustomPriceLengthException(Exception):
    def __init__(self):
        super().__init__("Invalid Price")

class CustomWholePriceException(Exception):
    def __init__(self):
        super().__init__("Invalid Price")

#ad = AddProduct()