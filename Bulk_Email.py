import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email credentials
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'qazizain2001@gmail.com'
EMAIL_PASSWORD = 'phfl eymw cfon iwcx'  # Replace with your App Password generated by Google

class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender App")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0)

        # Email content variables
        self.csv_file_path = ""
        self.selected_column = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.message_var = tk.StringVar()
        self.attachment_path = ""

        # Counters for successful and failed emails
        self.success_count = 0
        self.failed_emails = []

        # Create widgets
        ttk.Label(self.main_frame, text="Select CSV File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.csv_file_entry = ttk.Entry(self.main_frame, width=50, state='readonly')
        self.csv_file_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_csv_file).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Select Column:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.column_combobox = ttk.Combobox(self.main_frame, values=[], state="readonly", textvariable=self.selected_column, width=20)
        self.column_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Subject:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.subject_entry = ttk.Entry(self.main_frame, textvariable=self.subject_var, width=50)
        self.subject_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Message:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.message_text = tk.Text(self.main_frame, height=10, width=50)
        self.message_text.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.main_frame, text="Attach File", command=self.attach_file).grid(row=4, column=1, padx=5, pady=5)
        self.file_label = ttk.Label(self.main_frame, text="No file attached")
        self.file_label.grid(row=4, column=2, padx=5, pady=5)

        ttk.Button(self.main_frame, text="Send Emails", command=self.send_emails).grid(row=5, column=1, padx=5, pady=10)

        # Label to display successful count
        self.success_label = ttk.Label(self.main_frame, text="Successfully sent: 0")
        self.success_label.grid(row=6, column=1, padx=5, pady=5)

        # Text widget to display failed emails
        ttk.Label(self.main_frame, text="Failed Emails:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.failed_text = tk.Text(self.main_frame, height=5, width=50)
        self.failed_text.grid(row=7, column=1, padx=5, pady=5, columnspan=2)

    def browse_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_file_path = file_path
            self.csv_file_entry.config(state='normal')
            self.csv_file_entry.delete(0, tk.END)
            self.csv_file_entry.insert(0, file_path)
            self.csv_file_entry.config(state='readonly')

            # Update column combobox with column names from the CSV file
            try:
                df = pd.read_csv(file_path)
                self.column_combobox['values'] = df.columns.tolist()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV file. Error: {str(e)}")

    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.attachment_path = file_path
            self.file_label.config(text=file_path.split("/")[-1])  # Display only the file name

    def send_emails(self):
        csv_file_path = self.csv_file_entry.get()
        selected_column = self.selected_column.get()
        subject = self.subject_var.get()
        message = self.message_text.get("1.0", tk.END)  # Retrieve message from Text widget

        if not csv_file_path:
            messagebox.showerror("Error", "Please select a CSV file.")
            return

        if not selected_column:
            messagebox.showerror("Error", "Please select a column.")
            return

        self.success_count = 0
        self.failed_emails = []

        try:
            # Read the CSV file
            email_list = pd.read_csv(csv_file_path)

            # Remove duplicates
            email_list = email_list.drop_duplicates(subset=selected_column)

            # Replace NaN values with empty strings
            email_list[selected_column] = email_list[selected_column].fillna('')

            # Email content
            for index, row in email_list.iterrows():
                to_address = row[selected_column]

                # Set up the server
                server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
                server.starttls()
                server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

                # Create the email
                msg = MIMEMultipart()
                msg['From'] = EMAIL_USERNAME
                msg['To'] = to_address
                msg['Subject'] = subject

                # Attach message
                msg.attach(MIMEText(message, 'plain'))

                # Attach file if provided
                if self.attachment_path:
                    with open(self.attachment_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename= {self.attachment_path}')
                        msg.attach(part)

                try:
                    # Send the email
                    server.sendmail(EMAIL_USERNAME, to_address, msg.as_string())
                    self.success_count += 1
                    self.success_label.config(text=f"Successfully sent: {self.success_count}")
                except Exception as e:
                    self.failed_emails.append(to_address)

                # Disconnect from the server
                server.quit()

            # Display failed emails in the text widget
            if self.failed_emails:
                self.failed_text.delete("1.0", tk.END)
                self.failed_text.insert(tk.END, "\n".join(self.failed_emails))

            messagebox.showinfo("Success", "Emails sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send emails. Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()