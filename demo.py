#!/usr/bin/env python3
"""
Demo script for EconoVisionAI
Tests the functionality without GUI
"""

import sys
import os
import pandas as pd
import json

# Add current directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.search_utils import DataSearcher

def test_csv_search():
    """Test CSV search functionality"""
    print("🔍 Testing CSV Search Functionality")
    print("=" * 50)

    searcher = DataSearcher()

    # Load sample data
    try:
        gdp_df = pd.read_csv("data/gdp.csv")
        print(f"📊 Loaded GDP data: {len(gdp_df)} countries")

        # Test search
        matches, stats = searcher.search_dataframe(gdp_df, "india gdp")
        print(f"🔍 Search 'india gdp': {len(matches)} matches")

        if not matches.empty:
            print("Sample result:")
            print(matches[['Country', 'GDP_Billion_USD', 'GDP_Per_Capita_USD']].head(1))

        print()

    except FileNotFoundError:
        print("❌ GDP data file not found")

def test_report_search():
    """Test report search functionality"""
    print("📄 Testing Report Search Functionality")
    print("=" * 50)

    searcher = DataSearcher()

    # Load sample report
    try:
        with open("reports/india_2022.txt", "r", encoding="utf-8") as f:
            content = f.read()

        print(f"📖 Loaded India report: {len(content)} characters")

        # Test search
        matches = searcher.search_text_content(content, "education gdp")
        print(f"🔍 Search 'education gdp': {len(matches)} matches")

        if matches:
            print("Sample match:")
            print(f"  Line {matches[0]['line_number']}: {matches[0]['matched_line'][:100]}...")

        print()

    except FileNotFoundError:
        print("❌ India report file not found")

def test_json_search():
    """Test JSON search functionality"""
    print("🔧 Testing JSON Search Functionality")
    print("=" * 50)

    searcher = DataSearcher()

    # Load sample JSON
    try:
        with open("reports/germany_2023.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"📋 Loaded Germany JSON: {len(str(data))} characters")

        # Test search
        matches = searcher.search_json_content(data, "education innovation")
        print(f"🔍 Search 'education innovation': {len(matches)} matches")

        if matches:
            print("Sample match:")
            print(f"  Path: {matches[0]['path']}")
            print(f"  Value: {matches[0]['value'][:100]}...")

        print()

    except FileNotFoundError:
        print("❌ Germany JSON file not found")

def display_data_summary():
    """Display summary of available data"""
    print("📊 Data Summary")
    print("=" * 50)

    # CSV files
    csv_files = []
    if os.path.exists("data"):
        csv_files = [f for f in os.listdir("data") if f.endswith('.csv')]

    print(f"📁 CSV Files: {len(csv_files)}")
    for file in csv_files:
        try:
            df = pd.read_csv(f"data/{file}")
            print(f"  • {file}: {len(df)} rows, {len(df.columns)} columns")
        except:
            print(f"  • {file}: Error loading")

    # Report files
    report_files = []
    if os.path.exists("reports"):
        report_files = [f for f in os.listdir("reports") if f.endswith(('.txt', '.json'))]

    print(f"📄 Report Files: {len(report_files)}")
    for file in report_files:
        try:
            file_path = f"reports/{file}"
            size = os.path.getsize(file_path)
            print(f"  • {file}: {size:,} bytes")
        except:
            print(f"  • {file}: Error accessing")

    print()

def main():
    """Run all demo tests"""
    print("🌍 EconoVisionAI Demo")
    print("Testing functionality without GUI")
    print("=" * 60)
    print()

    display_data_summary()
    test_csv_search()
    test_report_search()
    test_json_search()

    print("✅ Demo completed!")
    print("🚀 Run 'python main.py' to start the GUI application")

if __name__ == "__main__":
    main()
