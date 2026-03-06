from customtkinter import *
from tkinter.messagebox import *
from ui import payment 

def open_blood_request_view(id,user_details):
    app = CTk()
    app.title("Urgent Blood Request")
    app.resizable(False, False)
    set_appearance_mode("light")
    app.configure(fg_color="#F8FAFC") 

    # Dimensions
    width, height = 370,670
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    # ================= HEADER =================
    header_color = "#D22B2B"
    header = CTkFrame(app, fg_color=header_color, height=140, corner_radius=0)
    header.pack(fill="x")

    # Back Button
    CTkButton(header, text="←", font=("Poppins", 22, "bold"), text_color="white",fg_color="transparent", hover_color="#B22222", width=40,command=lambda: app.destroy()).place(x=15, y=25)
    CTkLabel(header, text="EMERGENCY REQUEST", font=("Poppins", 20, "bold"), text_color="white").place(relx=0.5, rely=0.35, anchor="center")
    

    # ================= FORM CONTAINER =================
    container = CTkScrollableFrame(
        app, fg_color="white", corner_radius=15, 
        scrollbar_button_color="#E2E8F0",
        border_width=1, border_color="#E2E8F0"
    )
    container.pack(fill="both", expand=True, padx=20, pady=(20, 10))

    def create_section_header(text, icon="📍"):
        lbl = CTkLabel(
            container, text=f"{icon} {text}", 
            font=("Poppins", 12, "bold"), 
            text_color="#64748B"
        )
        lbl.pack(anchor="w", pady=(15, 5), padx=10)

    # --- Section 1: Request Type ---
    create_section_header("WHO IS THIS FOR?", "🏥")
    
    request_type_var = StringVar(value="Other")
    
    def on_type_change(choice):
        if choice == "Myself":
            name_entry.delete(0, 'end')
            name_entry.insert(0, user_details['name'])
            name_entry.configure(state="disabled", fg_color="#F1F5F9")
            age_entry.insert(END,str(user_details['age']))
        else:
            name_entry.configure(state="normal", fg_color="#F8FAFC")
            name_entry.delete(0, 'end')

    type_seg = CTkSegmentedButton(
        container, 
        values=["Myself", "Other"],
        variable=request_type_var,
        command=on_type_change,
        selected_color="#1E293B",
        height=45,
        corner_radius=10
    )
    type_seg.pack(fill="x", padx=10, pady=5)

    # --- Section 2: Patient Info ---
    create_section_header("PATIENT DETAILS", "👤")
    
    name_entry = CTkEntry(container, placeholder_text="Full Legal Name", font=("Poppins", 13), height=50, corner_radius=10, border_color="#E2E8F0", fg_color="#F8FAFC"
    )
    name_entry.pack(fill="x", padx=10, pady=5)

    age_entry = CTkEntry(container, placeholder_text="Age (Years)", font=("Poppins", 13), height=50, corner_radius=10, border_color="#E2E8F0", fg_color="#F8FAFC")
    age_entry.pack(fill="x", padx=10, pady=5)
    

    # --- Section 3: Blood Group & Priority ---
    create_section_header("BLOOD GROUP", "🩸")
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    blood_group_dropdown = CTkOptionMenu(container,values=blood_groups,fg_color="#F8FAFC",button_color="#E2E8F0",button_hover_color="#CBD5E1",text_color="#1E293B",font=("Poppins", 13),dropdown_font=("Poppins", 13),height=50,corner_radius=10,anchor="center")
    blood_group_dropdown.pack(fill="x", padx=10, pady=5)

    blood_group_dropdown.set("Select Blood Group")
    create_section_header("PRIORITY LEVEL","⚠️")

    urgency_var = StringVar(value="MEDIUM")

    urgency_seg = CTkSegmentedButton(
        container, 
        values=["LOW", "MEDIUM", "EXTREME"],
        variable=urgency_var,
        selected_color="#D22B2B",
        selected_hover_color="#B22222",
        font=("Poppins", 11, "bold"),
        height=45,
        corner_radius=10
    )
    urgency_seg.pack(fill="x", padx=10, pady=5)

    # --- Section 4: Hospital Info ---
    create_section_header("LOCATION", "🏢")
    hospital_entry = CTkEntry(
        container, placeholder_text="Hospital Name / City", 
        font=("Poppins", 13), height=50, corner_radius=10, 
        border_color="#E2E8F0", fg_color="#F8FAFC"
    )
    hospital_entry.pack(fill="x", padx=10, pady=5)

    # ================= FOOTER =================
    footer = CTkFrame(app, fg_color="white", height=100)
    footer.pack(fill="x", side="bottom", padx=0, pady=0)

    def submit():
        name = name_entry.get()
        blood = blood_group_dropdown.get()
        
        if not name or blood == "Select Blood Group":
            showwarning("Missing Info", "Please provide the patient name and blood group.")
            return

        confirm = askyesno("Confirm Request", f"Broadcast urgent request for {blood} blood?")
        if confirm:
            data = {"userid":user_details['id'],"blood_bank_id":101,"blood_bank_name":"Java Seva Blood Bank","destination_loc":hospital_entry.get(),"user": user_details["name"],"recipient_name": name,"type": request_type_var.get(),"blood_group": blood,"urgency": urgency_var.get(),"age":age_entry.get(),"email_id":user_details['email_id'],"request_type":"NEED"}
            app.destroy()
            payment.open_payment_gateway(id,data)

    submit_btn = CTkButton(footer,text="Broadcast Urgent Request",fg_color="#D22B2B", hover_color="#B22222",font=("Poppins", 15, "bold"),height=55,corner_radius=12,command=submit)
    submit_btn.pack(fill="x", padx=20, pady=20)

    app.mainloop()

if __name__ == "__main__":
    open_blood_request_view()