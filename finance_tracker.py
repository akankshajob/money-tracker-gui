#!/usr/bin/env python3
"""
Personal Finance Tracker - Modern GUI Version
A beautiful desktop application to track personal expenses and income.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
from typing import Dict, List
import os
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from matplotlib.figure import Figure

class ModernFinanceTracker:
    def __init__(self):
        self.data_file = "finance_data.json"
        self.transactions = self.load_data()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("💰 Personal Finance Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0D1117')  # Dark GitHub-like theme
        
        # Color scheme
        self.colors = {
            'bg_primary': '#0D1117',
            'bg_secondary': '#161B22',
            'bg_tertiary': '#21262D',
            'accent': '#58A6FF',
            'success': '#3FB950',
            'warning': '#D29922',
            'danger': '#F85149',
            'text_primary': '#F0F6FC',
            'text_secondary': '#8B949E',
            'border': '#30363D'
        }
        
        self.setup_styles()
        self.create_widgets()
        self.update_dashboard()
    
    def setup_styles(self):
        """Setup custom styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 12))
        
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Modern.TButton',
                 background=[('active', '#4F94D4'),
                           ('pressed', '#3D7CBF')])
    
    def load_data(self) -> List[Dict]:
        """Load transaction data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_data(self) -> None:
        """Save transaction data to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Left panel - Dashboard
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_primary'])
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_dashboard(left_panel)
        
        # Right panel - Controls
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_primary'], width=350)
        right_panel.pack(side='right', fill='y', padx=(10, 0))
        right_panel.pack_propagate(False)
        
        self.create_controls(right_panel)
    
    def create_header(self, parent):
        """Create the application header."""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x')
        
        title_label = ttk.Label(header_frame, text="💰 Personal Finance Tracker", 
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        subtitle_label = ttk.Label(header_frame, text="Track your money with style ✨", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(side='left', padx=(20, 0))
    
    def create_dashboard(self, parent):
        """Create the main dashboard area."""
        # Balance cards
        cards_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        cards_frame.pack(fill='x', pady=(0, 20))
        
        self.balance_card = self.create_stat_card(cards_frame, "Balance", "$0.00", self.colors['accent'])
        self.income_card = self.create_stat_card(cards_frame, "Income", "$0.00", self.colors['success'])
        self.expense_card = self.create_stat_card(cards_frame, "Expenses", "$0.00", self.colors['danger'])
        
        # Chart area
        chart_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', bd=1)
        chart_frame.pack(fill='both', expand=True)
        
        chart_title = tk.Label(chart_frame, text="📊 Spending by Category", 
                              bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                              font=('Segoe UI', 14, 'bold'))
        chart_title.pack(pady=10)
        
        self.create_chart(chart_frame)
    
    def create_stat_card(self, parent, title, value, color):
        """Create a statistics card."""
        card = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', bd=1)
        card.pack(side='left', fill='x', expand=True, padx=5)
        
        title_label = tk.Label(card, text=title, bg=self.colors['bg_secondary'], 
                              fg=self.colors['text_secondary'], font=('Segoe UI', 10))
        title_label.pack(pady=(15, 5))
        
        value_label = tk.Label(card, text=value, bg=self.colors['bg_secondary'], 
                              fg=color, font=('Segoe UI', 20, 'bold'))
        value_label.pack(pady=(0, 15))
        
        return value_label
    
    def create_chart(self, parent):
        """Create the expense chart."""
        fig = Figure(figsize=(8, 5), facecolor=self.colors['bg_secondary'])
        fig.patch.set_facecolor(self.colors['bg_secondary'])
        
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor(self.colors['bg_secondary'])
        
        # Initial empty chart
        self.ax.text(0.5, 0.5, '📈 Add some transactions to see your spending patterns!', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=self.ax.transAxes, fontsize=12, 
                    color=self.colors['text_secondary'])
        
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        self.canvas = FigureCanvasTkAgg(fig, parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_controls(self, parent):
        """Create the control panel."""
        # Add Transaction Section
        add_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', bd=1)
        add_frame.pack(fill='x', pady=(0, 20))
        
        add_title = tk.Label(add_frame, text="➕ Add Transaction", 
                            bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                            font=('Segoe UI', 14, 'bold'))
        add_title.pack(pady=15)
        
        # Transaction type
        type_frame = tk.Frame(add_frame, bg=self.colors['bg_secondary'])
        type_frame.pack(fill='x', padx=15, pady=5)
        
        self.transaction_type = tk.StringVar(value="expense")
        
        income_btn = tk.Radiobutton(type_frame, text="💰 Income", variable=self.transaction_type, 
                                   value="income", bg=self.colors['bg_secondary'], 
                                   fg=self.colors['text_primary'], selectcolor=self.colors['bg_tertiary'],
                                   activebackground=self.colors['bg_secondary'], font=('Segoe UI', 10))
        income_btn.pack(side='left')
        
        expense_btn = tk.Radiobutton(type_frame, text="💸 Expense", variable=self.transaction_type, 
                                    value="expense", bg=self.colors['bg_secondary'], 
                                    fg=self.colors['text_primary'], selectcolor=self.colors['bg_tertiary'],
                                    activebackground=self.colors['bg_secondary'], font=('Segoe UI', 10))
        expense_btn.pack(side='right')
        
        # Amount input
        self.create_input_field(add_frame, "Amount ($)", "amount_entry")
        
        # Category input
        self.create_input_field(add_frame, "Category", "category_entry")
        
        # Description input
        self.create_input_field(add_frame, "Description", "description_entry")
        
        # Add button
        add_btn = tk.Button(add_frame, text="✨ Add Transaction", 
                           bg=self.colors['accent'], fg='white', font=('Segoe UI', 11, 'bold'),
                           relief='flat', cursor='hand2', command=self.add_transaction)
        add_btn.pack(pady=15, padx=15, fill='x')
        
        # Recent Transactions
        recent_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', bd=1)
        recent_frame.pack(fill='both', expand=True)
        
        recent_title = tk.Label(recent_frame, text="📝 Recent Transactions", 
                               bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                               font=('Segoe UI', 14, 'bold'))
        recent_title.pack(pady=15)
        
        # Transactions list
        list_frame = tk.Frame(recent_frame, bg=self.colors['bg_secondary'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.transactions_listbox = tk.Listbox(list_frame, bg=self.colors['bg_tertiary'], 
                                              fg=self.colors['text_primary'], 
                                              selectbackground=self.colors['accent'],
                                              font=('Consolas', 9), relief='flat',
                                              borderwidth=0, highlightthickness=0)
        self.transactions_listbox.pack(fill='both', expand=True)
    
    def create_input_field(self, parent, label, attr_name):
        """Create a labeled input field."""
        label_widget = tk.Label(parent, text=label, bg=self.colors['bg_secondary'], 
                               fg=self.colors['text_secondary'], font=('Segoe UI', 10))
        label_widget.pack(anchor='w', padx=15, pady=(10, 0))
        
        entry = tk.Entry(parent, bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                        font=('Segoe UI', 11), relief='flat', bd=5)
        entry.pack(fill='x', padx=15, pady=(5, 0))
        
        setattr(self, attr_name, entry)
    
    def add_transaction(self):
        """Add a new transaction."""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get().strip()
            description = self.description_entry.get().strip()
            transaction_type = self.transaction_type.get()
            
            if not category or not description:
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            transaction = {
                "id": len(self.transactions) + 1,
                "date": datetime.datetime.now().isoformat(),
                "amount": abs(amount),
                "category": category.lower(),
                "description": description,
                "type": transaction_type.lower()
            }
            
            self.transactions.append(transaction)
            self.save_data()
            
            # Clear inputs
            self.amount_entry.delete(0, 'end')
            self.category_entry.delete(0, 'end')
            self.description_entry.delete(0, 'end')
            
            # Update dashboard
            self.update_dashboard()
            
            # Show success message
            messagebox.showinfo("Success", f"✅ {transaction_type.title()} added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
    
    def update_dashboard(self):
        """Update all dashboard elements."""
        # Calculate totals
        income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        balance = income - expenses
        
        # Update stat cards
        self.balance_card.config(text=f"${balance:.2f}")
        self.income_card.config(text=f"${income:.2f}")
        self.expense_card.config(text=f"${expenses:.2f}")
        
        # Update chart
        self.update_chart()
        
        # Update recent transactions
        self.update_recent_transactions()
    
    def update_chart(self):
        """Update the expense chart."""
        expense_categories = defaultdict(float)
        for transaction in self.transactions:
            if transaction["type"] == "expense":
                expense_categories[transaction["category"]] += transaction["amount"]
        
        self.ax.clear()
        self.ax.set_facecolor(self.colors['bg_secondary'])
        
        if expense_categories:
            # Create a modern donut chart
            categories = list(expense_categories.keys())
            values = list(expense_categories.values())
            
            # Color palette
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            
            wedges, texts, autotexts = self.ax.pie(values, labels=categories, autopct='%1.1f%%',
                                                  colors=colors[:len(categories)], startangle=90,
                                                  pctdistance=0.85)
            
            # Create donut effect
            centre_circle = plt.Circle((0,0), 0.70, fc=self.colors['bg_secondary'])
            self.ax.add_artist(centre_circle)
            
            # Style the text
            for text in texts:
                text.set_color(self.colors['text_primary'])
                text.set_fontsize(10)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            self.ax.set_title('', color=self.colors['text_primary'])
        else:
            self.ax.text(0.5, 0.5, '📈 Add some expenses to see your spending patterns!', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=12, 
                        color=self.colors['text_secondary'])
        
        self.canvas.draw()
    
    def update_recent_transactions(self):
        """Update the recent transactions list."""
        self.transactions_listbox.delete(0, 'end')
        
        recent = sorted(self.transactions, key=lambda x: x["date"], reverse=True)[:10]
        
        for transaction in recent:
            date = datetime.datetime.fromisoformat(transaction["date"]).strftime("%m/%d")
            emoji = "💰" if transaction["type"] == "income" else "💸"
            amount = f"${transaction['amount']:.2f}"
            category = transaction['category'][:10]
            description = transaction['description'][:15]
            
            line = f"{emoji} {date} {amount:>8} {category:<10} {description}"
            self.transactions_listbox.insert('end', line)
    
    def run(self):
        """Start the application."""
        self.root.mainloop()

def main():
    """Main function to run the application."""
    app = ModernFinanceTracker()
    app.run()

if __name__ == "__main__":
    main()