#importing required modules for the project
import tkinter
import tkinter.messagebox
import smartmart, login
import datetime
import mysql.connector
import uuid

#defined IndividualBilling class
class IndividualBilling:
    #Defined list to be used for added product details
    prodNumList = []
    prodPriceList = []
    prodUnitsList = []
    amountList = []


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

    # defined initializer for IndividualBilling class
    def __init__(self):
        #db connection
        self.init_dbconnect()
        # Calling the windows initializer method for the creation of the windows
        self.init_window()

    # defined method for creation of window
    def init_window(self):
        # Create the main window.
        self.main_window = tkinter.Tk(className=" Shoppers Billing")

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
        self.frame8 = tkinter.Frame(self.main_window)

        #initialized variabled to be used for dynamic billing details generation
        self.value1 = tkinter.StringVar()
        self.prodNum = tkinter.StringVar()
        self.prodP= tkinter.StringVar()
        self.prodUnits = tkinter.StringVar()
        self.amount = tkinter.StringVar()

        # created labels widgets for the frames
        self.label1 = tkinter.Label(self.frame1, text="Billing Application", font=("", 18), pady=80)

        #created label for frame2
        self.label2 = tkinter.Label(self.frame2, text="Product Number ", font=("", 14), padx=54)
        #created entry for product num
        self.entry1 = tkinter.Entry(self.frame2, width=25)

        # created label for frame3
        self.label3 = tkinter.Label(self.frame3, text="Number of Units", font=("", 14), padx=58)
        # created entry for product units
        self.entry2 = tkinter.Entry(self.frame3, width=25)

        # created label for frame4
        self.label4 = tkinter.Label(self.frame4, text="Status : ", font=("", 12), padx=20)
        self.label5 = tkinter.Label(self.frame4, textvariable = self.value1,font=("", 10), padx=20)



        #creatd buttons for adding product and generatig bill
        self.myButton1 = tkinter.Button(self.frame5, width=15, text='Add To Cart', command=self.productAdd)
        self.myButton2 = tkinter.Button(self.frame5, width=15, text='Generate Bill', command=self.generateBill)
        self.myButton4 = tkinter.Button(self.frame5, width=15, text='Remove from Cart', command=self.productRemove)

        # create button go back to main menu
        self.myButton3 = tkinter.Button(self.frame8, width=15, text='Back to main menu', command=self.clientExit)

        # created label for productnum, num of units and amount
        self.label6 = tkinter.Label(self.frame6, text="Product Number ", font=("", 12), padx=20)
        self.label12 = tkinter.Label(self.frame6, text="Product Price", font=("", 12), padx=20)
        self.label7 = tkinter.Label(self.frame6, text="Number of Units", font=("", 12), padx=20)
        self.label8 = tkinter.Label(self.frame6, text="Amount ", font=("", 12), padx=20)

        #created labels for dynamic generation of the add products details
        self.label9 = tkinter.Label(self.frame7, textvariable = self.prodNum,font=("", 10), padx=80)
        self.label13 = tkinter.Label(self.frame7, textvariable = self.prodP,font=("", 10), padx=60)
        self.label10 = tkinter.Label(self.frame7, textvariable = self.prodUnits,font=("", 10), padx=60)
        self.label11 = tkinter.Label(self.frame7, textvariable = self.amount,font=("", 10), padx=50)

        #labels pack
        self.label1.pack()
        self.label2.pack(side="left")
        self.label3.pack(side="left")
        self.label4.pack(side="left")
        self.label5.pack(side="left")
        #self.label6.pack(side="left")
        #self.label12.pack(side="left")
        #self.label7.pack(side="left")
        #self.label8.pack(side="left")
        self.label9.pack(side="left")
        self.label13.pack(side="left")
        self.label10.pack(side="left")
        self.label11.pack(side="left")



        #entry widget pack
        self.entry1.pack()
        self.entry2.pack()

        #buttons pack
        self.myButton3.pack(side="left")
        self.myButton1.pack(side = "left",padx = 10)
        self.myButton2.pack(side = "left",padx = 30)
        self.myButton4.pack(side = "left")


        #frames pack
        self.frame8.pack(pady=10)
        self.frame1.pack()
        self.frame2.pack(pady=10)
        self.frame3.pack(pady=10)
        self.frame4.pack(pady=10)
        self.frame5.pack(pady=50)
        self.frame6.pack(pady=10)
        self.frame7.pack(pady=10)

        # tkinter mainloop to keep the window running
        tkinter.mainloop()


##########################BIll Generation#####################

    # defined method for the generation of bill button
    def generateBill(self):
        #self.id = uuid.uuid1()
        self.date = datetime.date.today()
        self.billId = str(uuid.uuid4().fields[-1])[:5]
        #checking if a product is added
        if(len(self.prodNumList) == 0):
            tkinter.messagebox.showinfo("Alert", "No Products Added")
        #generation of bill in a new child window
        else:
            self.sno = 1
            self.subtotalTable = 0
            for values in self.prodNumList:
                #print(values)
                listIndex = self.prodNumList.index(values)
                produnit = self.prodUnitsList[listIndex]
                prodpric = self.prodPriceList[listIndex]
                prodamount = (float(produnit) * float(prodpric))
                sql1 = "insert into billingdetails values(%s, %s, %s, %s, %s)"
                val1 = (self.billId, self.sno, values, produnit, prodamount,)
                self.mycursor.execute(sql1,val1)

                self.subtotalTable = self.subtotalTable + prodamount

                sqlRemove = "update inventory set prodUnits = produnits - %s where prodnum = %s "
                valRemove = (produnit,values,)
                self.mycursor.execute(sqlRemove,valRemove)

                self.sno += 1
                self.mydb.commit()

            self.taxTotal = (13*(self.subtotalTable/100))
            self.totalAmountTable = self.subtotalTable + self.taxTotal
            sql2 = "insert into billing values(%s, %s, %s, %s, %s)"
            val2 = (self.billId, self.date, self.subtotalTable,self.taxTotal ,self.totalAmountTable )
            self.mycursor.execute(sql2,val2)
            self.mydb.commit()
            #created a child window
            self.child_window = tkinter.Tk(className=" Bill ")
            #initialized the size of the window
            self.child_window.geometry("1024x768")
            #created frames using Frame widget
            self.child_frame1 = tkinter.Frame(self.child_window)
            self.child_frame2 = tkinter.Frame(self.child_window)
            self.child_frame3 = tkinter.Frame(self.child_window)
            self.child_frame3 = tkinter.Frame(self.child_window)
            self.child_frame4 = tkinter.Frame(self.child_window)
            self.child_frame5 = tkinter.Frame(self.child_window)
            self.child_frame6 = tkinter.Frame(self.child_window)
            self.child_frame7 = tkinter.Frame(self.child_window)

            #temp variables for dynamic content generation
            self.billId = "Bill#" + "\n\n" + self.billId
            self.prodNumber = "Product Number" + "\n\n"
            self.prodGenerateUnits = "Product Units" + "\n\n"
            self.prodAmount = "Amount" + "\n\n"
            self.subtotal = 0

            #fetching details of the added products
            for items in range(len(self.prodNumList)):
                self.prodNumber = self.prodNumber + (str(self.prodNumList[items]) + '\n')
            for items in range(len(self.prodUnitsList)):
                self.prodGenerateUnits = self.prodGenerateUnits + (str(self.prodUnitsList[items]) + '\n')
            for items in range(len(self.amountList)):
                self.prodAmount = self.prodAmount + (str(self.amountList[items]) + '\n')


            #calculating sub total of all the products
            for items in range(len(self.amountList)):
                self.subtotal = self.subtotal + self.amountList[items]

            #calculating hst
            self.hst = (self.subtotal * 13) / 100

            #calculating total amount including hst
            self.totalAmount = float("{:.2f}".format(self.subtotal + self.hst))



            #creating labels for bill generation details
            self.child_label1 = tkinter.Label(self.child_frame1, text="Billing Details", font=("", 16), pady=40)
            self.child_label14 = tkinter.Label(self.child_frame2, text="Bill#", font=("", 12), padx=60)
            self.child_label2 = tkinter.Label(self.child_frame2, text="Product Number", font=("", 12), padx=60)
            self.child_label3 = tkinter.Label(self.child_frame2, text="Product Units", font=("", 12), padx=60)
            self.child_label4 = tkinter.Label(self.child_frame2, text="Amount", font=("", 12), padx=40)
            self.child_label15 = tkinter.Label(self.child_frame3, text =self.billId, font=("", 12), padx = 50,pady=10)
            self.child_label5 = tkinter.Label(self.child_frame3, text =self.prodNumber, font=("", 12), padx = 100,pady=10)
            self.child_label6 = tkinter.Label(self.child_frame3, text =self.prodGenerateUnits, font=("", 12), padx = 100,pady=10)
            self.child_label7 = tkinter.Label(self.child_frame3, text =self.prodAmount, font=("", 12), padx = 40,pady=10)
            self.child_label8 = tkinter.Label(self.child_frame4, text="SubTotal", font=("", 12),padx=125, pady=10)
            self.child_label9 = tkinter.Label(self.child_frame4, text = self.subtotal, font=("", 12), pady=10)
            self.child_label10 = tkinter.Label(self.child_frame5, text="Hst(13%)", font=("", 12),padx=120, pady=10)
            self.child_label11 = tkinter.Label(self.child_frame5, text=self.hst, font=("", 12), pady=10)
            self.child_label12 = tkinter.Label(self.child_frame6, text="Total", font=("", 12),padx=130, pady=10)
            self.child_label13 = tkinter.Label(self.child_frame6, text=self.totalAmount, font=("", 12), pady=10)
            self.child_label16 = tkinter.Label(self.child_frame7, text="Date : ", font=("", 12),padx=100, pady=10)
            self.child_label17 = tkinter.Label(self.child_frame7, text=self.date, font=("", 12), pady=10)

            # Packing Labels
            self.child_label1.pack(side="left")
            # self.child_label14.pack(side="left")
            # self.child_label2.pack(side="left")
            # self.child_label3.pack(side="left")
            # self.child_label4.pack(side="left")
            self.child_label15.pack(side = "left")
            self.child_label5.pack(side = "left")
            self.child_label6.pack(side = "left")
            self.child_label7.pack(side = "left")
            self.child_label9.pack(side="right")
            self.child_label8.pack(side = "right")
            self.child_label11.pack(side="right")
            self.child_label10.pack(side = "right")
            self.child_label13.pack(side="right")
            self.child_label12.pack(side="right")
            self.child_label17.pack(side="right")
            self.child_label16.pack(side="right")


            # Packing frames
            self.child_frame1.pack()
            self.child_frame2.pack()
            self.child_frame3.pack()
            self.child_frame4.pack()
            self.child_frame5.pack()
            self.child_frame6.pack()
            self.child_frame7.pack()

            # self.main_window.destroy()
            # self.__init__()
            # self.prodNumList.clear()
            # self.prodUnitsList.clear()
            # self.prodPriceList.clear()
            # self.amountList.clear()
            # tkinter mainloop to keep the window running
            self.clear_content()
            tkinter.mainloop()





    #for adding added product details on same page
    def productAdd(self):
        try:
            #checking if a both the required entries are entered
            if(self.entry1.get() == "" or self.entry2.get() == ""):
                self.value1.set("Please Provide both the values to add product")
            #checking if added quantity is less than 1
            elif(int(self.entry2.get()) < 1):
                self.value1.set("Quantity can't be less than 1")
            #adding product to cart
            else :
                self.mycursor.execute("select prodnum from inventory")
                for value in self.mycursor:
                    if(str(self.entry1.get()) == ''.join(value)):
                        sql = "select produnits from inventory where prodnum = %s"
                        valuep = (self.entry1.get(),)
                        self.mycursor.execute(sql,valuep)
                        for value in self.mycursor:
                            if(int(''.join(str(i) for i in value)) < int(self.entry2.get())):
                                tkinter.messagebox.showinfo('Info', 'Insufficient quantity available in store')
                                break
                        else:
                            if(self.prodNumList.count(self.entry1.get()) == 1):
                                print(self.prodNumList[0])
                                tkinter.messagebox.showinfo('Info', 'Product already present in cart! Remove the product and add again to chance quantity')
                                break
                            else:
                                # code for the generation of the added products details to same page

                                sql = "select prodpric from products where prodnum = %s "
                                val = (self.entry1.get(),)
                                self.mycursor.execute(sql,val)
                                self.prodprice = ''.join(str(i) for i in self.mycursor.fetchone())
                                # appending the list with the details of the added products
                                self.prodNumList.append(self.entry1.get())
                                self.prodUnitsList.append(self.entry2.get())
                                self.prodPriceList.append(self.prodprice)
                                self.amountList.append(float(self.prodprice) * float(self.entry2.get()))

                                # defined temp variables for dynamic product added details
                                self.tempvar1 = "Product Number" + "\n\n"
                                self.tempvar2 = "Number of Units"+ "\n\n"
                                self.tempvar3 = "Total Amount"+ "\n\n"
                                self.tempvar4 = "Product Price"+ "\n\n"

                                # adding to temp variable for dynamic product added details generation
                                for i in range(len(self.prodNumList)):
                                    self.tempvar1 = self.tempvar1 + (str(self.prodNumList[i]) + '\n')
                                for i in range(len(self.prodUnitsList)):
                                    self.tempvar2 = self.tempvar2 + (str(self.prodUnitsList[i]) + '\n')
                                for i in range(len(self.amountList)):
                                    self.tempvar3 = self.tempvar3 + (str(self.amountList[i]) + '\n')
                                for i in range(len(self.prodPriceList)):
                                    self.tempvar4 = self.tempvar4 + (str(self.prodPriceList[i]) + '\n')

                                # Specifying that the product has been added to cart
                                self.value1.set("Product Added to cart")
                                # setting values for the labels defined in main windows for dynamic content generation
                                self.prodNum.set(self.tempvar1)
                                self.prodUnits.set(self.tempvar2)
                                self.amount.set(self.tempvar3)
                                self.prodP.set(self.tempvar4)

                                # setting entry to blank after the product is added
                                self.entry1.delete(0, tkinter.END)
                                self.entry2.delete(0, tkinter.END)
                                break
                            break
                        break
                else:
                    tkinter.messagebox.showinfo('Info', 'Product Not available')
        except ValueError:
            tkinter.messagebox.showinfo('Error',"Invalid Value entered! Please Check")

    def productRemove(self):
        # checking if a both the required entries are entered
        if (self.entry1.get() == ""):
            self.value1.set("Please Provide product id to remove the product")
        # code for the generation of the added products details to same page
        else:
            try:
                index = self.prodNumList.index(self.entry1.get())

                # appeding the list with the details of the added products
                self.prodNumList.remove(self.entry1.get())
                del self.prodUnitsList[index]
                del self.prodPriceList[index]
                del self.amountList[index]

                #defined temp variables for dynamic product added details
                self.tempvar1 ="Product Number" + "\n\n"
                self.tempvar2 ="Product Price" + "\n\n"
                self.tempvar3 ="Number of Units" + "\n\n"
                self.tempvar4 ="Amount" + "\n\n"

                #adding to temp variable for dynamic product added details generation
                for i in range(len(self.prodNumList)):
                    self.tempvar1 = self.tempvar1 + (str(self.prodNumList[i]) + '\n')
                for i in range(len(self.prodUnitsList)):
                    self.tempvar2 = self.tempvar2 + (str(self.prodUnitsList[i]) + '\n')
                for i in range(len(self.amountList)):
                    self.tempvar3 = self.tempvar3 + (str(self.amountList[i]) + '\n')
                for i in range(len(self.prodPriceList)):
                    self.tempvar4 = self.tempvar4 + (str(self.prodPriceList[i]) + '\n')

                #Specifying that the product has been added to cart
                self.value1.set("Product Removed from cart")
                #setting values for the labels defined in main windows for dynamic content generation
                self.prodNum.set(self.tempvar1)
                self.prodUnits.set(self.tempvar2)
                self.amount.set(self.tempvar3)
                self.prodP.set(self.tempvar4)

                #setting entry to blank after the product is added
                self.entry1.delete(0, tkinter.END)
                self.entry2.delete(0, tkinter.END)
            except ValueError:
                tkinter.messagebox.showinfo('Error', 'No Such Product Available in Cart')

    # defined method for the menu About us option
    def aboutUs(self):
        tkinter.messagebox.showinfo('About Company',
                                    'Smart-Mart is a convenient store that is located in Toronto, Canada. This application is developed to use it in its daily business.')

    # defined method for the menu exit option
    def clientExit(self):
        self.main_window.destroy()
        smartmart.SmartMart()

    # defined method for the menu logout option
    def logout(self):
        self.main_window.destroy()
        login.Login()

    #defined to exit whole application
    def clientSystemExit(self):
        self.main_window.destroy()

    def clear_content(self):
        self.prodPriceList.clear()
        self.prodUnitsList.clear()
        self.prodNumList.clear()
        self.amountList.clear()
        self.prodNum.set("")
        self.prodUnits.set("")
        self.amount.set("")
        self.prodP.set("")

#s = IndividualBilling()
#s = IndividualBilling()