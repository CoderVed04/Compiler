import tkinter as tk
from tkinter import messagebox, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from leftrecursion import LeftRecursionEliminator
from leftfactor import left_factor

def process_grammar(option):
    user_input = grammar_input.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showerror("Error", "Please enter a grammar.")
        return
    
    grammar = {}
    try:
        for line in user_input.split("\n"):
            parts = line.split("->")
            if len(parts) != 2:
                raise ValueError("Invalid format. Use 'A -> B | C'")
            non_terminal = parts[0].strip()
            productions = [p.strip() for p in parts[1].split("|")]
            grammar[non_terminal] = productions
    except Exception as e:
        messagebox.showerror("Error", f"Invalid grammar format: {e}")
        return
    
    if option == "recursion":
        eliminator = LeftRecursionEliminator(grammar)
        result = eliminator.eliminate_left_recursion()
    else:
        result = left_factor(grammar)
    
    output_text.delete("1.0", tk.END)
    for nt, rules in result.items():
        output_text.insert(tk.END, f"{nt} -> {' | '.join(rules)}\n")

def clear_text():
    grammar_input.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

# Main Window
root = ttk.Window(themename="darkly")  # Sleek dark theme
root.title("Grammar Transformation Tool")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="#2C2F33")  # Darker background

# Title Label
title_label = ttk.Label(root, text="Grammar Transformation Tool", font=("Arial", 20, "bold"), bootstyle="info")
title_label.pack(pady=15)

# Grammar Input
input_label = ttk.Label(root, text="Enter Grammar:", font=("Arial", 12, "bold"), background="#2C2F33", foreground="white")
input_label.pack(anchor="w", padx=20)

grammar_input = scrolledtext.ScrolledText(root, height=5, width=75, font=("Consolas", 11), bg="#23272A", fg="white", insertbackground="white")
grammar_input.pack(padx=20, pady=5)

# Buttons
button_frame = ttk.Frame(root, bootstyle="secondary")
button_frame.pack(pady=15)

recursion_btn = ttk.Button(button_frame, text="Eliminate Left Recursion", bootstyle="success-outline", command=lambda: process_grammar("recursion"))
factor_btn = ttk.Button(button_frame, text="Left Factor", bootstyle="info-outline", command=lambda: process_grammar("factor"))
clear_btn = ttk.Button(button_frame, text="Clear", bootstyle="danger-outline", command=clear_text)

recursion_btn.grid(row=0, column=0, padx=12, pady=5, ipadx=10, ipady=3)
factor_btn.grid(row=0, column=1, padx=12, pady=5, ipadx=10, ipady=3)
clear_btn.grid(row=0, column=2, padx=12, pady=5, ipadx=10, ipady=3)

# Output Section
output_label = ttk.Label(root, text="Transformed Grammar:", font=("Arial", 12, "bold"), background="#2C2F33", foreground="white")
output_label.pack(anchor="w", padx=20)

output_text = scrolledtext.ScrolledText(root, height=8, width=75, font=("Consolas", 11), bg="#23272A", fg="white", insertbackground="white")
output_text.pack(padx=20, pady=5)

# Run App
root.mainloop()
