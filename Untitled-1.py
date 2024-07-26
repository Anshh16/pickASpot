import pymysql
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from tkinter import *
from tkinter import ttk
from datetime import *
from PIL import Image, ImageTk
import qrcode
import os
import cv2

win=CTk()
win.geometry("710x485")
win.title("pickAspot: Automared Parking Experience")
img=ImageTk.PhotoImage(Image.open("D:\\pickAspot\\pict2.jpg"))
imge=ImageTk.PhotoImage(Image.open("D:\\pickAspot\\logo1.png"))
lbl1=CTkLabel(win,text="",width=480,image=img)
lbl1.place(x=0,y=0)
lbl3=CTkLabel(win,text="",image=imge)
lbl3.place(x=0,y=40)
textimg=ImageTk.PhotoImage(Image.open("D:\\pickAspot\\choicetext1.png"))
lbl4=CTkLabel(win,text="",image=textimg,fg_color = ('#88909b'),text_color=('black'))
lbl4.place(x=450,y=150)


def parking_fr():
    global parkfr
    parkfr=CTk()
    parkfr.title("Parking Dashboard")
    parkfr.geometry("353x330")
    lbl8=CTkLabel(parkfr,text="    Parking Dashboard    ",bg_color="#b97c0c",height=65,font=("Arial Bold", 32),text_color='black')
    lbl8.place(x=0,y=0)
    lbl9=CTkLabel(parkfr,text ='', height=225, width=320,fg_color = ('#b97c0c'), text_color = ('black'),corner_radius = 10)
    lbl9.place(x=16,y=83)
    ent3=CTkEntry(parkfr,placeholder_text="Enter Name",border_width=0,height=30,width=294,corner_radius=20,bg_color="#b97c0c",fg_color='black')
    ent3.place(x=30,y=100)
    ent4=CTkEntry(parkfr,placeholder_text="Enter Phone Number",border_width=0,height=30,width=294,corner_radius=20,bg_color="#b97c0c",fg_color='black')
    ent4.place(x=30,y=140)
    ent5=CTkEntry(parkfr,placeholder_text="Enter Vehicle Number",border_width=0,height=30,width=294,corner_radius=20,bg_color="#b97c0c",fg_color='black')
    ent5.place(x=30,y=180)
    lbl10=CTkLabel(parkfr,text="SLOT : ",bg_color="#b97c0c",font=("Arial Bold", 14),text_color='black')
    lbl10.place(x=37,y=221)
    que="select * from slots"
    c.execute(que)
    a=c.fetchall()
    d = [item for i in a for item in i]
    combobox = CTkComboBox(parkfr, values=d,bg_color="#b97c0c",width=235,corner_radius=20,fg_color='black')
    combobox.place(x=87,y=220)
    btn7=CTkButton(parkfr,text="SUBMIT",hover_color = 'green',bg_color="#b97c0c",fg_color="black", command=lambda:[submit(ent3,ent4,ent5,combobox,parkfr)])
    btn7.place(x=30,y=260)
    btn8=CTkButton(parkfr,text="CANCEL",bg_color="#b97c0c",fg_color="black",hover_color="dark red",command=parkfr.destroy)
    btn8.place(x=180,y=260)
    parkfr.resizable(0,0)
    parkfr.mainloop()


def submit(nm,phn,vh,cm,parkfr):
    name=nm.get()
    phno=phn.get()
    vehno=vh.get().upper()
    combx=cm.get()
    now=datetime.now()
    global entime
    entime=now.strftime("%H:%M")
    que1="insert into entry values('{}',{},'{}','{}','{}')".format(name,phno,vehno,entime,combx)
    que2="delete from slots where slot='{}'".format(combx)
    c.execute(que1)
    c.execute(que2)
    c.execute("commit") 
    CTkMessagebox(title="PARKED",message="Vehicle Parked Successfully!!",icon="D:\\pickAspot\\tick.ico")
    parkfr.destroy()


def picking_fr():
    global pickfr
    pickfr=CTk()
    pickfr.title("Picking Dashboard")
    pickfr.geometry("388x270")
    lbl11=CTkLabel(pickfr,text="      Picking Dashboard      ",bg_color="#b97c0c",height=65,font=("Arial Bold", 32),text_color='black')
    lbl11.place(x=0,y=0)
    lbl13=CTkLabel(pickfr,text = '', height=165, width=360,fg_color = ('#b97c0c'), text_color = ('black'),corner_radius = 10)
    lbl13.place(x=16,y=83)
    lbl12=CTkLabel(pickfr,text="Please select your VEHICLE NO. and press SUBMIT : ",bg_color="#b97c0c",text_color='black',font=("Arial Bold", 14))
    lbl12.place(x=19,y=90)
    que4="select VehicleNo from entry"
    c.execute(que4)
    y=c.fetchall()
    e = [item for i in y for item in i]
    combobox1 = CTkComboBox(pickfr, values=e,bg_color="#b97c0c",fg_color='black',width=245,corner_radius=20)
    combobox1.place(x=70,y=130)
    btn10=CTkButton(pickfr,text="SUBMIT",hover_color = 'green',bg_color="#b97c0c",fg_color="black",command=lambda:[picsub(combobox1,pickfr)])
    btn10.place(x=42,y=200)
    btn11=CTkButton(pickfr,text="CANCEL",bg_color="#b97c0c",fg_color="black",hover_color="dark red",command=pickfr.destroy)
    btn11.place(x=195,y=200)
    pickfr.resizable(0,0)
    pickfr.mainloop()


def picsub(com,pickfr):
    nom=com.get()
    que5="select Slot from entry where VehicleNo='{}'".format(nom)
    c.execute(que5)
    u=c.fetchone()
    stt=""
    for item in u:
        stt=stt+item
    que6="select EntryTime from entry where VehicleNo='{}'".format(nom)
    c.execute(que6)
    o=c.fetchone()
    sty=""
    for itm in o:
        sty=sty+itm
    que8="delete from entry where VehicleNo='{}'".format(nom)
    c.execute(que8)
    que9="insert into slots values('{}')".format(stt)
    c.execute(que9)
    c.execute("commit")
    now=datetime.now()
    global exttime
    exttime=now.strftime("%H:%M")
    entrtime=datetime.strptime(sty,"%H:%M")
    ettime=datetime.strptime(exttime,"%H:%M")
    diff=ettime-entrtime
    seconds = diff.total_seconds() 
    hour = seconds / (60 * 60) 
    hour_f= "{:.2f}".format(hour) 
    houri=float(hour_f)
    hourf=35.0
    pickfr.destroy()
    global resfr
    resfr=CTk()
    resfr.title("Payment Section")
    lblpay=CTkLabel(resfr,text="",font=("Arial Bold", 20))
    lblpay.place(x=15,y=15)
    if houri<=1:
        lblpay.configure(text=f'Your was parked for less than \nan hour, therefore you have to\npay minimum fare amount of ₹{hourf}.\n\nBy scanning the QR code in\n the right you can perform\n the transaction.\nThankyou!')
    else:
        hourf=hourf*houri
        lblpay.configure(text=f'Your vehicle was parked for\n{hour_f} hours, therefore your\nbilling amount is ₹{hourf}.\n\nBy scanning the QR code in\n the right you can perform the\ntransaction.\nThankyou!')
    upi_id="7351415200@airtel"
    googlepay_url=f'upi://pay?pa={upi_id}&pn=Recipient%20Name&am={hourf}&tn=Paid ₹{hourf} to the parking station.'
    googlepay_qr=qrcode.make(googlepay_url)
    googlepay_qr.save(f'C:\\Users\\anshv\\OneDrive\\Desktop\\gp1.png')
    qrimg=cv2.imread(f'C:\\Users\\anshv\\OneDrive\\Desktop\\gp1.png')
    cv2.imshow("Payment",qrimg)
    os.remove(f'C:\\Users\\anshv\\OneDrive\\Desktop\\gp1.png')
    resfr.geometry("362x300+40+342")
    resfr.resizable(0,0)
    btn119=CTkButton(resfr,text="PAID",hover_color = 'green',bg_color="#242424",fg_color="black", command=lambda:(resfr.destroy(),cv2.destroyAllWindows()))
    btn119.place(x=115,y=215)
    resfr.mainloop()


parklbl=ImageTk.PhotoImage(Image.open("D:\\pickAspot\\parkbtn.png"))    
btn1 = CTkButton(win,text="",image=parklbl,width=0,height=0,border_width=0,bg_color='black',fg_color='black',text_color='black',corner_radius=30,command=parking_fr)
btn1.place(x=450,y=195)
picklbl=ImageTk.PhotoImage(Image.open("D:\\pickAspot\\pickbtn.png"))
btn2 = CTkButton(win,text="",image=picklbl,width=0,height=0,border_width=0,bg_color='black',fg_color='black',text_color = 'black',corner_radius=30,command=picking_fr)
btn2.place(x=450,y=290)


def customer_support():
    CTkMessagebox(title="Customer Support", message="For any queries or support you can contact to: \n7351415200\n0121-255693",icon="D:\\pickAspot\\supp.ico")


def about_us():
    CTkMessagebox(title="About Us",message="This app is designed and developed by Ansh as a project in DBMS.",icon="D:\\pickAspot\\dev.ico")
    

def manag_log():
    global Maglog
    Maglog=CTk()
    Maglog.geometry("500x250")
    Maglog.title("Management Login")
    lbl6=CTkLabel(Maglog,text = '', height=100, width=320,fg_color = "#b97c0c", text_color ='black',corner_radius = 10)
    lbl6.place(x=90,y=75)
    lbl5=CTkLabel(Maglog,text="             Management Login             ",bg_color="#b97c0c",height=55,font=("Arial Bold", 32),text_color='black')
    lbl5.place(x=0,y=0)
    ent1=CTkEntry(Maglog,placeholder_text="Enter Username",border_width=0,height=30,width=300,corner_radius=20,bg_color="#b97c0c",fg_color='black')
    ent1.place(x=100,y=87)
    ent2=CTkEntry(Maglog,placeholder_text="Enter Password",show="*",border_width=0,height=30,width=300,corner_radius=20,bg_color="#b97c0c",fg_color='black')
    ent2.place(x=100,y=133)
    btn3=CTkButton(Maglog,text="Login",hover_color = 'green',bg_color="#242525",fg_color="black",command=lambda:[mag_ent(ent1,ent2,Maglog)])
    btn3.place(x=100,y=195)
    btn4=CTkButton(Maglog,text="Exit",bg_color="#242525",fg_color="black",hover_color="dark red",command=Maglog.destroy)
    btn4.place(x=260,y=195)
    Maglog.resizable(0,0)
    Maglog.mainloop()


def curparfr():
    global Pasfr
    Pasfr=Tk()
    Pasfr.geometry("1050x360")
    Pasfr.title("Current Parking Status")
    lbl18=Label(Pasfr,text="Current Parking Entries",bg="#b97c0c",fg="black",height=1,width=35,font=("Arial Bold", 36))
    lbl18.place(x=0,y=0)
    que13="select * from entry"
    tree=ttk.Treeview(Pasfr,column=("c1", "c2","c3","c4","c5"), show='headings', height=11)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Owner Name")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Phone Number")
    tree.column("# 3",anchor=CENTER)
    tree.heading("# 3", text="Vehicle Number")
    tree.column("# 4",anchor=CENTER)
    tree.heading("# 4", text="Entry Time")
    tree.column("# 5",anchor=CENTER)
    tree.heading("# 5", text="Slot")
    tree.place(x=23,y=80)
    c.execute(que13)
    ent=c.fetchall()
    d = [item for i in ent for item in i]
    tree.insert('', 'end', values=(d[0],d[1],d[2],d[3],d[4]))
    try:
        tree.insert('', 'end', values=(d[5],d[6],d[7],d[8],d[9]))
        tree.insert('', 'end', values=(d[10],d[11],d[12],d[13],d[14]))
        tree.insert('', 'end', values=(d[15],d[16],d[17],d[18],d[19]))
        tree.insert('', 'end', values=(d[20],d[21],d[22],d[23],d[24]))
        tree.insert('', 'end', values=(d[25],d[26],d[27],d[28],d[28]))
        tree.insert('', 'end', values=(d[29],d[30],d[31],d[32],d[33]))
        tree.insert('', 'end', values=(d[34],d[35],d[36],d[37],d[38]))
        tree.insert('', 'end', values=(d[39],d[40],d[41],d[42],d[43]))
        tree.insert('', 'end', values=(d[44],d[45],d[46],d[47],d[48]))
    except:
        pass
    Pasfr.resizable(False,False)
    Pasfr.mainloop()


def avalfr():
    global Avlfr
    Avlfr=Tk()
    Avlfr.geometry("380x360")
    Avlfr.title("Available Slots")
    lbl19=Label(Avlfr,text="Available Slots",bg="#b97c0c",fg="black",height=1,width=13,font=("Arial Bold", 36))
    lbl19.place(x=0,y=0)
    que14="select * from slots"
    tree=ttk.Treeview(Avlfr,column=("c1"), show='headings', height=11)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Available Slots")
    tree.place(x=85,y=80)
    c.execute(que14)
    et=c.fetchall()
    d = [item for i in et for item in i]
    tree.insert('', 'end', values=(d[0]))
    try:
        tree.insert('', 'end', values=(d[1]))
        tree.insert('', 'end', values=(d[2]))
        tree.insert('', 'end', values=(d[3]))
        tree.insert('', 'end', values=(d[4]))
        tree.insert('', 'end', values=(d[5]))
        tree.insert('', 'end', values=(d[6]))
        tree.insert('', 'end', values=(d[7]))
        tree.insert('', 'end', values=(d[8]))
        tree.insert('', 'end', values=(d[9]))
        tree.insert('', 'end', values=(d[10]))
    except:
        pass
    Avlfr.resizable(False,False)
    Avlfr.mainloop()


def mag_ent(et1,et2,Maglog):
    user=et1.get()
    pas=et2.get()
    if user=='admin' and pas=='admin':
        Maglog.destroy()
        global mag_fr
        mag_fr=CTk()
        mag_fr.title("Management Dashboard")
        mag_fr.geometry("500x250")
        lbl7=CTkLabel(mag_fr, text = '', height=180, width=390,fg_color = ('#b97c0c'), text_color = ('black'),corner_radius = 10)
        lbl7.place(x=56,y=34)
        btn3=CTkButton(mag_fr,text="Show available slots",height=35,width=170,corner_radius=20,bg_color='#b97c0c',fg_color='black',hover_color='green',command=avalfr)
        btn3.place(x=80,y=67)
        btn4=CTkButton(mag_fr,text="Show current parking",height=35,width=170,corner_radius=20,bg_color='#b97c0c',fg_color='black',hover_color='green',command=curparfr)
        btn4.place(x=260,y=67)
        btn5=CTkButton(mag_fr,text="Edit entry",height=35,width=170,corner_radius=20,bg_color='#b97c0c',fg_color='black',hover_color='green')
        btn5.place(x=80,y=148)
        btn6=CTkButton(mag_fr,text="Exit",height=35,width=170,corner_radius=20,bg_color='#b97c0c',fg_color='black',hover_color='red',command=mag_fr.destroy)
        btn6.place(x=260,y=148)
        mag_fr.resizable(0,0)
        mag_fr.mainloop()
    else:
        CTkMessagebox(title="Information",message="Invalid Username or Password!")

con=pymysql.connect(user="root",password="",host="localhost",database="pickaspot")
c=con.cursor()     
men=Menu(win)
men.add_command(label="Management Login",command=manag_log)
men.add_separator()
men.add_command(label="Customer Support",command=customer_support)
men.add_separator()
men.add_command(label="About Us",command=about_us)
men.add_separator()
men.add_command(label="Quit",command=win.destroy)
win.config(menu=men)
win.resizable(0,0)
win.mainloop()