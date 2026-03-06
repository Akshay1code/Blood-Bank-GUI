from customtkinter import *
from ui import create_account
from ui import dashboard
from backend import db
from tkinter.messagebox import *
def open_login_page():
    def check_login_credentials():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username == "" and password == "":
            showwarning('Warning','Please fill login details')
            username_entry.configure(border_color="#760707", border_width=2)
            password_entry.configure(border_color="#760707", border_width=2)
        else:
            if db.user_authenticate(username, password):
                showinfo('Success','User Verification Successfully Authenticated')
                app.destroy()
                data=db.fetch_current_user(username)
                dashboard.open_dashboard(data["id"])
            else:
                showerror('Error','Inccorect Login-id and Password')

    app = CTk()
    
    app.title("Blood Bank | Login")
    
    app.resizable(False, False)
    
    # Matching the Landing Page Deep Red
    app.configure(fg_color="#B81313")
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    width, height = 370, 670
    app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")
    # ===================== HEADER SECTION =====================
    # Using PoppinsBold for the high-impact title
    CTkLabel(
        app, 
        text='LOGIN', 
        text_color='#FFFFFF', 
        font=('Poppins Bold', 60)
    ).place(x=30, y=40)

    # ===================== MAIN CARD (White Container) =====================
    # Positioned lower to give the "LOGIN" text breathing room
    card = CTkFrame(
        app, 
        width=360, 
        height=540, 
        corner_radius=25, 
        fg_color="white"
    )
    card.place(relx=0.5, rely=0.5,y=30, anchor="center")

    # ===================== BRANDING & ICON =====================
    # A cleaner emoji icon with PoppinsBold text
    CTkLabel(card, text="🩸", font=("Poppins", 44),text_color='#D22B2B').place(relx=0.5, y=50, anchor="center")
    
    CTkLabel(
        card, 
        text="Blood Bank", 
        font=("Poppins Bold", 24), 
        text_color="#1A1A1A"
    ).place(relx=0.5, y=95, anchor="center")
    
    CTkLabel(
        card, 
        text="Empowering Donors, Saving Lives", 
        font=("Poppins", 13), 
        text_color="#7F8C8D"
    ).place(relx=0.5, y=125, anchor="center")

    # ===================== INPUT FIELDS =====================
    # Username
    CTkLabel(card, text="Username", font=("Poppins SemiBold", 13), text_color="#2C3E50").place(x=30, y=165)
    username_entry = CTkEntry(card, width=280, height=45, corner_radius=12, placeholder_text="Enter your username",fg_color='#F8F9F9', text_color='#000000', border_width=1, border_color="#E0E0E0")
    username_entry.place(x=30, y=190)

    # Password
    CTkLabel(card, text="Password", font=("Poppins SemiBold", 13), text_color="#2C3E50").place(x=30, y=245)
    password_entry = CTkEntry(
        card, width=280, height=45, corner_radius=12, show="*", 
        placeholder_text="••••••••",
        fg_color='#F8F9F9', text_color='#000000', border_width=1, border_color="#E0E0E0"
    )
    password_entry.place(x=30, y=270)

    # Forgot Password (Right Aligned)
    CTkButton(
        card, text="Forgot Password?", fg_color="transparent", hover=False, 
        text_color="#D22B2B", font=("Poppins SemiBold", 11)
    ).place(x=185, y=315)

    # ===================== ACTION BUTTONS =====================
    # Main Login Button
    login_btn = CTkButton(
        card, text="Login", width=280, height=48, corner_radius=12, 
        fg_color="#D22B2B", hover_color="#B22222",
        font=("Poppins SemiBold", 16),command=check_login_credentials
    )
    login_btn.place(x=30, y=360)

    # Divider
    CTkLabel(
        card, text="────────  or  ────────", 
        font=("Poppins", 11), text_color="#BDC3C7"
    ).place(relx=0.5, y=425, anchor="center")

    # Create Account Button (Outline Style)
    signup_btn = CTkButton(
        card, text="Create Account", width=280, height=48, corner_radius=12, 
        fg_color="white", border_width=2, border_color="#D22B2B", 
        text_color="#D22B2B", hover_color="#FFF5F5", 
        font=("Poppins SemiBold", 15),
        command=lambda: [app.destroy(),create_account.open_create_account()]
    )
    signup_btn.place(x=30, y=450)

    # ===================== FOOTER =====================
    CTkLabel(
        card, 
        text="A Secure Community for Life-Savers", 
        font=("Poppins", 10), 
        text_color="#95A5A6"
    ).place(relx=0.5, y=515, anchor="center")

    app.mainloop()

if __name__ == "__main__":
    open_login_page()