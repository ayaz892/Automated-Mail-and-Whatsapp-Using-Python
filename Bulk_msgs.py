import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import pywhatkit as kit
import threading
import time

class WhatsAppApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Message Sender")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0)

        # Message content variables
        self.message_var = tk.StringVar()

        # Create widgets
        ttk.Label(self.main_frame, text="Message:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.message_entry = ttk.Entry(self.main_frame, textvariable=self.message_var, width=50)
        self.message_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.main_frame, text="Attach CSV File", command=self.attach_csv_file).grid(row=1, column=0, padx=5, pady=5)
        self.file_label = ttk.Label(self.main_frame, text="No file attached")
        self.file_label.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.main_frame, text="Select Column:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.column_combobox = ttk.Combobox(self.main_frame, values=[], state="readonly", width=20)
        self.column_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.main_frame, text="Send Messages", command=self.send_messages).grid(row=3, column=1, padx=5, pady=10)

    def attach_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                # Read the CSV file
                self.df = pd.read_csv(file_path)

                # Update file label
                self.file_label.config(text=file_path.split("/")[-1])

                # Update column combobox with column names
                self.column_combobox['values'] = self.df.columns.tolist()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV file. Error: {str(e)}")

    def send_messages(self):
        message = self.message_var.get().strip()
        selected_column = self.column_combobox.get().strip()

        if not message:
            messagebox.showerror("Error", "Please enter a message.")
            return

        if not selected_column:
            messagebox.showerror("Error", "Please select a column.")
            return

        try:
            phone_numbers = self.df[selected_column].astype(str).tolist()

            if not phone_numbers:
                messagebox.showwarning("Warning", f"No phone numbers found in the selected column '{selected_column}'.")
                return

            # Disable send button during sending
            self.root.config(cursor="wait")
            self.root.update()

            # Send messages in a separate thread to avoid freezing the GUI
            threading.Thread(target=self.send_messages_thread, args=(phone_numbers, message)).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send messages. Error: {str(e)}")
            self.root.config(cursor="")
    
    def send_messages_thread(self, phone_numbers, message):
        try:
            for number in phone_numbers:
                if str(number).strip():  # Check if the number is not empty
                    kit.sendwhatmsg_instantly(f"+{number}", message)
                    time.sleep(10)  # Sleep for 10 seconds between messages to avoid being flagged as spam

            messagebox.showinfo("Success", "Messages sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send messages. Error: {str(e)}")
        finally:
            # Re-enable send button after sending
            self.root.config(cursor="")

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppApp(root)
    root.mainloop()
