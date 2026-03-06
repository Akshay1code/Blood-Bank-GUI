from customtkinter import *
from backend import db
from ui import dashboard

def open_waiting_room(id):
    def openDashboard():
        app.destroy()
        dashboard.open_dashboard(id)

    app = CTk()
    app.title("Blood Portal - Activity Center")
    app.resizable(False, False)
    set_appearance_mode("light")
    app.configure(fg_color="#F1F5F9")

    # Window Centering
    width, height = 370, 670
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")
        
    # ================= TOP HEADER =================
    header = CTkFrame(app, fg_color="#D22B2B", height=160, corner_radius=0)
    header.pack(fill="x")

    # Back to Dashboard via top button
    CTkButton(header, text="←", font=("Poppins Bold", 22), text_color="white", 
              fg_color="#B22222", width=40, height=40, corner_radius=20,
              hover_color="#8B0000", command=openDashboard).place(x=20, y=30)

    refresh_btn = CTkButton(header, text="↻", font=("Poppins Bold", 18),
                            text_color="white", fg_color="#B22222",
                            width=40, height=40, corner_radius=10,
                            hover_color="#8B0000", command=lambda: open_waiting_room(id))
    refresh_btn.place(x=310, y=30)

    CTkLabel(header, text="ACTIVITY LOG", font=("Poppins Bold", 10), text_color="#FFDADA").place(x=75, y=32)
    CTkLabel(header, text="Request Status", font=("Poppins Bold", 19), text_color="white").place(x=75, y=48)

    # ================= MAIN CONTAINER =================
    main_container = CTkFrame(app, fg_color="#FFFFFF", corner_radius=30, border_width=1, border_color="#E2E8F0")
    main_container.place(relx=0.5, rely=0.56, anchor="center", relwidth=0.90, relheight=0.80)

    # Fetching Data from Backend
    data, count = db.fetch_bloodQueue(id)

    if not data:
        # ================= EMPTY STATE UI =================
        empty_frame = CTkFrame(main_container, fg_color="transparent")
        empty_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Icon or Illustration Placeholder
        CTkLabel(empty_frame, text="Empty", font=("Poppins Bold", 40), 
                 text_color="#E2E8F0").pack()
        
        # Professional Empty State Message
        CTkLabel(empty_frame, text="No Active Requests Found", 
                 font=("Poppins Bold", 16), text_color="#1E293B").pack(pady=(10, 5))
        
        CTkLabel(empty_frame, text="You don't have any scheduled appointments\nor active blood requests at this moment.", 
                 font=("Poppins Medium", 12), text_color="#64748B", justify="center").pack()

        # Simple Return Button for Empty State
        btn_return = CTkButton(main_container, text="← RETURN TO DASHBOARD", height=45, 
                               corner_radius=15, fg_color="#F1F5F9", hover_color="#E2E8F0", 
                               text_color="#0F172A", font=("Poppins Bold", 12), command=openDashboard)
        btn_return.pack(side="bottom", fill="x", padx=20, pady=20)

    else:
        # ================= DATA EXISTS UI =================
        req_type = data.get("request_type", "NEED")
        badge_color = "#3B82F6" if req_type == "DONATE" else "#EF4444"

        # Content area with padding to avoid overlapping the corner badge
        content_frame = CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(40, 5))

        # Corner Badge
        type_badge = CTkFrame(main_container, fg_color=badge_color, corner_radius=10)
        type_badge.place(relx=0.95, rely=0.05, anchor="ne")
        CTkLabel(type_badge, text=req_type, font=("Poppins Bold", 10), text_color="white").pack(padx=12, pady=2)

        # Bank Name
        CTkLabel(content_frame, text=data["blood_bank_name"], 
                 font=("Poppins Bold", 17), text_color="#0F172A").pack(pady=(0, 2))
        
        id_badge = CTkFrame(content_frame, fg_color="#F1F5F9", corner_radius=8)
        id_badge.pack(pady=5)
        CTkLabel(id_badge, text=f"REQUEST ID: {data['id']}", font=("Poppins Bold", 10), text_color="#64748B").pack(padx=10, pady=2)

        CTkLabel(content_frame, text=f"📅 {data['created_at']}", 
                 font=("Poppins SemiBold", 11), text_color="#94A3B8").pack(pady=5)

        # Recipient Details
        CTkLabel(content_frame, text="RECIPIENT DETAILS", 
                 font=("Poppins Bold", 10), text_color="#94A3B8").pack(pady=(10, 2))
        
        recipient_info_frame = CTkFrame(content_frame, fg_color="transparent")
        recipient_info_frame.pack(pady=(0, 5))

        CTkLabel(recipient_info_frame, text=data["recipient_name"], 
                 font=("Poppins Bold", 14), text_color="#1E293B").pack(side="left", padx=(0, 8))

        blood_badge = CTkFrame(recipient_info_frame, fg_color="#D22B2B", corner_radius=6)
        blood_badge.pack(side="left")
        CTkLabel(blood_badge, text=data["blood_group"], font=("Poppins Bold", 10), text_color="white").pack(padx=6, pady=1)

        # Queue Status
        queue_badge = CTkFrame(content_frame, fg_color="#F8FAFC", corner_radius=10, border_width=1, border_color="#F1F5F9")
        queue_badge.pack(pady=10, fill="x")
        CTkLabel(queue_badge, text=f"👥 {count} users ahead of you", 
                 font=("Poppins Medium", 12), text_color="#475569").pack(pady=8)

        # Status Badge
        status_colors = {"WAITING": "#FEF3C7", "APPROVED": "#DCFCE7", "SERVED": "#DBEAFE"}
        text_colors = {"WAITING": "#92400E", "APPROVED": "#166534", "SERVED": "#1E40AF"}
        
        current_status = data["status"]
        status_frame = CTkFrame(content_frame, fg_color=status_colors.get(current_status, "#F1F5F9"), corner_radius=12)
        status_frame.pack(pady=10, fill="x")
        CTkLabel(status_frame, text=current_status, font=("Poppins Bold", 15), 
                 text_color=text_colors.get(current_status, "#0F172A")).pack(pady=10)

        # Remarks Box
        CTkLabel(content_frame, text="REMARKS", font=("Poppins Bold", 10), text_color="#94A3B8").pack(pady=(10, 0))
        remarks_box = CTkTextbox(content_frame, fg_color="#F8FAFC", font=("Poppins Medium", 11), 
                                 text_color="#475569", height=70, corner_radius=10, border_width=1, border_color="#E2E8F0")
        remarks_box.pack(fill="x", pady=5)
        remarks_box.insert("0.0", data["description"] if data["description"] else "No specific remarks provided.")
        remarks_box.configure(state="disabled")

        # Bottom Button for active data
        btn_return = CTkButton(main_container, text="← RETURN TO DASHBOARD", height=45, 
                               corner_radius=15, fg_color="#F1F5F9", hover_color="#E2E8F0", 
                               text_color="#0F172A", font=("Poppins Bold", 12), command=openDashboard)
        btn_return.pack(side="bottom", fill="x", padx=20, pady=(10, 20))

    app.mainloop()