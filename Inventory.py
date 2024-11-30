import pandas as pd
from tabulate import tabulate
import mysql.connector as sqlt
con=sqlt.connect(host="localhost",user="root",password="MPM_772005",database="inventory")
cursor=con.cursor()
def add_item():
    ino=int(input("enter the item number"))
    iname=input("ënter the item name")
    srate=float(input("enter the sales rate"))
    prate=float(input("enter the purchase rate"))
    qoh=int(input("enter the qty on hand"))
    q="insert into item values({},'{}',{},{},{});".format(ino,iname,prate,srate,qoh)
    cursor.execute(q)
    con.commit()
    print("item added")
def edit_item():
    ino=int(input("enter item number"))
    q="select*from item where ino={};"
    cursor.execute(q)
    if cursor.fetchone():
        iname=input("enter the item name")
        cursor.execute("update item set iname= '{}' wehre ino={};".format(iname,ino))
        con.commit()
        print("iteam edited")
    else:
        print("item not found")     
def fix_rate():
    ino=int(input("enter item number"))
    q="select*from item where ino={};".format(ino)
    cursor.execute(q)
    if cursor.fetchone():
        prate=int(input("enter new purchase rate"))
        srate=int(input("enter new sales rate"))
        cursor.execute("update item set srate= {},prate={} wehre ino={};".format(srate,prate))
        con.commit()
        print("new rate applied")
    else:
        print("item not found") 
def search_item():
    ino=int(input("enter item number"))
    q="select*from item where ino={};".format(ino)
    cursor.execute(q)
    if cursor.fetchone():
        df=pd.read_sql(q,con)
        print(tabulate(df,header="keys",tablefmt="psql",showindex=False))
def delete_item():
    ino=int(input("enter item number"))      
    q="select*from item where ino={};".format(ino)
    cursor.execute(q)
    if cursor.fetchone():
        cursor.execute("delete from item where ino={};".format(ino))  
        con.cummit()
        print("item deleted")
    else:
        print("item not found") 
def add_customer():
    cid=int(input("enter customer ID"))
    cname=input("enter customer name")
    cadd=input("enter address")
    mobile=int(input("enter mobile"))
    q="insert into customer values({},'{}','{}',{});".format(cid,cname,cadd,mobile)
    cursor.execute(q)
    con.commit()
    print("customer added")
def edit_customer():
    cid=int(input("enter customer ID"))
    q="select*from customer where cid={};".format(cid)
    if cursor.fetchone():
        cadd=input("enter customer address")
        cursor.execute("update customer set cadd='{}'wehre cid={};".format(cadd,cid))
        con.commit()
        print("customer edited")
    else:
        print("customer not found")
def search_customer():
    cname=input("enter customer name")
    q="select*from customer where cname like'%{}%';".format(cname)
    cursor.execute(q)
    if cursor.fetchall():
        df=pd.read_sql(q,con)
        print(tabulate(df,headers='keys',tablefmt='psql',showindex=False))
    else:
        print("customer not found")  
def delete_customer():
    cid=int(input("enter customer ID"))
    q="select*from customer where cid={};".format(cid)
    if cursor.fetchone():
        cursor.execute("delete from customer wehre cid={};".format(cid))
        con.commit()
        print("customer deleted")
    else:
        print("customer not found")
def add_supplier():
    sid=int(input("enter supplier ID"))
    sname=input("enter supplier name")
    sadd=input("enter address")
    mobile=int(input("enter mobile"))
    q="insert into supplier values({},'{}','{}',{});".format(sid,sname,sadd,mobile)
    cursor.execute(q)
    con.commit()
    print("supplier added") 
def edit_supplier():
    sid=int(input("enter supplier ID"))
    q="select*from supplier where sid={};".format(sid)
    cursor.execute(q)
    if cursor.fetchone():
        sadd=input("enter supplier address")
        cursor.execute("update supplier set sadd='{}'wehre sid={};".format(sadd,sid))
        con.commit()
        print("supplier edited")
    else:
        print("supplier not found")
def search_supplier():
    sid=int(input("enter supplier name"))
    q="select*from supplier where sid={};".format(sid)
    cursor.execute(q)
    if cursor.fetchone():
        df=pd.read_sql(q,con)
        print(tabulate(df,headers='keys',tablefmt='psql',showindex=False))
    else:
        print("supplier not found")  
def delete_supplier():
    sid=int(input("enter supplier ID"))
    q="select*from supplier where sid={};".format(sid)
    if cursor.fetchone():
        cursor.execute("delete from supplier wehre sid={};".format(sid))
        con.commit()
        print("supplier deleted")
    else:
        print("supplier not found")
def purchase():
    pid=0
    total=0
    grand=0
    l=[]
    ch='y'
    q="select max(pid) from pmaster" 
    cursor.execute(q)
    r=cursor.fetchone()[0]
    if r:
        pid=r+1
    else:
        pid=1
    pdate=input("enter purchase date")
    sid=int(input("enter supplier ID"))
    cursor.execute("select * from supplier where sid={};,format(sid)")
    if cursor.fetchone():
        print("item deatils")    
        df=pd.read_sql("select*from item;",con)   
        print(tabulate(df,headers='keys',tablefmt='psql',showindex=False))
        ino=int(int("enter item number")) 
        while(ch=='y'):   
            cursor.execute("select * from item where ino={};",format(ino))
            r1=cursor.fetchone()
            if r:
                qty=int(input("enter qty"))
                rate = r1[2]
                total=qty*rate
                grand=grand+total
                t=(pid,ino,qty,rate,total)
                l.append(t)
            else:
                print("item not found")
            ch=input("do you want to enter more item in bucket y/n")   
            q1=("insert into pmaster values({},{},{},'{}','{}');",format(pid,pdate,sid,grand))
            cursor.execute(q1)
            con.commit()
            q2=("insert into pdetail values(%s,%s,%s,%s,%s);")
            cursor.executemany(q2,l)
            con.commit()
    else:
        print("supplier not found")        
def sale():
    saleid=0
    total=0
    grand=0
    l=[]
    ch='y'
    q="select max(saleid) from smaster" 
    cursor.execute(q)
    r=cursor.fetchone()[0]
    if r:
        saleid=r+1
    else:
        saleid=1
    sdate=input("enter sale date")
    sid=int(input("enter supplier ID"))
    cursor.execute("select * from supplier where sid={};,format(sid)")
    if cursor.fetchone():
        print("item deatils")    
        df=pd.read_sql("select*from item;",con)   
        print(tabulate(df,headers='keys',tablefmt='psql',showindex=False))
        ino=int(int("enter item number")) 
        while(ch=='y'):   
            cursor.execute("select * from item where ino={};",format(ino))
            r1=cursor.fetchone()
            if r:
                qty=int(input("enter qty"))
                rate = r1[2]
                total=qty*rate
                grand=grand+total
                t=(saleid,ino,qty,rate,total)
                l.append(t)
            else:
                print("item not found")
            ch=input("do you want to enter more item in bucket y/n")   
            q1=("insert into smaster values({},{},{},'{}','{}');",format(saleid,sdate,sid,grand))
            cursor.execute(q1)
            con.commit()
            q2=("insert into pdetail values(%s,%s,%s,%s,%s);")
            cursor.executemany(q2,l)
            con.commit()
    else:
        print("supplier not found")  
def show_item():
    df=pd.read_sql("select*from item",con)   
    print(tabulate(df,header="keys",tablefmt="psql",showindex=False))  
def show_customer():
    df=pd.read_sql("select*from customer",con)   
    print(tabulate(df,header="keys",tablefmt="psql",showindex=False))  
def show_supplier():
    df=pd.read_sql("select*from supplier",con)   
    print(tabulate(df,header="keys",tablefmt="psql",showindex=False))   
def show_sale():
    bdate=input("enter beginning date")
    edate=input("enter end date")
    df=pd.read_sql("select*from smaster wehre sdate between '{}', and '{}';".format(bdate,edate),con)   
    print(tabulate(df,header="keys",tablefmt="psql",showindex=False))   
def show_purchase():
    bdate=input("enter beginning date")
    edate=input("enter end date")
    df=pd.read_sql("select*from pmaster wehre pdate between '{}', and '{}';".format(bdate,edate),con)   
    print(tabulate(df,header="keys",tablefmt="psql",showindex=False))                                 
while(True):
    print("\nenter your choice\n1.items\n2.customer\n3.supplier\n4.transaction\n5.delete item\n6.exit")
    ch=int (input())
    if ch==1:
        while(True):
            print("\nenter your choice\n1.add item\n2.edit item\n3.fix rate\n4.search item\n5.delete item\n6.exit")
            ch=int(input())
            if ch==1:
                add_item()
            elif ch==2:
                edit_item()
            elif ch==3:
                fix_rate
            elif ch==4:
                search_item
            elif ch==5:
                delete_item
            elif ch==6:
                break
    if ch==2:
        while(True):
            print("\nenter your choice\n1.add customer\n2.edit customer\n3.search customer\n4.delete customer\n5.exit")
            ch=int(input())
            if ch==1:
                add_customer()
            elif ch==2:
                edit_customer()
            elif ch==3:
                search_customer()
            elif ch==4:
                delete_customer()
            elif ch==5:
                break
    if ch==3:
        while(True):
             print("\nenter your choice\n1.add supplier\n2.edit supplier\n3.search supplier\n4.delete supplier\n5.exit")
             ch=int(input())
             if ch==1:
                add_supplier()
             elif ch==2:
                edit_supplier()
             elif ch==3:
                search_item()
             elif ch==4:
                delete_supplier
             elif ch==5:
                break
    if ch==4:
        while(True):
             print("\nenter your choice\n1.sales\n2.purchase\n3.exit")
             ch=int(input())
             if ch==1:
                sale()
             elif ch==2:
                purchase()
             elif ch==3:
                 break
    if ch==5:
        while(True):
             print("\nenter your choice\n1.item details\n2.customer details\n3.supplier details\n4.sales report\n5.purchase report\n6.exit")

             ch=int(input())
             if ch==1:
                show_item()
             elif ch==2:
                show_customer()
             elif ch==3:
                show_supplier()
             elif ch==4:
                show_sale()
             elif ch==5:
                show_purchase
             elif ch==6:
                break
    elif ch==6:
        print("Have a good day")
        break
