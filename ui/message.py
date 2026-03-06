from customtkinter import *
from ui import dashboard
def open_status_page(username):
    # ================= WINDOW SETUP =================
    win = CTk()
    win.geometry("370x670")
    win.title("Donation Status")
    win.resizable(False, False)
    set_appearance_mode("light")

    win.configure(fg_color="#D22B2B")

    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    width, height = 370, 670
    win.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    # ================= TOP BRANDING =================
    header_curve = CTkFrame(win, fg_color="#D22B2B", width=500, height=300, corner_radius=250)
    header_curve.place(x=-65, y=-180)

    CTkLabel(win, text="✅", font=("Poppins", 32)).place(x=25, y=30)

    CTkLabel(
        win,
        text="Screening Passed",
        font=("Poppins", 24, "bold"),
        text_color="white"
    ).place(x=75, y=35)

    CTkLabel(
        win,
        text="You are eligible for medical check-up",
        font=("Poppins", 13),
        text_color="#FFDADA"
    ).place(x=77, y=68)

    # ================= MAIN CONTAINER =================
    main_container = CTkFrame(win, fg_color="#FFFFFF", corner_radius=35)
    main_container.place(relx=0.5, rely=0.56, anchor="center", relwidth=1.0, relheight=0.75)

    content = CTkScrollableFrame(
        main_container,
        fg_color="#FFFFFF",
        scrollbar_button_color="#F1F5F9",
        scrollbar_button_hover_color="#E2E8F0"
    )
    content.pack(fill="both", expand=True, padx=15, pady=20)

    # ================= SUMMARY =================
    summary_box = CTkFrame(content, fg_color="#F8FAFC", corner_radius=20)
    summary_box.pack(fill="x", pady=(10, 15))

    CTkLabel(
        summary_box,
        text="Based on your screening, a medical examination is required to proceed with your donation.",
        font=("Poppins", 13),
        text_color="#475569",
        wraplength=280
    ).pack(padx=20, pady=20)

    # ================= APPOINTMENT DETAILS =================
    appt_badge = CTkFrame(content, fg_color="#FFFFFF", border_width=2,
                          border_color="#F1F5F9", corner_radius=25)
    appt_badge.pack(fill="x", pady=5)

    title_row = CTkFrame(appt_badge, fg_color="transparent")
    title_row.pack(fill="x", pady=(15, 10))

    CTkLabel(title_row, text="📍", font=("Poppins", 16)).pack(side="left", padx=(20, 5))
    CTkLabel(
        title_row,
        text="APPOINTMENT DETAILS",
        font=("Poppins", 11, "bold"),
        text_color="#D22B2B"
    ).pack(side="left")

    details_frame = CTkFrame(appt_badge, fg_color="#F8FAFC", corner_radius=15)
    details_frame.pack(fill="x", padx=15, pady=(0, 15))

    CTkLabel(
        details_frame,
        text="🗓  18th March 2026\n⏰  10:00 AM – 11:00 AM\n\n🏥  City Bank Hospital, Dombivli",
        font=("Poppins", 14),
        text_color="#1E293B",
        justify="left"
    ).pack(padx=15, pady=15)

    # ================= GUIDELINES =================
    guide_frame = CTkFrame(content, fg_color="transparent")
    guide_frame.pack(fill="x", pady=10)

    CTkLabel(
        guide_frame,
        text="Quick Reminders:",
        font=("Poppins", 13, "bold"),
        text_color="#1E293B"
    ).pack(anchor="w", padx=10)

    guidelines = [
        "🪪 Bring your original Aadhar/Pan Card",
        "💧 Stay well hydrated before your visit",
        "🥗 Have a light meal 2 hours prior"
    ]

    for rule in guidelines:
        CTkLabel(
            guide_frame,
            text=rule,
            font=("Poppins", 12),
            text_color="#64748B",
            anchor="w"
        ).pack(fill="x", padx=10, pady=2)

    # ================= REGULATORY NOTE =================
    regulatory_box = CTkFrame(content, fg_color="#FFFBEB", corner_radius=12)
    regulatory_box.pack(fill="x", pady=20)

    CTkLabel(
        regulatory_box,
        text="Final acceptance is subject to on-site Medical Officer approval following mandatory NACO/NBTC testing protocols.",
        font=("Poppins", 10),
        text_color="#92400E",
        wraplength=280
    ).pack(padx=15, pady=10)

    # ================= FIXED FOOTER =================
    footer = CTkFrame(win, fg_color="#B22222", height=90, corner_radius=0)
    footer.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0)

    CTkLabel(
        footer,
        text="We are proud of your initiative ❤️",
        font=("Poppins", 11),
        text_color="#FFDADA"
    ).pack(pady=(12, 5))

    btn_done = CTkButton(
        footer,
        text="Return to Dashboard",
        font=("Poppins", 15, "bold"),
        fg_color="white",
        text_color="#D22B2B",
        hover_color="#F1F5F9",
        corner_radius=18,
        height=45,
        command=lambda:(win.destroy(), dashboard.open_dashboard(username))
    )
    btn_done.pack(pady=(0, 12), padx=20, fill="x")

    win.mainloop()


if __name__ == "__main__":
    open_status_page()
