import tkinter as tk
from tkinter import messagebox, scrolledtext
import instaloader

root = None

def fetch_profile_info(username, password, output_text, loading_label):
    global root
    if not username:
        messagebox.showerror("Error", "Username cannot be empty.")
        return

    L = instaloader.Instaloader()

    try:
        loading_label.config(text="Loading... Please wait")
        root.update_idletasks()

        L.login(username, password)

        profile = instaloader.Profile.from_username(L.context, username)
        
        info = (
            f"Username: {profile.username}\n"
            f"Number of Posts: {profile.mediacount}\n"
            f"Followers Count: {profile.followers}\n"
            f"Following Count: {profile.followees}\n"
            f"Bio: {profile.biography}\n"
            f"External URL: {profile.external_url}\n"
        )
        
        L.download_profile(profile.username, profile_pic_only=False)

        followers = profile.get_followers()
        followers_list = [follower.username for follower in followers]

        followees = profile.get_followees()
        followees_list = [followee.username for followee in followees]

        with open('followers_list.txt', 'w') as f:
            for follower in followers_list:
                f.write(f"{follower}\n")

        with open('followees_list.txt', 'w') as f:
            for followee in followees_list:
                f.write(f"{followee}\n")

        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, info)
        output_text.insert(tk.END, "\nFollowers and following lists have been saved to files.")
        output_text.insert(tk.END, "\nPosts have been saved.")
    
    except instaloader.exceptions.ProfileNotExistsException:
        messagebox.showerror("Error", "Profile does not exist.")
    except instaloader.exceptions.ConnectionException:
        messagebox.showerror("Error", "Invalid username or network issue.")
    except instaloader.exceptions.LoginRequiredException:
        messagebox.showerror("Error", "Login required or login credentials are incorrect.")
    except instaloader.exceptions.InstaloaderException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        loading_label.config(text="")

def option_two(username, output_text, loading_label):
    global root
    if not username:
        messagebox.showerror("Error", "Username cannot be empty.")
        return

    L = instaloader.Instaloader()

    try:
        loading_label.config(text="Loading... Please wait")
        root.update_idletasks()

        profile = instaloader.Profile.from_username(L.context, username)

        info = (
            f"Username: {profile.username}\n"
            f"Number of Posts: {profile.mediacount}\n"
            f"Followers Count: {profile.followers}\n"
            f"Following Count: {profile.followees}\n"
            f"Bio: {profile.biography}\n"
            f"External URL: {profile.external_url}\n"
        )

        L.download_profile(profile.username, profile_pic_only=False)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, info)
        output_text.insert(tk.END, "\nPosts have been saved.")
    
    except instaloader.exceptions.ProfileNotExistsException:
        messagebox.showerror("Error", "Profile does not exist.")
    except instaloader.exceptions.ConnectionException:
        messagebox.showerror("Error", "Network issue or Instagram is down.")
    except instaloader.exceptions.InstaloaderException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        loading_label.config(text="")

def main():
    global root
    def on_submit():
        username = username_entry.get().strip()
        password = password_entry.get()
        choice = choice_var.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        if choice == '1':
            if not password:
                messagebox.showerror("Error", "Password cannot be empty when both username and password are required.")
                return
            fetch_profile_info(username, password, output_text, loading_label)
        elif choice == '2':
            option_two(username, output_text, loading_label)
        else:
            messagebox.showerror("Error", "Invalid choice. Please enter 1 or 2.")

    def update_ui(*args):
        if choice_var.get() == '1':
            password_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
            password_entry.grid(row=5, column=1, padx=10, pady=10)
        else:
            password_label.grid_forget()
            password_entry.grid_forget()

    root = tk.Tk()
    root.title("Social Media Data Extractor")
    root.geometry("665x700") 

    root.configure(bg="#f0f0f0")
    label_font = ("Helvetica", 12)
    entry_font = ("Helvetica", 12)
    button_font = ("Helvetica", 12, "bold")
    button_bg = "#4CAF50"
    button_fg = "#ffffff"
    heading_font = ("Helvetica", 16, "bold")
    loading_font = ("Helvetica", 12, "italic")
    text_bg = "#ffffff"

    tk.Label(root, text="Social Media Data Extractor", font=heading_font, bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=(20, 10))

    tk.Label(root, text="BY: TEAM CAPSLOCK", font=("Helvetica", 10), bg="#f0f0f0", fg="#04aa6d").grid(row=1, column=0, columnspan=2, pady=(0, 10))

    tk.Label(root, text="Choose an option:", font=label_font, bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    choice_var = tk.StringVar(value='1')
    tk.Radiobutton(root, text="Both username & password", variable=choice_var, value='1', font=label_font, bg="#f0f0f0", command=update_ui).grid(row=2, column=1, padx=10, pady=10, sticky="w")
    tk.Radiobutton(root, text="Only username", variable=choice_var, value='2', font=label_font, bg="#f0f0f0", command=update_ui).grid(row=3, column=1, padx=10, pady=10, sticky="w")

    tk.Label(root, text="Username:", font=label_font, bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    username_entry = tk.Entry(root, font=entry_font, bd=2, relief="solid")
    username_entry.grid(row=4, column=1, padx=10, pady=10)

    password_label = tk.Label(root, text="Password:", font=label_font, bg="#f0f0f0")
    password_entry = tk.Entry(root, show='*', font=entry_font, bd=2, relief="solid")

    button_frame = tk.Frame(root, bg="#f0f0f0")
    submit_button = tk.Button(button_frame, text="Submit", command=on_submit, font=button_font, bg=button_bg, fg=button_fg, bd=2, relief="raised")
    submit_button.pack(side=tk.LEFT, padx=10)

    loading_label = tk.Label(button_frame, text="", font=loading_font, bg="#f0f0f0", fg="#FF5722")
    loading_label.pack(side=tk.LEFT, padx=10)

    button_frame.grid(row=6, column=0, columnspan=2, pady=20)

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=entry_font, bd=2, relief="solid")
    output_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    update_ui()

    root.mainloop()

if __name__ == "__main__":
    main()
