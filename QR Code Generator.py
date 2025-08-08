import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

import smtplib
from email.message import EmailMessage

def send_email_with_qr_code(to_email, file_name):
    try:
        msg = EmailMessage()
        msg['Subject'] = "QR code"
        msg['From'] = "chandrusns2006@gmail.com"
        msg['To'] = to_email
        msg.set_content("Your QR code")

        with open(file_name, 'rb') as img:
            img_data = img.read()
            img_name = file_name.split("/")[-1]
            msg.add_attachment(img_data, maintype='image', subtype='png', filename=img_name)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("chandrusns2006@gmail.com","yrjh rxgu sbfo gmvr")
                smtp.send_message(msg)
            messagebox.showerror("Success", f"QR code has been sent successfully")
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")
        
def create_qr_code(data, file_name, size=10, color='black', bg_color='white', logo=None):
    try:
        qr = qrcode.QRCode(
            version=1,  
            error_correction=qrcode.constants.ERROR_CORRECT_H,  
            box_size=size,  
            border=4,  
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=color, back_color=bg_color)
        if logo:
            embed_logo(img, logo)
        img.save(file_name)
        return img
    except Exception as e:
        print(f"Error generating QR code: {e}")
        messagebox.showerror("Error", f"Error generating QR code: {e}")

def embed_logo(qr_image, logo_path):
    try:
        logo = Image.open(logo_path)
        qr_width, qr_height = qr_image.size
        logo_size = qr_width // 5  
        logo = logo.resize((logo_size, logo_size))
        logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_image.paste(logo, logo_position, logo.convert('RGBA')) 
    except Exception as e:
        print(f"Error embedding logo: {e}")
        messagebox.showerror("Error", "Error embedding logo")

def validate_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return True
    else:
        return True

def validate_email(email):
    if '@' in email and '.' in email:
        return True
    return False

def select_logo():
    logo_path = filedialog.askopenfilename(title="Select Logo", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if logo_path:
        logo_entry.delete(0, tk.END) 
        logo_entry.insert(0, logo_path)  

def generate_qr_code():
    data_type = data_type_var.get()
    file_name = file_name_entry.get() + '.png'
    to_email=email_entry1.get()
    
    size = int(size_entry.get())
    color = color_entry.get() or 'black'
    bg_color = bg_color_entry.get() or 'white'
    logo = logo_entry.get() if logo_entry.get() else None
    data = ""
    if data_type == "Text":
        data = text_entry.get()
    elif data_type == "URL":
        url = url_entry.get()
        if not url or not validate_url(url):
            messagebox.showerror("Error", "Invalid URL. Please enter a valid URL starting with 'http://' or 'https://'.")
            return
        data = url
    elif data_type == "Email":
        email = email_entry.get()
        if not email or not validate_email(email):
            messagebox.showerror("Error", "Invalid email address.")
            return
        data = f"mailto:{email}"
    elif data_type == "Contact":
        name = name_entry.get()
        phone = phone_entry.get()
        email = contact_email_entry.get()
        if not name or not phone or not email:
            messagebox.showerror("Error", "All fields are required for contact info.")
            return
        data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"

    img = create_qr_code(data, file_name, size, color, bg_color, logo)

    if img:
        img.thumbnail((250, 250))  
        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk
        qr_label.place(x=frame.winfo_width() - 260, y=20)

    messagebox.showinfo("Success", f"QR Code saved as {file_name}")
    send_email_with_qr_code(to_email, file_name)    
root = tk.Tk()
root.title("QR Code Generator")

root.attributes('-fullscreen', True)
root.configure(bg="#4ADEDE")  
root.bind("<Escape>", lambda event: root.destroy())
title_font = ('Gvtime', 40, 'bold')
label_font = ('Helvetica', 14, 'bold')
entry_font = ('Helvetica', 12)
button_font = ('Helvetica', 12, 'bold')
frame = tk.Frame(root, bg="#4ADEDE") 
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
title_label = tk.Label(frame, text="QR Code Generator", font= title_font, fg="#1C1DAB", bg="#ADC6E5")
title_label.grid(row=0, column=1, columnspan=3, pady=20)
data_type_var = tk.StringVar(value="Contact")
data_type_label = tk.Label(frame, text="Select Data Type:", font=label_font, bg='#4ADEDE', anchor='w')
data_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
data_type_dropdown = ttk.Combobox(frame, textvariable=data_type_var, values=["Contact","URL","Email", "Text"], font=entry_font, width=20)
data_type_dropdown.grid(row=1, column=1, padx=10, pady=5)
text_label = tk.Label(frame, text="Enter Text:", font=label_font, bg='#4ADEDE', anchor='w')
text_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
text_entry = tk.Entry(frame, font=entry_font, width=40)
text_entry.grid(row=2, column=1, padx=10, pady=5)
text_entry.grid_remove()  
url_label = tk.Label(frame, text="Enter URL:", font=label_font, bg='#4ADEDE', anchor='w')
url_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
url_entry = tk.Entry(frame, font=entry_font, width=40)
url_entry.grid(row=3, column=1, padx=10, pady=5)
url_entry.grid_remove() 
email_label = tk.Label(frame, text="Enter Email:", font=label_font, bg='#4ADEDE', anchor='w')
email_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
email_entry = tk.Entry(frame, font=entry_font, width=40)
email_entry.grid(row=4, column=1, padx=10, pady=5)
email_entry.grid_remove()  
name_label = tk.Label(frame, text="Enter Name:", font=label_font, bg='#4ADEDE', anchor='w')
name_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(frame, font=entry_font, width=40)
name_entry.grid(row=5, column=1, padx=10, pady=5)
name_entry.grid_remove() 
phone_label = tk.Label(frame, text="Enter Phone Number:", font=label_font, bg='#4ADEDE', anchor='w')
phone_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
phone_entry = tk.Entry(frame, font=entry_font, width=40)
phone_entry.grid(row=6, column=1, padx=10, pady=5)
phone_entry.grid_remove() 
contact_email_label = tk.Label(frame, text="Enter Contact Email:", font=label_font, bg='#4ADEDE', anchor='w')
contact_email_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
contact_email_entry = tk.Entry(frame, font=entry_font, width=40)
contact_email_entry.grid(row=7, column=1, padx=10, pady=5)
contact_email_entry.grid_remove() 
file_name_label = tk.Label(frame, text="File name (without extension):", font=label_font, bg='#4ADEDE', anchor='w')
file_name_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
file_name_entry = tk.Entry(frame, font=entry_font, width=40)
file_name_entry.grid(row=8, column=1, padx=10, pady=5)
size_label = tk.Label(frame, text="QR Code Size (e.g., 10):", font=label_font, bg='#4ADEDE', anchor='w')
size_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
size_entry = tk.Entry(frame, font=entry_font, width=10)
size_entry.grid(row=9, column=1, padx=10, pady=5)
size_entry.insert(0, '10') 
color_label = tk.Label(frame, text="Foreground color (default black):", font=label_font, bg='#4ADEDE', anchor='w')
color_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")
color_entry = tk.Entry(frame, font=entry_font, width=40)
color_entry.grid(row=10, column=1, padx=10, pady=5)
bg_color_label = tk.Label(frame, text="Background color (default white):", font=label_font, bg='#4ADEDE', anchor='w')
bg_color_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")
bg_color_entry = tk.Entry(frame, font=entry_font, width=40)
bg_color_entry.grid(row=11, column=1, padx=10, pady=5)
logo_label = tk.Label(frame, text="Logo (optional):", font=label_font, bg='#4ADEDE', anchor='w')
logo_label.grid(row=12, column=0, padx=10, pady=5, sticky="w")
logo_entry = tk.Entry(frame, font=entry_font, width=40)
logo_entry.grid(row=12, column=1, padx=10, pady=5)
logo_button = tk.Button(frame, text="Select Logo", command=select_logo, font=button_font, bg="#4CAF50", fg="white", relief="flat")
logo_button.grid(row=12, column=2, padx=10, pady=5)
email_label1 = tk.Label(frame, text="Send QR to Email (Optional):", font=label_font, bg="#4ADEDE")
email_entry1 = tk.Entry(frame, font=entry_font,width=40)
email_label1.grid(row=13, column=0, padx=10, pady=5, sticky="w")
email_entry1.grid(row=13, column=1, padx=10, pady=5)
generate_button = tk.Button(frame, text="Generate QR Code", command=generate_qr_code, font=button_font, bg="#4CAF50", fg="white", relief="flat")
generate_button.grid(row=14, column=0, columnspan=3, pady=20)
qr_label = tk.Label(frame, bg='#ff999f')
qr_label.place(x=frame.winfo_width() - 260, y=20)

def update_ui():
    data_type = data_type_var.get()
    text_label.grid_remove()
    text_entry.grid_remove()
    url_label.grid_remove()
    url_entry.grid_remove()
    email_label.grid_remove()
    email_entry.grid_remove()
    name_label.grid_remove()
    name_entry.grid_remove()
    phone_label.grid_remove()
    phone_entry.grid_remove()
    contact_email_label.grid_remove()
    contact_email_entry.grid_remove()

    if data_type == "Text":
        text_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        text_entry.grid(row=2, column=1, padx=10, pady=5)
        email_entry1.grid(row=13, column=1, padx=10, pady=5)
    elif data_type == "URL":
        url_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        url_entry.grid(row=3, column=1, padx=10, pady=5)
        email_entry1.grid(row=13, column=1, padx=10, pady=5)
    elif data_type == "Email":
        email_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        email_entry.grid(row=4, column=1, padx=10, pady=5)
        email_entry1.grid(row=13, column=1, padx=10, pady=5)
    elif data_type == "Contact":
        name_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        name_entry.grid(row=5, column=1, padx=10, pady=5)
        phone_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        phone_entry.grid(row=6, column=1, padx=10, pady=5)
        contact_email_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        contact_email_entry.grid(row=7, column=1, padx=10, pady=5)
        email_entry1.grid(row=13, column=1, padx=10, pady=5)

data_type_var.trace("w", lambda *args: update_ui())
root.mainloop()
