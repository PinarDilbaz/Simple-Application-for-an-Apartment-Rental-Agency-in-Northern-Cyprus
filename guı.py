from tkinter import *
from tkinter import messagebox
from client import Client

#call client 
client = Client()
client.start_connection()
class LoginScreen(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Login")
        
        self.frame1 = Frame(self)
        self.frame1.pack(padx=5,pady=5)
       
        self.userNameLabel = Label(self.frame1, text = "Username")
        self.userNameLabel.pack(side = LEFT, padx = 5, pady = 5)

        self.userName = Entry(self.frame1, name="username")
        self.userName.pack(side = LEFT, padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5,pady=5)
        
        self.passwordLabel = Label(self.frame2, text = "Password")
        self.passwordLabel.pack(side = LEFT, padx = 5, pady = 5)

        self.password = Entry(self.frame2, name="password", show="*")
        self.password.pack(side = LEFT, padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5,pady=5)
        
        self.login = Button(self.frame3, text = "Login", command=self.buttonPressed)
        self.login.pack(side = LEFT, padx = 5, pady = 5)



    def buttonPressed(self):

        username = str(self.userName.get())
        password = str(self.password.get())
        message = "login;"+username+";"+password
        message = client.send_message(message)
        result = str(message).split("'")[1]
    
        if result != 'loginfailure':
            result = result.split(";")
            userType = result[2]
            # For employee page
            if userType == 'employee':
                LoginScreen.destroy(self)
                EmployeeScreen(username)
                
            # For manager page   
            elif userType == 'manager':
                LoginScreen.destroy(self)
                ManagerScreen()
        else:
            messagebox.showerror(title = "Message", message = "Invalid credentials")

#for Employee Screen
class EmployeeScreen(Frame):
    def __init__(self,userName):
        Frame.__init__(self)
        self.userName = userName
        self.pack()
        self.master.title("Employee")
        self.master.geometry("270x210")

        #for Apartment code frame
        self.frame1 = Frame(self)
        self.frame1.pack(padx=5,pady=5)
        
        self.apartmentCodeLabel = Label(self.frame1, text = "Apartment Code:")
        self.apartmentCodeLabel.pack(side = LEFT, padx = 5, pady = 5)

        self.apartmentCode = Entry(self.frame1, name="apartmentCode")
        self.apartmentCode.pack(side = LEFT, padx=5, pady=5)

        #for Start Date frame
        self.frame2 = Frame(self)
        self.frame2.pack(padx=5,pady=5)
        
        self.startDateLabel = Label(self.frame2, text = "Start Date:")
        self.startDateLabel.pack(side = LEFT, padx = 5, pady = 5)

        self.startDate = Entry(self.frame2, name="startDate")
        self.startDate.pack(side = LEFT, padx=5, pady=5)

        #for End Date frame
        self.frame3 = Frame(self)
        self.frame3.pack(padx=5,pady=5)
        
        self.endDateLabel = Label(self.frame3, text = "End Date:")
        self.endDateLabel.pack(side = LEFT, padx = 5, pady = 5)

        self.endDate = Entry(self.frame3, name="endDate")
        self.endDate.pack(side = LEFT, padx=5, pady=5)

        #for Customer Name frame
        self.frame4 = Frame(self)
        self.frame4.pack(padx=5,pady=5)
        
        self.customerNameLabel = Label(self.frame4, text = "Customer Name:")
        self.customerNameLabel.pack(side = LEFT, padx = 5, pady = 5)

        self.customerName = Entry(self.frame4, name="customerName")
        self.customerName.pack(side = LEFT, padx=5, pady=5)
        
        #for Show Button
        self.show = Button(self.master, text = "Show", command=self.buttonPressed)
        self.show.place(relx=0.5, rely=0.93, anchor=SE)
        
        #for Reserve Button
        self.reserve = Button(self.master, text = "Reserve", command=self.buttonPressed2)
        self.reserve.place(relx=0.72, rely=0.93, anchor=SE)
    

    #If Show Button is pressed
    def buttonPressed(self): 
        apartment_code = str(self.apartmentCode.get())
        start_date = str(self.startDate.get())
        end_date = str(self.endDate.get())
        message = "apartment;"+apartment_code+";"+start_date+";"+end_date
        client.start_connection()
        message = client.send_message(message)

        result = str(message).split("'")[1]
        print(result)
        if result != 'invalidapartmentcode':
            result = result.split(";")
            apartCode = result[0]
            address = result[1]
            city = result[2]
            postCode = result[3]
            size = result[4]
            numberOfBedrooms = result[5]
            avability = result[6]
            messagebox.showinfo(title = "Message", message = "Apartment Code: "+apartCode +"\nAddress: "+address +"\nCity: "+city +"\nPostcode: "+postCode +"\nSize: "+size +"\nThe number of bedrooms: "+numberOfBedrooms +"\nAvalibility: "+avability)
        else:
            messagebox.showerror(title = "Message", message = "Invalid Apartment Code")

    #If Reserve Button is pressed
    def buttonPressed2(self):
        user_name = self.userName
        apartment_code = str(self.apartmentCode.get())
        start_date = str(self.startDate.get())
        end_date = str(self.endDate.get())
        customer = str(self.customerName.get())
        message = "reservation;"+apartment_code+";"+ customer +";"+start_date+";"+end_date+";"+user_name
        message = client.send_message(message)
        result = str(message).split("'")[1]

        if result == 'successfulreservation':
            messagebox.showinfo(title = "Message", message = "Successful Reservation")
        elif result == 'invalidapartmentcode':
            messagebox.showerror(title = "Message", message = "Invalid Apartment Code")
        elif result == 'notavailable':
            messagebox.showerror(title = "Message", message = "Not Available")


#for Manager Screen
class ManagerScreen(Frame):
    def __init__(self):
            Frame.__init__(self)
            self.pack()
            self.master.title("Manager")
            self.master.geometry("370x250")
            #for first radioButton
            self.frame1 = Frame(self)
            self.frame1.pack(padx=5, pady=5)

            self.sizeLabel = Label(self.frame1, text="Select your report:")
            self.sizeLabel.pack(side=TOP, padx=5, pady=5)
            self.selection1 = StringVar()
            self.selection1.set(self.frame1)
            self.report1Selection = Radiobutton(self.frame1, text="Which employee makes the highest number of reservations?", value=1, variable = self.selection1)
            self.report1Selection.pack(side=LEFT, padx=5, pady=5)
            #for second radioButton
            self.frame2 = Frame(self)
            self.frame2.pack(padx=5, pady=5)
            
            self.report2Selection = Radiobutton(self.frame2, text="Which apartment is the most popular", value=2, variable = self.selection1)
            self.report2Selection.pack(side=LEFT, padx=5, pady=5)
            #for third radioButton
            self.frame3 = Frame(self)
            self.frame3.pack(padx=5, pady=5)
           
            self.report3Selection = Radiobutton(self.frame3, text="How many apartments are currently available", value=3, variable = self.selection1)
            self.report3Selection.pack(side=LEFT, padx=5, pady=5)
            #for fourth radioButton
            self.frame4 = Frame(self)
            self.frame4.pack(padx=5, pady=5)
          
            self.report4Selection = Radiobutton(self.frame4, text="How many apartments have not been reserved yet?", value=4, variable = self.selection1)
            self.report4Selection.pack(side=LEFT, padx=5, pady=5)

            #for Request Button
            self.request = Button(self.master, text = "Request", command=self.buttonPressed)
            self.request.place(relx=0.5, rely=0.94, anchor=SE)
            
            #for Close Button
            self.close = Button(self.master, text = "Close", command=self.buttonPressed2)
            self.close.place(relx=0.63, rely=0.94, anchor=SE)

    #If Request Button is pressed
    def buttonPressed(self): 
        selection = self.selection1.get()
        if(selection == '1'):
  
            message = client.send_message('report1')

            result = str(message).split("'")[1]
            result = result.split(';')
            answers = ""
            result.pop(0)
            if(len(result)>1):
                for i in result:
                    answers = answers +", "+i
            else:
                answers = result

            messagebox.showinfo(title = "Report-1", message = answers)

        elif(selection == '2'):

            message = client.send_message('report2')

            result = str(message).split("'")[1]
            result = result.split(';')
            answers = ""
            result.pop(0)
            if(len(result)>1):
                for i in result:
                    answers = answers +", "+i
            else:
                answers = result

            messagebox.showinfo(title = "Report-2", message = answers)
        elif(selection == '3'):

            message = client.send_message('report3')

            result = str(message).split("'")[1]
            result = result.split(';')
            answers = ""
            result.pop(0)
            if(len(result)>1):
                for i in result:
                    answers = answers +", "+i
            else:
                answers = result

            messagebox.showinfo(title = "Report-3", message = answers)
        elif(selection == '4'):
            message = client.send_message('report4')

            result = str(message).split("'")[1]
            result = result.split(';')
            answers = ""
            result.pop(0)
            if(len(result)>1):
                for i in result:
                    answers = answers +", "+i
            else:
                answers = result
            messagebox.showinfo(title = "Report-4", message = answers)
  
    #If Close Button is pressed
    def buttonPressed2(self):
        client.send_message('close')
        client.stop_connection()
        ManagerScreen.destroy(self)

    
if __name__ =="__main__":
    
    window = LoginScreen()
    window.mainloop()

    