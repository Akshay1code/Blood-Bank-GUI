from customtkinter import *
import os
import webview
from geopy.geocoders import Nominatim
from backend.db import validate_usernamepwd, create_account, check_fields
from ui import dashboard
from tkinter.messagebox import *
from backend import otp
# ================= SETTINGS & GLOBALS =================
set_appearance_mode("light")
geolocator = Nominatim(user_agent="location_picker_app")
user_data = {}

def reverse_geocode(lat, lng):
    try:
        location = geolocator.reverse((lat, lng), language="en")
        if location:
            return location.address
        return None
    except Exception as e:
        print("Geocode error:", e)
        return None
    
# ================= APP SETUP =================
def open_create_account():
    app = CTk()
    app.title("Donor Registration Portal")
    app.resizable(False, False)
    app.configure(fg_color="#F8F9FA")

    width, height = 370, 670
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    padx = (screen_width - width) // 2
    pady = (screen_height - height) // 2
    app.geometry(f"{width}x{height}+{padx}+{pady}")

    # ================= LOGIC FUNCTIONS =================

    def finalize_account(win):
        if(create_account(user_data)):
            win.destroy()
            app.destroy()
            dashboard.open_dashboard(user_data.get('username'))
        else:
            showerror('Error','Database error occurred!')

    def show_location_confirmed(address):
        confirm_win = CTkToplevel(app)
        confirm_win.title("Verified")
        confirm_win.geometry(f"{width}x{height}+{padx}+{pady}")
        confirm_win.configure(fg_color="#D22B2B")

        success_frame = CTkFrame(confirm_win, fg_color="#FFFFFF", corner_radius=180, width=450, height=450)
        success_frame.place(x=-40, y=-150)

        CTkLabel(success_frame, text="✓", font=("Poppins Bold", 80), text_color="#27AE60").place(relx=0.5, rely=0.68, anchor="center")
        CTkLabel(success_frame, text="PROFILE VERIFIED", font=("Poppins Bold", 20), text_color="#1A1A1A").place(relx=0.5, rely=0.82, anchor="center")

        CTkLabel(confirm_win, text="Identity & Location\nSuccessfully Validated", font=("Poppins Bold", 22), 
                text_color="#FFFFFF", justify="center").place(relx=0.5, rely=0.58, anchor="center")

        addr_label = CTkLabel(confirm_win, text=f"Primary Location:\n{address}", font=("Poppins", 13), 
                            text_color="#FFDADA", wraplength=300, justify="center")
        addr_label.place(relx=0.5, rely=0.72, anchor="center")
        user_data["home_location"] = address

        finish_btn = CTkButton(confirm_win, text="Finish Registration", height=52, width=250, corner_radius=26,
                            fg_color="#FFFFFF", text_color="#D22B2B", hover_color="#F2F2F2", 
                            font=("Poppins SemiBold", 16), command=lambda: finalize_account(confirm_win))
        finish_btn.place(relx=0.5, rely=0.91, anchor="center")

    def open_map_window():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(BASE_DIR, "map.html")
        
        class API:
            def confirm_location(self, lat, lng):
                addr = reverse_geocode(lat, lng)
                if webview.windows: webview.windows[0].destroy()
                app.after(100, lambda: show_location_confirmed(addr))

        webview.create_window("Select Home Location", url=map_path, width=370, height=670, js_api=API())
        webview.start()

    def open_location_info():
        info_win = CTkToplevel(app)
        info_win.geometry(f"{width}x{height}+{padx}+{pady}")
        info_win.configure(fg_color="#FFFFFF")

        CTkLabel(info_win, text="Location Required", font=("Poppins Bold", 24), text_color="#D22B2B").pack(pady=(60, 20))
        guide_text = ("In medical emergencies, every second matters. Sharing your home location helps us route blood units faster.")
        
        CTkLabel(info_win, text=guide_text, font=("Poppins", 14), text_color="#475569", wraplength=300, justify="center").pack(padx=30, pady=10)

        btn = CTkButton(info_win, text="Continue to Map", height=55, corner_radius=15,
                        fg_color="#D22B2B", hover_color="#A31D1D", font=("Poppins SemiBold", 16),
                        command=lambda: [info_win.destroy(), open_map_window()])
        btn.pack(side="bottom", fill="x", padx=35, pady=40)



    def open_otp_window(name,email):
    # ================= APP SETUP =================
        def verify(otp_entry):
            if otp.verify_otp(otp_entry,email):
                app.withdraw()
                open_location_info()
            else:
                showerror("Error","Wrong OTP entered")
                return
        app = CTk()
        app.title("OTP Verification")
        app.resizable(False, False)
        app.configure(fg_color="#F8F9FA")

        width, height = 370, 670
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        padx = (screen_width - width) // 2
        pady = (screen_height - height) // 2
        app.geometry(f"{width}x{height}+{padx}+{pady}")

        # --- VALIDATION LOGIC ---
        # Limits input to exactly 6 digits and only numbers
        def validate_otp(P):
            if P == "": return True
            if str.isdigit(P) and len(P) <= 6:
                return True
            return False

        vcmd = (app.register(validate_otp), '%P')

        # ================= UI COMPONENTS =================

        # 1. Top Red Curved Header
        header_curve = CTkFrame(app, fg_color="#D22B2B", width=500, height=350, corner_radius=250)
        header_curve.place(x=-65, y=-180)

        CTkLabel(app, text="Verification", font=("Poppins Bold", 26), 
                text_color="white", fg_color="#D22B2B").place(x=30, y=50)
        CTkLabel(app, text="Enter the code sent to your mobile", font=("Poppins", 12), 
                text_color="#FFDADA", fg_color="#D22B2B", wraplength=300).place(x=19, y=85)

        # 2. Central Card
        card = CTkFrame(app, fg_color="#FFFFFF", corner_radius=30, border_width=1, border_color="#EAEAEA")
        card.place(relx=0.5, rely=0.54, anchor="center", relwidth=0.92, relheight=0.50)

        CTkLabel(card, text="Secure Access", font=("Poppins Bold", 20), text_color="#1A1A1A").pack(pady=(35, 5))
        CTkLabel(card, text="Please enter the 6-digit verification code", 
                font=("Poppins", 12), text_color="#64748B", justify="center").pack()

        # 3. Single Beautiful OTP Entry
        # Using a larger tracking/spacing effect via font size and width
        otp_entry = CTkEntry(card, width=240, height=65, corner_radius=15, fg_color="#F1F3F5", border_width=2, border_color="#F1F3F5",placeholder_text="• • • • • •",placeholder_text_color="#94A3B8",justify="center",font=("Poppins SemiBold", 32, "bold"),text_color="#D22B2B",validate="key", validatecommand=vcmd)
        otp_entry.pack(pady=20)
        # Helper Instruction Text
        CTkLabel(card, 
                text="Check your messages or spam folder.\nCode valid for 5 minutes.",
                font=("Poppins", 11), text_color="#94A3B8", justify="center",wraplength=350
        ).pack(pady=(0,2))
        # 4. Static Resend Section
        resend_label = CTkLabel(card, text="Didn't receive code?", font=("Poppins", 12), text_color="#94A3B8")
        resend_label.pack(pady=(5, 0))
        
        resend_btn = CTkButton(card, text="Resend OTP", font=("Poppins Bold", 13), text_color="#D22B2B", fg_color="transparent",hover_color="#ECECEC", width=40,corner_radius=10,command=lambda:otp.delete_current_user(name,email))
        resend_btn.pack()


        otp.generate_otp(name,email)

        # 5. Bottom Action Button
        btn_verify = CTkButton(app, text="Verify & Proceed →", height=55, corner_radius=15,
                            fg_color="#D22B2B", hover_color="#B22222", 
                            font=("Poppins SemiBold", 16), 
                            command=lambda:verify(otp_entry.get()))
        btn_verify.place(relx=0.5, rely=0.88, anchor="center", relwidth=0.85)

        app.mainloop()




    def save_and_continue():
        # Validation for all fields including new ones
        if any(v.strip() == "" for v in [username_entry.get(), password_entry.get(), name_entry.get(), phone_entry.get(), email_entry.get()]):
            showwarning('Request', "Fill all the details")
            return
        
        # Note: check_fields still called to maintain your backend logic structure
        if not check_fields(name_entry.get().strip(),phone_entry.get().strip(),email_entry.get().strip()):
            showwarning('Warning',"Check phone_no.,email and name correctly")
        if validate_usernamepwd(username_entry.get().strip(), password_entry.get().strip()):
            user_data.update({
                "name": name_entry.get(),
                "phone": f"{code_entry.get()}-{phone_entry.get()}",
                "email": email_entry.get(),
                "age": int(age_menu.get()),
                "username": username_entry.get(),
                "password": password_entry.get()
            })
            app.withdraw()
            open_otp_window(user_data['name'],user_data['email'])
        else:
            showwarning('Fail', 'Username and Password fields format doesnt meet guidelines')
            return

    # ================= UI COMPONENTS =================
    header_curve = CTkFrame(app, fg_color="#D22B2B", width=500, height=380, corner_radius=250)
    header_curve.place(x=-65, y=-200)

    CTkLabel(app, text="Create Account", font=("Poppins Bold", 26), text_color="white", fg_color="#D22B2B").place(x=30, y=40)
    CTkLabel(app, text="Step 1: Personal Details", font=("Poppins", 12), text_color="#FFDADA", fg_color="#D22B2B").place(x=30, y=75)

    card = CTkFrame(app, fg_color="#FFFFFF", corner_radius=30, border_width=1, border_color="#EAEAEA")
    card.place(relx=0.5, rely=0.58, anchor="center", relwidth=0.92, relheight=0.75)

    form = CTkScrollableFrame(card, fg_color="#FFFFFF", scrollbar_button_color="#FFFFFF")
    form.pack(fill="both", expand=True, padx=10, pady=20)

    def add_styled_field(parent, label, placeholder, icon, is_pass=False, is_menu=False, use_grid=False):
        lbl_frame = CTkFrame(parent, fg_color="transparent")
        lbl_frame.pack(fill="x", padx=15, pady=(15, 2))
        CTkLabel(lbl_frame, text=icon, font=("Poppins", 14)).pack(side="left")
        CTkLabel(lbl_frame, text=label, font=("Poppins SemiBold", 13), text_color="#2D3436").pack(side="left", padx=8)
        
        if is_menu:
            w = CTkOptionMenu(parent, values=[str(i) for i in range(18, 66)], height=45, corner_radius=12,
                            fg_color="#F1F3F5", button_color="#D22B2B", text_color="#2D3436")
        else:
            w = CTkEntry(parent, placeholder_text=placeholder, show="*" if is_pass else "", height=45, 
                        corner_radius=12, fg_color="#F1F3F5", border_width=0, text_color="#2D3436")
        if not use_grid: w.pack(fill="x", padx=15)
        return w

    # --- GENERATING THE UI ---
    name_entry = add_styled_field(form, "Full Name", "John Doe", "👤")

    # --- PHONE NUMBER ROW ---
    lbl_frame_phone = CTkFrame(form, fg_color="transparent")
    lbl_frame_phone.pack(fill="x", padx=15, pady=(15, 2))
    CTkLabel(lbl_frame_phone, text="📞", font=("Poppins", 14)).pack(side="left")
    CTkLabel(lbl_frame_phone, text="Mobile Number", font=("Poppins SemiBold", 13), text_color="#2D3436").pack(side="left", padx=8)
    
    phone_row = CTkFrame(form, fg_color="transparent")
    phone_row.pack(fill="x", padx=15)
    code_entry = CTkEntry(phone_row, width=60, height=45, corner_radius=12, fg_color="#F1F3F5", border_width=0)
    code_entry.insert(0, "+91")
    code_entry.pack(side="left", padx=(0, 5))
    phone_entry = CTkEntry(phone_row, placeholder_text="1234567890", height=45, corner_radius=12, fg_color="#F1F3F5", border_width=0)
    phone_entry.pack(side="left", fill="x", expand=True)

    email_entry = add_styled_field(form, "Email Address", "name@example.com", "✉️")
    age_menu = add_styled_field(form, "Donor Age", "", "🎂", is_menu=True)

    # Security Section
    CTkLabel(form, text="Security Settings", font=("Poppins Bold", 12), text_color="#D22B2B").pack(anchor="w", padx=15, pady=(25, 5))
    username_entry = add_styled_field(form, "Username", "unique_id", "📧")

    pass_row = CTkFrame(form, fg_color="transparent")
    pass_row.pack(fill="x", pady=(0, 10))
    password_entry = add_styled_field(pass_row, "Password", "••••••••", "🔒", is_pass=True, use_grid=True)
    password_entry.pack(side="left", fill="x", expand=True, padx=(15, 5))

    def toggle_password():
        if password_entry.cget('show') == '':
            password_entry.configure(show='*')
            toggle_btn.configure(text="👁️")
        else:
            password_entry.configure(show='')
            toggle_btn.configure(text="🙈")

    toggle_btn = CTkButton(pass_row, text="👁️", width=45, height=45, fg_color="#F1F3F5", text_color="#2D3436", corner_radius=12, command=toggle_password)
    toggle_btn.pack(side="right", padx=(0, 15))
    CTkLabel(form,text="",fg_color="#FFFFFF").pack()
    btn_save = CTkButton(app, text="Save and Proceed →", height=55, corner_radius=15,fg_color="#D22B2B", hover_color="#B22222", font=("Poppins SemiBold", 16), command=lambda:(save_and_continue()))
    btn_save.place(relx=0.5, rely=0.94, anchor="center", relwidth=0.85)

    app.mainloop()

if __name__ == "__main__":
    open_create_account()