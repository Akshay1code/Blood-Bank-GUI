from customtkinter import *
import qrcode
from PIL import Image
from ui import availability
from ui import dashboard,waiting
import time,requests,threading
from backend import db
from tkinter.messagebox import *
def open_payment_gateway(id,data):
    def open_waiting():
        if db.saveToBloodQueue(data):
            pay_app.destroy()
            waiting.open_waiting_room(id)
            
        
    def openAvailability():
        pay_app.destroy()
        dashboard.open_dashboard(id)

    def generate_qr():
        url="https://qr-trigger.vercel.app/"
        qr=qrcode.QRCode()
        qr.add_data(url)
        dis_img=qr.make_image().convert("RGB")
        show_img=CTkImage(light_image=dis_img,size=(200,200))
        return show_img

    def on_payment_success():
        print("✅ Payment confirmed")

        payment_layer.lower()
        success_layer.lift()
        # reset for next use
        try:
            requests.get(
                "https://qr-trigger.vercel.app/api/status?value=0",
                verify=False
            )
        except:
            pass

    def checkStatus(root):
        URL = "https://qr-trigger.vercel.app/api/status"

        while True:
            try:
                r = requests.get(URL, timeout=5, verify=False)
                if r.status_code == 200:
                    status = r.json().get("status")
                    print("Status:", status)

                    if status == "1":
                        # 🔐 UI updates MUST be on main thread
                        root.after(0, on_payment_success)
                        break   # ✅ stop polling

            except Exception as e:
                print("Polling error:", e)

            time.sleep(1)   # ✅ very important


            time.sleep(1)
    def goToAvailability():
        pay_app.destroy()
        availability.open_availability(id)
    pay_app = CTk()
    pay_app.title("Blood Portal - Payment Secure")
    pay_app.resizable(False, False)
    set_appearance_mode("light")
    pay_app.configure(fg_color="#F1F5F9")

    # Window Centering
    width, height = 370, 670
    sw, sh = pay_app.winfo_screenwidth(), pay_app.winfo_screenheight()
    pay_app.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")

    # ================= LAYERING SYSTEM =================
    payment_layer = CTkFrame(pay_app, fg_color="#F1F5F9", corner_radius=0)
    success_layer = CTkFrame(pay_app, fg_color="#F1F5F9", corner_radius=0)
    
    for frame in (payment_layer, success_layer):
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # ================= 1. PAYMENT LAYER (Your Original Code) =================
    header = CTkFrame(payment_layer, fg_color="#D22B2B", height=160, corner_radius=0)
    header.pack(fill="x")

    CTkButton(header, text="←", font=("Poppins Bold", 22), text_color="white", 
              fg_color="#B22222", width=40, height=40, corner_radius=20,
              hover_color="#8B0000", command=goToAvailability).place(x=20, y=30)

    CTkLabel(header, text="SECURE CHECKOUT", font=("Poppins Bold", 10), text_color="#FFDADA").place(x=75, y=32)
    CTkLabel(header, text="Payment Gateway", font=("Poppins Bold", 19), text_color="white").place(x=75, y=48)

    pay_card = CTkFrame(payment_layer, fg_color="#FFFFFF", corner_radius=30, border_width=1, border_color="#E2E8F0")
    pay_card.place(relx=0.5, rely=0.56, anchor="center", relwidth=0.90, relheight=0.78)

    CTkLabel(pay_card, text="SUPPLEMENTARY FEE", font=("Poppins Bold", 11), text_color="#64748B").pack(pady=(25, 2))
    CTkLabel(pay_card, text="₹100.00", font=("Poppins Bold", 32), text_color="#0F172A").pack(pady=(0, 10))

    qr_container = CTkFrame(pay_card, fg_color="#FFFFFF", corner_radius=20, border_width=2, border_color="#E2E8F0", width=220, height=220)
    qr_container.pack(pady=10)
    show_img = generate_qr()
    qr_label = CTkLabel(qr_container, image=show_img, text="")
    qr_label.pack(pady=(10,0))
    qr_container.pack_propagate(False) 

    CTkLabel(pay_card, text="Scan the QR code to pay via UPI", font=("Poppins SemiBold", 12), text_color="#475569").pack(pady=10)

    details_frame = CTkFrame(pay_card, fg_color="#F1F5F9", corner_radius=12)
    details_frame.pack(fill="x", padx=25, pady=10)
    CTkLabel(details_frame, text="Service: Processing Fee", font=("Poppins Medium", 11), text_color="#64748B").pack(pady=(8, 2))
    CTkLabel(details_frame, text="Transaction ID: #PAY99201", font=("Poppins Medium", 11), text_color="#64748B").pack(pady=(0, 8))

    # Modified Button: Clicking this now triggers the success page
    btn_confirm = CTkButton(pay_card, text="I HAVE PAID", height=48, corner_radius=15, 
                            fg_color="#D22B2B", hover_color="#B22222", text_color="white",
                            font=("Poppins Bold", 13), command=lambda: success_layer.lift())
    btn_confirm.pack(side="bottom", fill="x", padx=25, pady=(5, 15))

    btn_cancel = CTkButton(pay_card, text="CANCEL PAYMENT", height=40, corner_radius=15, 
                            fg_color="transparent", hover_color="#F1F5F9", text_color="#64748B",
                            font=("Poppins Bold", 11), command=openAvailability)
    btn_cancel.pack(side="bottom", fill="x", padx=25, pady=0)

    # ================= 2. SUCCESS LAYER (The Transition) =================
    success_card = CTkFrame(success_layer, fg_color="#FFFFFF", corner_radius=35, border_width=1, border_color="#E2E8F0")
    success_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.7)

    icon_c = CTkFrame(success_card, fg_color="#DCFCE7", width=90, height=90, corner_radius=45)
    icon_c.pack(pady=(50, 20))
    icon_c.pack_propagate(False)
    CTkLabel(icon_c, text="✔", font=("Poppins Bold", 40), text_color="#166534").place(relx=0.5, rely=0.5, anchor="center")

    CTkLabel(success_card, text="Payment Successful!", font=("Poppins Bold", 20), text_color="#0F172A").pack(pady=10)
    CTkLabel(success_card, text="Transaction Approved.\nYou may now proceed.", 
             font=("Poppins Regular", 13), text_color="#64748B", justify="center").pack(pady=5)

    btn_proceed = CTkButton(success_card, text="GO TO WAITING ROOM", height=50, corner_radius=18, 
                            fg_color="#D22B2B", font=("Poppins Bold", 13), 
                            command=open_waiting)
    btn_proceed.pack(side="bottom", fill="x", padx=30, pady=(10, 40))

    payment_layer.lift()
    threading.Thread(
        target=checkStatus,
        args=(pay_app,),
        daemon=True).start()
    pay_app.mainloop()

if __name__ == "__main__":
    open_payment_gateway()