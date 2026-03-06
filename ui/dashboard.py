from customtkinter import *
from ui import availability
from tkinter.messagebox import *
from backend import db
from ui import profile, waiting

def open_dashboard(id):
    def open_profile():
        app.destroy()
        profile.open_profile_view(id)

    def open_waiting_room():
        app.destroy()
        waiting.open_waiting_room(id)

    # ================= APP SETUP =================
    app = CTk()
    app.title("Donor Dashboard")
    app.resizable(False, False)
    set_appearance_mode("light")
    
    # Fetch User Details for the Greeting
    user_details = db.fetch_current_userId(id)
    if user_details is None:
        showerror("Error", "Database Error: User not found.")
        app.destroy()
        return

    # Branded Red Background
    app.configure(fg_color="#D22B2B")

    # Center window
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    width, height = 370, 670
    app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    # ================= TOP BRANDING BACKGROUND =================
    header_curve = CTkFrame(
        app,
        fg_color="#D22B2B",
        width=500,
        height=300,
        corner_radius=250
    )
    header_curve.place(x=-65, y=-180)

    # ================= STATIC PROFILE BUTTON =================
    profile_btn = CTkButton(
        app,
        text="👤",
        width=46,
        height=46,
        corner_radius=23, 
        fg_color="#D22B2B",
        hover_color="#B22222", 
        text_color="white",
        font=("Poppins", 20),
        command=open_profile
    )
    profile_btn.place(x=320, y=55, anchor="center")

    # ================= TOP TEXT =================
    first_name = user_details.get("name", "Donor").split()[0]
    CTkLabel(
        app,
        text=f"Hello, {first_name}! 👋",
        font=("Poppins", 26, "bold"),
        text_color="white"
    ).place(x=25, y=35)

    CTkLabel(
        app,
        text="Ready to save lives today?",
        font=("Poppins", 13),
        text_color="#FFDADA"
    ).place(x=25, y=70)

    # ================= MAIN CONTENT CONTAINER =================
    main_container = CTkFrame(
        app,
        fg_color="#F8F9FA",
        corner_radius=35
    )
    main_container.place(
        relx=0.5,
        rely=0.58,
        anchor="center",
        relwidth=1.0,
        relheight=0.78
    )

    content = CTkScrollableFrame(
        main_container,
        fg_color="#F8F9FA",
        scrollbar_button_color="#E2E8F0",
        scrollbar_button_hover_color="#CBD5E1"
    )
    content.pack(fill="both", expand=True, padx=10, pady=(10, 80))

    # ================= IMPACT SECTION =================
    impact_card = CTkFrame(
        content,
        fg_color="#FFFFFF",
        corner_radius=25,
        border_width=1,
        border_color="#EAEAEA"
    )
    impact_card.pack(fill="x", padx=10, pady=10)

    stat_frame = CTkFrame(impact_card, fg_color="transparent")
    stat_frame.pack(side="left", padx=20, pady=20)

    progress = CTkProgressBar(
        stat_frame,
        width=12,
        height=100,
        orientation="vertical",
        fg_color="#FEE2E2",
        progress_color="#D22B2B",
        corner_radius=10
    )
    progress.pack()
    progress.set(0.91)

    CTkLabel(
        stat_frame,
        text="91%",
        font=("Poppins", 14, "bold"),
        text_color="#D22B2B"
    ).pack(pady=5)

    text_frame = CTkFrame(impact_card, fg_color="transparent")
    text_frame.pack(side="left", fill="both", expand=True, pady=20)

    CTkLabel(text_frame, text="YOUR IMPACT", font=("Poppins", 11, "bold"), text_color="#94A3B8").pack(anchor="w")
    CTkLabel(text_frame, text="Life Saver Status", font=("Poppins", 18, "bold"), text_color="#1E293B").pack(anchor="w")
    CTkLabel(
        text_frame,
        text="You've helped more people\nthan 91% of donors in Dombivli.",
        font=("Poppins", 12),
        text_color="#64748B",
        justify="left"
    ).pack(anchor="w", pady=5)

    # ================= DYNAMIC APPOINTMENT SECTION =================
    data, count = db.fetch_bloodQueue(id)

    if data:
        # --- ACTIVE APPOINTMENT CARD ---
        appt_card = CTkFrame(content, fg_color="#D22B2B", corner_radius=25)
        appt_card.pack(fill="x", padx=10, pady=10)

        CTkLabel(
            appt_card,
            text="🗓 ACTIVE REQUEST",
            font=("Poppins", 11, "bold"),
            text_color="#FFCDCD"
        ).pack(anchor="w", padx=20, pady=(15, 0))

        detail_frame = CTkFrame(appt_card, fg_color="#B22222", corner_radius=15)
        detail_frame.pack(fill="x", padx=15, pady=15)

        # Hospital & Date Info
        hospital_source = data.get("blood_bank_name", "Local Blood Bank")
        dest_hospital = data.get("destination_hospital", "Emergency Department")
        date_str = data.get("created_at", "Date TBD")

        CTkLabel(
            detail_frame,
            text=f"{date_str}\n{hospital_source}",
            font=("Poppins", 13, "bold"),
            text_color="white",
            justify="left"
        ).pack(anchor="w", padx=15, pady=(12, 0))

        # Destination Info (High Trust)
        CTkLabel(
            detail_frame,
            text=f"📍 Delivery to: {dest_hospital}",
            font=("Poppins", 11),
            text_color="#FFDADA"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        # Waiting Room Button
        waiting_room_btn = CTkButton(
            detail_frame,
            text="Enter Waiting Room",
            height=35,
            corner_radius=10,
            fg_color="#FFFFFF",
            text_color="#D22B2B",
            hover_color="#FFDADA",
            font=("Poppins", 12, "bold"),
            command=open_waiting_room
        )
        waiting_room_btn.pack(fill="x", padx=15, pady=(0, 15))

    else:
        # --- EMPTY STATE CARD ---
        empty_card = CTkFrame(content, fg_color="#FFFFFF", corner_radius=25, border_width=1, border_color="#EAEAEA")
        empty_card.pack(fill="x", padx=10, pady=10)

        CTkLabel(
            empty_card, 
            text="No Active Appointments", 
            font=("Poppins", 14, "bold"), 
            text_color="#1E293B"
        ).pack(pady=(20, 5))
        
        CTkLabel(
            empty_card, 
            text="Your scheduled blood deliveries or\ndonations will appear here.", 
            font=("Poppins", 11), 
            text_color="#64748B",
            justify="center"
        ).pack(pady=(0, 20))

    # ================= SEARCH BLOOD CTA =================
    def check_availability():
        app.destroy()
        availability.open_availability(id, user_details)

    search_cta = CTkButton(
        content,
        text="        Blood Assistance",
        height=70,
        corner_radius=20,
        fg_color="#FFFFFF",
        border_width=2,
        border_color="#D22B2B",
        text_color="#D22B2B",
        font=("Poppins", 15, "bold"),
        hover_color="#F8F9FA",
        command=check_availability,
        anchor="w"
    )
    search_cta.pack(fill="x", padx=10, pady=15)

    CTkLabel(
        search_cta,
        text="🔍",
        font=("Poppins", 20)
    ).place(relx=0.08, rely=0.5, anchor="center")

    # ================= FOOTER =================
    footer = CTkFrame(app, fg_color="#D22B2B", height=65)
    footer.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0)

    CTkLabel(
        footer,
        text="“A few minutes of your time can give someone years of life.”",
        font=("Poppins Bold", 11, 'bold'),
        text_color="#FFFFFF",
        wraplength=300,
        justify="center"
    ).pack(expand=True, pady=10)

    app.mainloop()

if __name__ == "__main__":
    # Test with a dummy ID
    open_dashboard("test_user_id")