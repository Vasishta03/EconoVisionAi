#!/usr/bin/env python3
"""
EconoVisionAI - Economic Development Data Explorer
A simple GUI application to search economic development data from OECD-style datasets
"""

import customtkinter as ctk
import pandas as pd
import json
import os
import glob
from tkinter import messagebox
import sys

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class EconoVisionAI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("EconoVisionAI - Economic Development Data Explorer")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Initialize data storage
        self.csv_data = {}
        self.report_data = {}

        # Load data on startup
        self.load_data()

        # Create GUI
        self.create_widgets()

    def load_data(self):
        """Load CSV and report data from files"""
        try:
            # Load CSV files from data folder
            if os.path.exists("data"):
                csv_files = glob.glob("data/*.csv")
                for csv_file in csv_files:
                    try:
                        df = pd.read_csv(csv_file)
                        filename = os.path.basename(csv_file)
                        self.csv_data[filename] = df
                        print(f"Loaded CSV: {filename} with {len(df)} rows")
                    except Exception as e:
                        print(f"Error loading {csv_file}: {e}")

            # Load report files from reports folder
            if os.path.exists("reports"):
                # Load .txt files
                txt_files = glob.glob("reports/*.txt")
                for txt_file in txt_files:
                    try:
                        with open(txt_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        filename = os.path.basename(txt_file)
                        self.report_data[filename] = content
                        print(f"Loaded report: {filename}")
                    except Exception as e:
                        print(f"Error loading {txt_file}: {e}")

                # Load .json files
                json_files = glob.glob("reports/*.json")
                for json_file in json_files:
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            content = json.load(f)
                        filename = os.path.basename(json_file)
                        self.report_data[filename] = content
                        print(f"Loaded JSON report: {filename}")
                    except Exception as e:
                        print(f"Error loading {json_file}: {e}")

        except Exception as e:
            print(f"Error in load_data: {e}")

    def create_widgets(self):
        """Create and arrange GUI widgets"""

        # Main title
        title_label = ctk.CTkLabel(
            self, 
            text="🌍 EconoVisionAI", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        subtitle_label = ctk.CTkLabel(
            self, 
            text="Economic Development Data Explorer", 
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(pady=(0, 20))

        # Search frame
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(pady=10, padx=20, fill="x")

        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter keywords (e.g., 'GDP India', 'education Brazil', 'inequality')",
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.search_entry.pack(pady=15, padx=15, fill="x")

        # Bind Enter key to search
        self.search_entry.bind("<Return>", lambda event: self.search_data())

        # Button frame
        button_frame = ctk.CTkFrame(search_frame)
        button_frame.pack(pady=(0, 15), padx=15, fill="x")

        # Search buttons
        search_data_btn = ctk.CTkButton(
            button_frame,
            text="🔍 Search Data (CSV)",
            command=self.search_data,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35
        )
        search_data_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)

        search_reports_btn = ctk.CTkButton(
            button_frame,
            text="📄 Search Reports",
            command=self.search_reports,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35
        )
        search_reports_btn.pack(side="left", padx=5, fill="x", expand=True)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear Results",
            command=self.clear_results,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=35,
            fg_color="gray",
            hover_color="darkgray"
        )
        clear_btn.pack(side="right", padx=(10, 0), fill="x", expand=True)

        # Results frame
        results_frame = ctk.CTkFrame(self)
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Results label
        self.results_label = ctk.CTkLabel(
            results_frame,
            text="Results will appear here...",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.results_label.pack(pady=(15, 10))

        # Scrollable text widget for results
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.results_text.pack(pady=15, padx=15, fill="both", expand=True)

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text=f"📊 Loaded: {len(self.csv_data)} CSV files, {len(self.report_data)} reports",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(5, 15))

    def search_data(self):
        """Search through CSV data files"""
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search keyword!")
            return

        self.results_label.configure(text=f"🔍 CSV Data Search Results for: '{query}'")
        self.results_text.delete("0.0", "end")

        if not self.csv_data:
            self.results_text.insert("0.0", "❌ No CSV data files found. Please check the 'data/' folder.")
            return

        results_found = False
        total_matches = 0

        for filename, df in self.csv_data.items():
            matches = []

            # Search in all text columns
            for column in df.columns:
                if df[column].dtype == 'object':  # Text columns
                    mask = df[column].astype(str).str.lower().str.contains(query, na=False)
                    column_matches = df[mask]
                    if not column_matches.empty:
                        matches.append((column, column_matches))

            # Search in numeric columns (convert to string first)
            for column in df.select_dtypes(include=['number']).columns:
                mask = df[column].astype(str).str.lower().str.contains(query, na=False)
                column_matches = df[mask]
                if not column_matches.empty:
                    matches.append((column, column_matches))

            if matches:
                results_found = True
                self.results_text.insert("end", f"\n📁 File: {filename}\n")
                self.results_text.insert("end", "=" * 50 + "\n")

                for column_name, match_df in matches:
                    match_count = len(match_df)
                    total_matches += match_count
                    self.results_text.insert("end", f"\n🔸 Found {match_count} match(es) in column '{column_name}':\n")

                    # Show first 5 matches to avoid overwhelming the display
                    display_df = match_df.head(5)
                    for _, row in display_df.iterrows():
                        self.results_text.insert("end", f"   • {dict(row)}\n")

                    if len(match_df) > 5:
                        self.results_text.insert("end", f"   ... and {len(match_df) - 5} more matches\n")

                self.results_text.insert("end", "\n" + "-" * 50 + "\n")

        if not results_found:
            self.results_text.insert("0.0", f"❌ No matches found for '{query}' in CSV data.\n\n💡 Try different keywords like:\n- Country names: India, Brazil, Germany\n- Indicators: GDP, education, inequality, unemployment\n- Years: 2020, 2021, 2022")
        else:
            self.results_text.insert("0.0", f"✅ Found {total_matches} total matches across {len([f for f, _ in self.csv_data.items() if any(query in str(df.values).lower() for df in [_])])} files\n\n")

    def search_reports(self):
        """Search through report files"""
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search keyword!")
            return

        self.results_label.configure(text=f"📄 Report Search Results for: '{query}'")
        self.results_text.delete("0.0", "end")

        if not self.report_data:
            self.results_text.insert("0.0", "❌ No report files found. Please check the 'reports/' folder.")
            return

        results_found = False
        total_matches = 0

        for filename, content in self.report_data.items():
            content_str = ""

            # Handle different content types
            if isinstance(content, dict):
                content_str = json.dumps(content, indent=2).lower()
            else:
                content_str = str(content).lower()

            if query in content_str:
                results_found = True
                total_matches += 1

                self.results_text.insert("end", f"\n📄 File: {filename}\n")
                self.results_text.insert("end", "=" * 50 + "\n")

                # Find and display context around matches
                lines = content_str.split('\n')
                matching_lines = []

                for i, line in enumerate(lines):
                    if query in line:
                        # Include context (previous and next lines)
                        start = max(0, i-2)
                        end = min(len(lines), i+3)
                        context = lines[start:end]
                        matching_lines.extend(context)
                        matching_lines.append("---")

                # Display unique matching content (first 10 matches)
                unique_matches = list(dict.fromkeys(matching_lines))[:10]
                for line in unique_matches:
                    if line != "---":
                        # Highlight the query term
                        highlighted = line.replace(query, f"**{query.upper()}**")
                        self.results_text.insert("end", f"   {highlighted}\n")
                    else:
                        self.results_text.insert("end", "   ---\n")

                self.results_text.insert("end", "\n" + "-" * 50 + "\n")

        if not results_found:
            self.results_text.insert("0.0", f"❌ No matches found for '{query}' in reports.\n\n💡 Try different keywords like:\n- Policy terms: development, investment, reform\n- Economic terms: growth, inflation, trade\n- Country names: India, Brazil, Germany")
        else:
            self.results_text.insert("0.0", f"✅ Found matches in {total_matches} report(s)\n\n")

    def clear_results(self):
        """Clear search results"""
        self.results_label.configure(text="Results will appear here...")
        self.results_text.delete("0.0", "end")
        self.search_entry.delete(0, "end")

def main():
    """Main function to run the application"""
    # Check if required directories exist
    if not os.path.exists("data"):
        print("Creating 'data' directory...")
        os.makedirs("data")

    if not os.path.exists("reports"):
        print("Creating 'reports' directory...")
        os.makedirs("reports")

    # Check for required libraries
    try:
        import customtkinter
        import pandas
    except ImportError as e:
        print(f"Required library not found: {e}")
        print("Please install required libraries:")
        print("pip install customtkinter pandas")
        sys.exit(1)

    # Create and run the application
    app = EconoVisionAI()
    app.mainloop()

if __name__ == "__main__":
    main()
