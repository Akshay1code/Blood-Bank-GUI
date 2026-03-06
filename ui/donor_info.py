from customtkinter import *
from ui import donar_form 
from ui import availability
def open_donate_page(username="Guest"):
    app = CTk()
    app.title("Donor Safety Guidelines")
    app.resizable(False, False)
    set_appearance_mode("light")
    
    # Branded Background
    app.configure(fg_color="#D22B2B") 

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    width, height = 370, 670
    padx = (screen_width - width) // 2
    pady = (screen_height - height) // 2
    app.geometry(f"{width}x{height}+{padx}+{pady}")

    # ================= TOP LOGO/ICON AREA =================
    header_circle = CTkFrame(app, fg_color="#990808", width=400, height=300, corner_radius=200)
    header_circle.place(x=-15, y=-180)

    # --- NEW: BACK BUTTON ---
    def go_back():
        app.destroy()
        availability.open_availability(username)
        

    back_btn = CTkButton(
        app, 
        text="←", 
        font=("Poppins Bold", 20),
        width=40,
        height=40,
        fg_color="#990808", # Matches header circle
        hover_color="#7A0606",
        text_color="white",
        corner_radius=10,
        command=go_back
    )
    back_btn.place(x=20, y=20)

    # ================= MAIN CONTAINER =================
    main = CTkFrame(app, fg_color="#FFFFFF", corner_radius=30)
    main.place(relx=0.5, rely=0.6, anchor="center", relwidth=1.0, relheight=0.82)

    # Header Text
    CTkLabel(main, text="Safety Checklist", font=("Poppins Bold", 22), 
             text_color="#1E293B").pack(pady=(25, 2))
    CTkLabel(main, text="Review these steps to ensure a safe donation", 
             font=("Poppins", 11), text_color="#64748B").pack(pady=(0, 15))

    # ================= SCROLLABLE CONTENT =================
    content = CTkScrollableFrame(main, fg_color="#FFFFFF", scrollbar_button_color="#F1F5F9", scrollbar_button_hover_color="#E2E8F0")
    content.pack(fill="both", expand=True, padx=15, pady=5)

    def add_instruction_block(parent, emoji, title, points):
        block = CTkFrame(parent, fg_color="#F8FAFC", corner_radius=15, border_width=1, border_color="#F1F5F9")
        block.pack(fill="x", pady=8, padx=5)

        title_frame = CTkFrame(block, fg_color="transparent")
        title_frame.pack(fill="x", padx=12, pady=(12, 5))
        
        CTkLabel(title_frame, text=emoji, font=("Segoe UI Emoji", 18)).pack(side="left")
        CTkLabel(title_frame, text=title, font=("Poppins SemiBold", 14), 
                 text_color="#D22B2B").pack(side="left", padx=8)

        for p in points:
            point_frame = CTkFrame(block, fg_color="transparent")
            point_frame.pack(fill="x", padx=15, pady=2)
            
            CTkLabel(point_frame, text="•", font=("Poppins Bold", 14), 
                     text_color="#94A3B8").pack(side="left")
            CTkLabel(point_frame, text=p, font=("Poppins", 12), text_color="#334155", 
                     wraplength=260, justify="left").pack(side="left", padx=5)
        
        CTkLabel(block, text="", height=5).pack()

    # Content Sections
    add_instruction_block(content, "⚖️", "Eligibility Basics", ["Age: 18 – 65 years", "Weight: Minimum 50 kg", "Healthy & well-rested"])
    add_instruction_block(content, "🥗", "Preparation", ["Eat a light meal (no fasting)", "Drink plenty of water/fluids", "Avoid alcohol for 24 hours"])
    add_instruction_block(content, "🪪", "What to Bring", ["Government Photo ID Card", "Donor Card (if you have one)"])
    add_instruction_block(content, "🩹", "Post-Donation Care", ["Rest for 10 minutes after", "Avoid heavy lifting for today", "Stay hydrated"])

    disclaimer_box = CTkFrame(content, fg_color="#FFFBEB", corner_radius=10)
    disclaimer_box.pack(fill="x", pady=15, padx=5)
    CTkLabel(disclaimer_box, text="Medical staff will perform a final check on-site.", 
             font=("Poppins", 10, "italic"), text_color="#92400E", wraplength=280).pack(pady=10)

    # ================= PROCEED BUTTON =================
    footer = CTkFrame(main, fg_color="white", height=80)
    footer.pack(side="bottom", fill="x")

    btn_proceed = CTkButton(
        footer,
        text="I Confirm & Understand",
        font=("Poppins Bold", 15),
        fg_color="#D22B2B",
        hover_color="#A31D1D",
        corner_radius=15,
        height=50,
        command=lambda: [app.destroy(), donar_form.open_donor_form(username)]
    )
    btn_proceed.pack(pady=20, padx=30, fill="x")

    app.mainloop()

if __name__ == "__main__":
    open_donate_page("JohnDoe")