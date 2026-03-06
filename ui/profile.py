from customtkinter import *
from backend import db
from datetime import datetime
from ui import dashboard,login

def open_profile_view(id):
    app = CTk()
    app.title("User Profile")
    app.resizable(False, False)
    set_appearance_mode("light")
    app.configure(fg_color="#F8FAFC")

    width, height = 380, 700
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    # ================= FETCH USER =================
    user_data = db.fetch_current_userId(id)

    # ================= FORMAT DATE =================
    raw_date = user_data.get("created_at", "")
    try:
        formatted_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y, %I:%M %p")
    except:
        formatted_date = raw_date

    # ================= HEADER =================
    header_color = "#D22B2B"
    header_container = CTkFrame(app, fg_color=header_color, height=120, corner_radius=0)
    header_container.pack(fill="x")

    def backToDashboard():
        app.destroy()
        dashboard.open_dashboard(id)

    def handle_logout():
        app.destroy()
        login.open_login_page()

    # Back Button
    CTkButton(
        header_container,
        text="←",
        font=("Poppins Bold", 20),
        text_color="white",
        fg_color="transparent",
        hover_color="#B22222",
        width=30,
        command=backToDashboard
    ).place(x=10, y=20)

    # Logout Button (Clean, top-right placement)
    CTkButton(
        header_container,
        text="Logout",
        font=("Poppins SemiBold", 11),
        text_color="white",
        fg_color="#B91C1C",
        hover_color="#991B1B",
        width=70,
        height=28,
        corner_radius=8,
        command=handle_logout
    ).place(x=300, y=24)

    CTkLabel(
        header_container,
        text="OFFICIAL PROFILE",
        font=("Poppins Bold", 18),
        text_color="white"
    ).place(relx=0.5, rely=0.5, anchor="center")

    # ================= MAIN CONTENT =================
    content_frame = CTkFrame(app, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=25, pady=(40, 0))

    # ---- NAME ----
    CTkLabel(
        content_frame,
        text=user_data["name"],
        font=("Poppins Bold", 22),
        text_color="#0F172A",
        wraplength=320,
        justify="center"
    ).pack(padx=10)

    # ---- USERNAME BADGE ----
    badge = CTkFrame(content_frame, fg_color="#E2E8F0", corner_radius=20)
    badge.pack(pady=(6, 15))

    CTkLabel(
        badge,
        text=f"@{user_data['username'].lower()}",
        font=("Poppins SemiBold", 11),
        text_color="#475569",
        padx=12,
        pady=2
    ).pack()

    # ================= INFO SECTION =================
    info_scroll = CTkScrollableFrame(content_frame, fg_color="transparent")
    info_scroll.pack(fill="both", expand=True)

    def add_info(label, value, highlight=False):
        row = CTkFrame(info_scroll, fg_color="transparent")
        row.pack(fill="x", pady=8)

        CTkLabel(
            row,
            text=label,
            font=("Poppins Bold", 10),
            text_color="#64748B"
        ).pack(anchor="w")

        box = CTkFrame(
            row,
            fg_color="#FFF1F1" if highlight else "#FFFFFF",
            border_color="#FECACA" if highlight else "#E2E8F0",
            border_width=1,
            corner_radius=8
        )
        box.pack(fill="x", pady=(4, 0))

        CTkLabel(
            box,
            text=value if value else "Not Provided",
            font=("Poppins Medium", 13),
            text_color="#1E293B",
            padx=12,
            pady=8,
            wraplength=280,
            justify="left"
        ).pack(anchor="w")

    # ---- INFO FIELDS ----
    add_info("OFFICIAL EMAIL", user_data["email_id"])
    add_info("CONTACT NUMBER", user_data["phone_no"])
    add_info("AGE", f"{user_data['age']} Years")
    add_info("RESIDENTIAL ADDRESS", user_data["home_location"])
    add_info("JOINED SYSTEM", formatted_date, highlight=True)

    # ================= FOOTER =================
    footer = CTkFrame(app, fg_color="white", height=100)
    footer.pack(fill="x", side="bottom")

    CTkButton(
        footer,
        text="Edit Profile",
        fg_color="#1E293B",
        hover_color="#000000",
        font=("Poppins Bold", 13),
        height=45,
        corner_radius=10
    ).pack(fill="x", padx=30, pady=(15, 5))

    CTkButton(
        footer,
        text="Deactivate Account",
        fg_color="transparent",
        text_color="#B91C1C",
        hover_color="#FEE2E2",
        font=("Poppins SemiBold", 11)
    ).pack(pady=(0, 10))

    app.mainloop()