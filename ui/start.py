from customtkinter import *
from ui import login

def open_landing_page():
    def open_nextPage():
        app.quit()
    # Initialize the app
    app = CTk()
    app.resizable(False, False)
    app.title("Blood Bank | Gift of Life")
    
    # Professional Crimson Red
    app.configure(fg_color="#D22B2B") 
    
    # Window dimensions and centering
    width, height = 370, 670
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    padx = (screen_width - width) // 2
    pady = (screen_height - height) // 2
    app.geometry(f"{width}x{height}+{padx}+{pady}")

    # ================= TOP CIRCULAR HERO SECTION =================
    # Creating a large soft-white circle for the welcome area
    main_frame = CTkFrame(
        app,
        fg_color="#FFFFFF",
        corner_radius=200,
        width=450,
        height=450,
    )
    # Positioned to create a curved header effect
    main_frame.place(x=-40, y=-120)

    # Welcome Text inside the circle
    welcome_lbl = CTkLabel(
        main_frame, 
        text="Welcome", 
        font=("Poppins SemiBold", 36),
        text_color="#D22B2B"
    )
    welcome_lbl.place(relx=0.5, rely=0.62, anchor="center")

    subtitle_lbl = CTkLabel(
        main_frame, 
        text="Blood Bank Community", 
        font=("Poppins", 14),
        text_color="#666666"
    )
    subtitle_lbl.place(relx=0.5, rely=0.70, anchor="center")

    # ================= MOTIVATIONAL SECTION (OUTSIDE) =================
    
    # Main Headline
    motivate_title = CTkLabel(
        app, 
        text="SAVE A LIFE", 
        font=("Poppins Bold", 32),
        text_color="#FFFFFF"
    )
    motivate_title.place(relx=0.5, rely=0.58, anchor="center")

    # Emotional Message
    details_lbl = CTkLabel(
        app, 
        text="Your courage to donate blood\ncan give a mother her son back,\nor a child their future.", 
        font=("Poppins", 15),
        text_color="#FFDADA",
        justify="center",
        wraplength=300
    )
    details_lbl.place(relx=0.5, rely=0.68, anchor="center")

    # Decorative Quote
    quote_lbl = CTkLabel(
        app, 
        text="“The blood you donate gives someone\nanother chance at life.”", 
        font=("Poppins", 12, "italic"),
        text_color="#FFFFFF"
    )
    quote_lbl.place(relx=0.5, rely=0.78, anchor="center")

    # ================= ACTION BUTTONS =================

    start_btn = CTkButton(
        app,
        text="Donate Now",
        fg_color="#FFFFFF",
        text_color="#D22B2B",
        hover_color="#F2F2F2",
        corner_radius=25,
        font=("Poppins SemiBold", 16),
        height=50,
        width=220,
        command=open_nextPage
    )
    start_btn.place(relx=0.5, rely=0.88, anchor="center")

    app.mainloop()
    app.destroy() 
    login.open_login_page()