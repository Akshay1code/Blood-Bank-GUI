from customtkinter import *
from tkinter import *
from ui import donor_info
from backend import db
from ui import availability

def open_welcome_page(id, b_id, hospital):
    def open_nextPage():
        app.destroy()
        donor_info.open_donate_page(id)

    def goToAvailability():
        app.destroy()
        availability.open_availability(id, {}) 

    # ================= WINDOW SETUP =================
    app = CTk()
    app.title("Welcome")
    app.resizable(False, False)
    app.configure(fg_color="#D22B2B") 

    width, height = 370, 670
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    # ================= TOP BRANDING =================
    top_bar = CTkFrame(app, fg_color="transparent", height=50)
    top_bar.pack(fill="x", pady=(15, 0), padx=15)
    
    back_btn = CTkButton(top_bar, text="←", font=("Poppins Bold", 20), width=40, height=40,
                          fg_color="#990808", hover_color="#7A0606", text_color="white",
                          corner_radius=12, command=goToAvailability)
    back_btn.pack(side="left")

    CTkLabel(top_bar, text="Greetings", font=("Poppins Bold", 15), text_color="#FFFFFF").pack(side="left", padx=20)

    # ================= MAIN BODY CARD =================
    main_card = CTkFrame(app, fg_color="#FFFFFF", corner_radius=35)
    main_card.pack(fill="both", expand=True, pady=(20, 0))

    content_area = CTkFrame(main_card, fg_color="transparent")
    content_area.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.9)

    # 1. ILLUSTRATION
    icon_bg = CTkFrame(content_area, fg_color="#F3F3F3", width=100, height=100, corner_radius=50)
    icon_bg.pack(pady=(0, 25))
    icon_bg.pack_propagate(False)
    CTkLabel(icon_bg, text="🤝", font=("Poppins", 45)).place(relx=0.5, rely=0.5, anchor="center")

    # 2. GREETING
    CTkLabel(content_area, text="Welcome!", font=("Poppins Bold", 32), text_color="#1E293B").pack()
    CTkLabel(content_area, text="Thank you for choosing", font=("Poppins Medium", 14), text_color="#64748B").pack(pady=(5, 0))

    # 3. HORIZONTAL HOSPITAL NAME + ID BADGE
    # We use a frame to keep them on the same line
    bank_info_frame = CTkFrame(content_area, fg_color="transparent")
    bank_info_frame.pack(pady=10)

    hospital_label = CTkLabel(
        bank_info_frame, 
        text=hospital, 
        font=("Poppins Bold", 18), 
        text_color="#D22B2B",
        wraplength=220, # Reduced to make room for badge
        justify="center"
    )
    hospital_label.pack(side="left")

    badge_frame = CTkFrame(bank_info_frame, fg_color="#F1F5F9", corner_radius=8, border_width=1, border_color="#E2E8F0")
    badge_frame.pack(side="left", padx=(10, 0))
    
    CTkLabel(
        badge_frame, 
        text=f"ID {b_id}", 
        font=("Poppins Bold", 10), 
        text_color="#64748B",
        padx=8,
        pady=2
    ).pack()

    # 4. SUPPORTING TEXT
    CTkLabel(
        content_area, 
        text="We are committed to making your donation process smooth and safe. Your contribution truly makes a difference.", 
        font=("Poppins", 13), text_color="#94A3B8", wraplength=280, justify="center"
    ).pack(pady=(10, 0))

    # ================= BOTTOM NAVIGATION =================
    nav_area = CTkFrame(main_card, fg_color="transparent")
    nav_area.pack(side="bottom", fill="x", padx=30, pady=40)

    stepper = CTkFrame(nav_area, fg_color="transparent")
    stepper.pack(pady=(0, 20))
    for i in range(3):
        dot_color = "#D22B2B" if i == 0 else "#E2E8F0"
        dot_width = 20 if i == 0 else 8 
        CTkFrame(stepper, fg_color=dot_color, width=dot_width, height=8, corner_radius=4).pack(side="left", padx=3)

    btn_proceed = CTkButton(
        nav_area, text="PROCEED TO NEXT", height=55, corner_radius=18,
        fg_color="#1E293B", hover_color="#334155", font=("Poppins Bold", 14),
        command=open_nextPage
    )
    btn_proceed.pack(fill="x")

    app.mainloop()

if __name__ == "__main__":
    open_welcome_page("test_user", "101", "AIMS Hospital")