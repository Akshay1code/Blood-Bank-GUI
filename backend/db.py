from backend.connection import get_connection 
from tkinter.messagebox import *
import re




con=get_connection()

def user_authenticate(username,password):
    try:    
        cursor=con.cursor(dictionary=True)
        query="select username,pwd from blood_users where username=%s;"
        cursor.execute(query,(username,))
        user_details=cursor.fetchone()
        print(user_details)
        if(user_details["username"]==username and user_details["pwd"]==password):
            return True
        else:
            return False
    except Exception as e:
        showerror("Error",f"{e}")
        return False
    

def check_fields(name,phone,email_id):
    name_patt=r'^[A-Za-z]{2,} [A-Za-z]{2,} [A-Za-z]{2,}$'
    phone_patt='^[6-9]\d{9}$'
    email_patt=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(name_patt,name) and re.match(phone_patt,phone) and re.match(email_patt,email_id) is not None:
        return True
    else:
        return False
#--------------------------------------------------------------------------------------------
def validate_usernamepwd(username,password):
    username_patt=r'^[A-Za-z][A-Za-z0-9_]{4,14}$'
    password_patt=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
    if re.match(username_patt,username) and re.match(password_patt,password) is not None:
        return True
    else:
        return False
#--------------------------------------------------------------------------------------------

def create_account(user_data):
    try:
        cursor=con.cursor()
        query="insert into blood_users (name,phone_no,email_id,age,username,pwd,home_location) values(%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(query,(user_data.get('name'),user_data.get('phone'),user_data.get('email'),user_data.get('age'),user_data.get('username'),user_data.get('password'),user_data.get('home_location')))
        con.commit()
        return True
    except Exception as e:
        showerror("Error",f"{e}\n ....You are not a Valid user....")
        con.rollback()
        return False

def fetch_current_user(username):
    try:
        cursor=con.cursor(dictionary=True)
        query="select * from blood_users where username = %s"
        cursor.execute(query,(username,))
        user_details=cursor.fetchone()
        con.commit()
        return user_details
    except Exception as e:
        showerror("Error",f"{e}\n ....You are not a Valid user....")
        con.rollback()
        return None
    
def fetch_current_userId(id):
    try:
        cursor=con.cursor(dictionary=True)
        query="select * from blood_users where id = %s;"
        cursor.execute(query,(id,))
        user_details=cursor.fetchone()
        con.commit()
        return user_details
    except Exception as e:
        showerror("Error",f"{e}\n ....You are not a Valid user....")
        con.rollback()
        return None

def fetch_all_blood_banks():
    try:
        cursor=con.cursor(dictionary=True)
        query="select * from availability;"
        cursor.execute(query)
        bank_list=cursor.fetchall()
        con.commit()
        return bank_list
    except Exception as e:
        showerror("Error",f"{e}")
        return None

def fetch_bankById(id):
    cursor=con.cursor(dictionary=True)
    query="select blood_bank_name from availability where id=%s;"
    cursor.execute(query,(id,))
    bank_details=cursor.fetchone()
    con.commit()
    return bank_details

def saveToBloodQueue(data):
    try:
        cursor=con.cursor()
        query="insert into blood_queue (user_id,email_id,blood_bank_id,blood_bank_name,destination_hospital,request_type,blood_group,recipient_name,age,urgency,status,description) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(query,(data["userid"],data["email_id"],data["blood_bank_id"],data["blood_bank_name"],data["destination_loc"],data["request_type"],data["blood_group"],data["recipient_name"],data["age"],data["urgency"],"WAITING"," "))
        con.commit()
        con.close()
        return True
    except Exception as e:
        showerror("Error",f"{e}")
        con.rollback()
        return False
    


def count_users_ahead(count_list,id):
    count=0
    for dict in count_list:
        if dict["user_id"] == id:
            return count
        count+=1
def fetch_bloodQueue(id):
    try:
        cursor=con.cursor(dictionary=True)
        query="select * from blood_queue where status <> %s order by created_at ;"
        cursor.execute(query,("DELIVERED",))
        count_list=cursor.fetchall()
        count=count_users_ahead(count_list,id)
        con.commit()
        query="select * from blood_queue where user_id = %s and status <> %s order by created_at DESC;"
        cursor.execute(query,(id,"DELIVERED"))
        data=cursor.fetchone()
        con.commit()
        return data,count

    except Exception as e:
        print(e)
