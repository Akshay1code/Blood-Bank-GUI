from customtkinter import *
from tkinter import filedialog
from ui import message
from ui import donor_info

set_appearance_mode("light")

def open_donor_form(username="Guest"):
    app = CTk()
    app.title("Donor Pre-Screening")
    app.resizable(False, False)
    app.configure(fg_color="#D22B2B")

    width, height = 370, 670
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    # --- BACK LOGIC ---
    def go_back():
        app.destroy()
        donor_info.open_donate_page(username)

    # --- TOP BRANDING ---
    header_curve = CTkFrame(app, fg_color="#D22B2B", width=500, height=300, corner_radius=250)
    header_curve.place(x=-65, y=-180)

    back_btn = CTkButton(app, text="←", font=("Poppins Bold", 20), width=40, height=40, 
                          fg_color="#B22222", hover_color="#8B1A1A", corner_radius=10, command=go_back)
    back_btn.place(x=20, y=20)

    CTkLabel(app, text="Health Screening", font=("Poppins Bold", 24), text_color="white").place(x=70, y=35)
    CTkLabel(app, text="Clinical Eligibility Check", font=("Poppins", 13), text_color="#FFDADA").place(x=70, y=68)

    # ================= MAIN CONTAINER =================
    main = CTkFrame(app, fg_color="#FFFFFF", corner_radius=35)
    main.place(relx=0.5, rely=0.6, anchor="center", relwidth=1.0, relheight=0.82)

    form = CTkScrollableFrame(main, fg_color="#FFFFFF", scrollbar_button_color="#F1F5F9")
    form.pack(fill="both", expand=True, padx=15, pady=(20, 10))

    # ================= HELPERS =================
    def section_header(text):
        lbl = CTkLabel(form, text=text, font=("Poppins Bold", 14), text_color="#D22B2B", justify="left")
        lbl.pack(anchor="w", padx=10, pady=(15, 5))
        return lbl

    def create_yes_no(question):
        frame = CTkFrame(form, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=5)
        
        # Note: CTkLabel DOES support wraplength, so we keep it here for automatic wrapping
        CTkLabel(frame, text=question, font=("Poppins Medium", 12), text_color="#334155", 
                 wraplength=280, justify="left").pack(anchor="w")
        
        radio_frame = CTkFrame(frame, fg_color="transparent")
        radio_frame.pack(anchor="w", pady=(2, 8))
        
        var = StringVar(value="No")
        CTkRadioButton(radio_frame, text="Yes", variable=var, value="Yes", font=("Poppins", 11),
                       fg_color="#D22B2B", radiobutton_width=18, radiobutton_height=18).pack(side="left", padx=(0, 20))
        CTkRadioButton(radio_frame, text="No", variable=var, value="No", font=("Poppins", 11),
                       fg_color="#D22B2B", radiobutton_width=18, radiobutton_height=18).pack(side="left")
        return var

    # ================= FORM SECTIONS =================

    # --- Section 1: Immediate Health ---
    section_header("🔴 Section 1: Immediate Health")
    q1 = create_yes_no("Do you currently feel well enough to donate blood?")
    q2 = create_yes_no("Have you had fever, cold, cough, or infection in last 14 days?")
    q3 = create_yes_no("Have you taken antibiotics or strong medicines in last 7 days?")
    q4 = create_yes_no("Have you received any vaccination in the last 7 days?")
    
    # --- Section 2: Donation Eligibility ---
    section_header("🔴 Section 2: Donation Eligibility")
    q5 = create_yes_no("Is your weight more than 50 kg?")
    q6 = create_yes_no("Have you donated blood in the last 3 months?")

    # --- Section 3: Medical History ---
    section_header("🔴 Section 3: Medical History")
    q7 = create_yes_no("Do you have any chronic illness (Heart, Epilepsy, Cancer, etc.)?")
    q8 = create_yes_no("Are you currently on regular medication?")
    q9 = create_yes_no("Have you undergone surgery or transfusion in last 6 months?")

    # --- Section 4: Risk & Safety ---
    section_header("🔴 Section 4: Risk & Safety")
    q10 = create_yes_no("Have you ever tested positive for HIV, Hepatitis B or C?")
    q11 = create_yes_no("Have you had a tattoo or body piercing in last 6–12 months?")

    # --- Section 5: Specific Indicators ---
    section_header("🔴 Section 5: Additional Indicators")
    q12 = create_yes_no("Are you currently pregnant or breastfeeding?")

    # ================= CONSENT & SUBMIT =================
    section_header("📝 Final Consent")
    
    consent_1 = BooleanVar(value=False)
    consent_2 = BooleanVar(value=False)

    def toggle_submit(*args):
        if consent_1.get() and consent_2.get():
            submit_btn.configure(state="normal", fg_color="#D22B2B")
        else:
            submit_btn.configure(state="disabled", fg_color="#E2E8F0")

    # Manually wrapped text for Checkboxes as they don't support wraplength
    c1_text = "I confirm that the above information is true to\nthe best of my knowledge."
    c1 = CTkCheckBox(form, text=c1_text, 
                     variable=consent_1, command=toggle_submit, font=("Poppins", 11), 
                     text_color="#64748B", checkbox_height=18, checkbox_width=18, fg_color="#D22B2B")
    c1.pack(anchor="w", padx=10, pady=5)

    c2_text = "I understand that final eligibility will be decided\nafter medical screening at the blood bank."
    c2 = CTkCheckBox(form, text=c2_text, 
                     variable=consent_2, command=toggle_submit, font=("Poppins", 11), 
                     text_color="#64748B", checkbox_height=18, checkbox_width=18, fg_color="#D22B2B")
    c2.pack(anchor="w", padx=10, pady=5)

    btn_frame = CTkFrame(main, fg_color="white", height=80)
    btn_frame.pack(side="bottom", fill="x", padx=20, pady=20)

    submit_btn = CTkButton(btn_frame, text="Complete Pre-Screening", font=("Poppins Bold", 15), 
                            state="disabled", fg_color="#E2E8F0", text_color_disabled="#94A3B8",
                            hover_color="#A31D1D", corner_radius=15, height=50,
                            command=lambda: [app.destroy(), message.open_status_page(username)])
    submit_btn.pack(fill="x")

    app.mainloop()

if __name__ == "__main__":
    open_donor_form()