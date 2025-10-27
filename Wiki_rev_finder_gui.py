import tkinter as tk
from tkinter import ttk, messagebox
import requests
from Wiki_rev_finder import fetch_rev

def process_response_gui(data, text_widget):
    text_widget.delete(1.0, tk.END)
    query = data.get("query", {})

   
    redirected_to = None
    if "redirects" in query:
        redirected_to = query["redirects"][0]["to"]
        text_widget.insert(tk.END, f"Note: Page was redirected to '{redirected_to}'\n\n")

  
    pages = query.get("pages", {})
    if not pages:
        text_widget.insert(tk.END, "Error: No pages found in the response.\n")
        return
    page = next(iter(pages.values()))
    if "missing" in page:
        text_widget.insert(tk.END, "Error: The requested page does not exist.\n")
        return

    
    revisions = page.get("revisions", [])
    if not revisions:
        text_widget.insert(tk.END, "No revisions found for this page.\n")
        return

    text_widget.insert(tk.END, f"Found {len(revisions)} revisions:\n\n")
    for rev in revisions:
        timestamp = rev.get("timestamp")
        user = rev.get("user")
        if timestamp and user:
            text_widget.insert(tk.END, f"{timestamp} — {user}\n")

def fetch_and_display(article_entry, text_widget):
    article_name = article_entry.get().strip()
    if not article_name:
        messagebox.showerror("Error", "Please enter an article name.")
        return
    try:
        data = fetch_rev(article_name)
        process_response_gui(data, text_widget)
    except requests.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to fetch data:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

def main_gui():
    root = tk.Tk()
    root.title("Wikipedia Revision Finder")

    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0, column=0, sticky="nsew")

    ttk.Label(frame, text="Enter Article Name:").grid(row=0, column=0, sticky="w")
    article_entry = ttk.Entry(frame, width=50)
    article_entry.grid(row=0, column=1, padx=5)

    text_widget = tk.Text(frame, width=80, height=25, wrap="word")
    text_widget.grid(row=2, column=0, columnspan=2, pady=10)

    fetch_button = ttk.Button(
        frame,
        text="Fetch Revisions",
        command=lambda: fetch_and_display(article_entry, text_widget)
    )
    fetch_button.grid(row=1, column=0, columnspan=2, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
