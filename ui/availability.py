from customtkinter import *
from tkinter import *
from ui import greetings
from ui import dashboard
from ui import need
import backend.db as db

# ================= ENHANCED DATA (Added specific IDs) =================

MOCK_URGENT_NEEDS = [
    {"id": "101", "name": "City Bank Hospital", "address": "Dombivli East", "groups": ["O+", "A-"]},
    {"id": "120", "name": "Lifeline Critical Care", "address": "MIDC Phase 2", "groups": ["B-", "AB-"]},
    {"id": "145", "name": "Metro Blood Center", "address": "Manpada Road", "groups": ["O-", "O+"]},
    {"id": "123", "name": "Arpan Blood Bank", "address": "Kalyan Shil Road", "groups": ["A+", "B+"]}
]

def open_availability(id, user_details):

    # ================= NAVIGATION =================
    def backToDashboard():
        app.destroy()
        dashboard.open_dashboard(id)

    def open_welcome(b_id,hospital):
        app.destroy()
        greetings.open_welcome_page(id,b_id,hospital)

    def open_waiting():
        app.destroy()
        need.open_blood_request_view(id, user_details)

    # ================= APP SETUP =================
    app = CTk()
    app.title("Blood Service Portal")
    app.resizable(False, False)
    app.configure(fg_color="#D22B2B")

    width, height = 370, 670
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    # ================= HEADER =================
    header = CTkFrame(app, fg_color="#D22B2B", height=140, corner_radius=0)
    header.pack(fill="x")

    CTkButton(header, text="←", font=("Poppins Bold", 20), text_color="white",
              fg_color="#B22222", width=40, height=40, corner_radius=12,
              hover_color="#8B0000", command=backToDashboard).place(x=20, y=25)

    CTkLabel(header, text="Blood Services", font=("Poppins Bold", 24), text_color="white").place(x=75, y=25)
    CTkLabel(header, text="📍 Serving Dombivli Region", font=("Poppins Medium", 12), text_color="#FFDADA").place(x=75, y=58)

    # ================= MAIN CONTAINER =================
    main = CTkFrame(app, fg_color="#F8FAFC", corner_radius=35)
    main.pack(fill="both", expand=True)

    # ================= TAB TOGGLE =================
    toggle_container = CTkFrame(main, fg_color="#E2E8F0", corner_radius=15, height=52)
    toggle_container.pack(fill="x", padx=25, pady=20)

    def switch_tab(tab):
        if tab == "need":
            need_frame.lift()
            btn_need.configure(fg_color="#FFFFFF", text_color="#D22B2B")
            btn_donate.configure(fg_color="transparent", text_color="#64748B")
        else:
            donate_frame.lift()
            btn_donate.configure(fg_color="#FFFFFF", text_color="#D22B2B")
            btn_need.configure(fg_color="transparent", text_color="#64748B")

    btn_need = CTkButton(toggle_container, text="Request Blood", fg_color="#FFFFFF", text_color="#D22B2B",
                         corner_radius=10, height=38, font=("Poppins Bold", 13),
                         command=lambda: switch_tab("need"))
    btn_need.place(relx=0.03, rely=0.5, relwidth=0.46, anchor="w")

    btn_donate = CTkButton(toggle_container, text="Urgent Needs", fg_color="transparent", text_color="#64748B",
                           corner_radius=10, height=38, font=("Poppins Bold", 13),
                           command=lambda: switch_tab("donate"))
    btn_donate.place(relx=0.97, rely=0.5, relwidth=0.46, anchor="e")

    # ================= STACK =================
    stack = CTkFrame(main, fg_color="transparent")
    stack.pack(fill="both", expand=True)

    need_frame = CTkFrame(stack, fg_color="transparent")
    donate_frame = CTkScrollableFrame(stack, fg_color="transparent", scrollbar_button_color="#CBD5E1")

    for f in (need_frame, donate_frame):
        f.place(relx=0, rely=0, relwidth=1, relheight=1)

    need_frame.lift()

    # ================= CALM NEED UI =================
    instruction_card = CTkFrame(need_frame, fg_color="#FFFFFF", corner_radius=25, border_width=1, border_color="#E2E8F0")
    instruction_card.pack(fill="both", expand=True, padx=25, pady=30)

    # Compassionate Icon Placeholder
    CTkLabel(instruction_card, text="🏥", font=("Poppins Bold", 45)).pack(pady=(30, 0))
    
    CTkLabel(instruction_card, text="Urgent Blood Service", font=("Poppins Bold", 20), text_color="#0F172A").pack(pady=(10, 5))

    CTkLabel(instruction_card, text=(
        "Apply for priority blood allocation.\n"
        "Our coordination team will find the\n"
        "nearest available unit for you."
    ), font=("Poppins Medium", 13), text_color="#64748B", justify="center").pack(padx=20, pady=10)

    # Reassurance Box
    status_box = CTkFrame(instruction_card, fg_color="#F0F9FF", corner_radius=12) # Blueish for calm
    status_box.pack(fill="x", padx=20, pady=15)
    CTkLabel(status_box, text="Verified Medical Networks Only", font=("Poppins Bold", 11), text_color="#0369A1").pack(pady=8)

    CTkButton(instruction_card, text="APPLY FOR SERVICE", height=50, corner_radius=15,
              fg_color="#D22B2B", hover_color="#B91C1C", font=("Poppins Bold", 14),
              command=open_waiting).pack(fill="x", padx=20, pady=(5, 10))

    CTkButton(instruction_card, text="Go Back", fg_color="transparent", text_color="#94A3B8",
              font=("Poppins SemiBold", 12), command=backToDashboard).pack()

    # ================= URGENT NEEDS CARDS (ID Included) =================
    def urgent_card(parent, b_id, blood_types, hospital, location):
        card = CTkFrame(parent, fg_color="#FFFFFF", corner_radius=20, border_width=1, border_color="#E2E8F0")
        card.pack(fill="x", pady=10, padx=15)

        # Hospital ID Badge
        id_badge = CTkFrame(card, fg_color="#F1F5F9", corner_radius=8)
        id_badge.place(relx=0.92, rely=0.15, anchor="e")
        CTkLabel(id_badge, text=f"ID: {b_id}", font=("Poppins Bold", 9), text_color="#64748B").pack(padx=6, pady=2)

        CTkLabel(card, text="URGENT REQUIREMENT", font=("Poppins Bold", 10), text_color="#D22B2B").pack(anchor="w", padx=15, pady=(15, 0))
        CTkLabel(card, text=hospital, font=("Poppins Bold", 16), text_color="#1E293B").pack(anchor="w", padx=15)
        CTkLabel(card, text=f"📍 {location}", font=("Poppins Medium", 11), text_color="#94A3B8").pack(anchor="w", padx=15, pady=(0, 10))

        badge_container = CTkFrame(card, fg_color="transparent")
        badge_container.pack(anchor="w", padx=10, pady=(0, 15))

        for i, b in enumerate(blood_types):
            badge = CTkFrame(badge_container, fg_color="#D22B2B", corner_radius=6)
            badge.grid(row=0, column=i, padx=4)
            CTkLabel(badge, text=b, font=("Poppins Bold", 11), text_color="white").pack(padx=8, pady=2)

        CTkButton(card, text="DONATE NOW", height=35, corner_radius=10, fg_color="#0F172A",
                  hover_color="#1E293B", font=("Poppins Bold", 12), command=lambda i=b_id,j=hospital:open_welcome(i,j)).pack(fill="x", padx=15, pady=(0, 15))

    for urgent in MOCK_URGENT_NEEDS:
        urgent_card(donate_frame, urgent["id"], urgent["groups"], urgent["name"], urgent["address"])

    app.mainloop()

if __name__ == "__main__":
    # Test call
    open_availability("user123", {"location": "Dombivli"})