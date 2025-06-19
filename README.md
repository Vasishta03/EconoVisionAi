# 🌍 EconoVisionAI

A powerful Python GUI application for exploring economic development data using CustomTkinter. Search through OECD-style datasets and reports with an intuitive interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Features

- **Modern GUI**: Built with CustomTkinter for a sleek, modern interface
- **Dual Search**: Search both CSV datasets and text/JSON reports
- **Keyword Matching**: Intelligent keyword search across all data fields
- **Real-time Results**: Instant search results with highlighted matches
- **OECD-style Data**: Pre-loaded with sample economic indicators (GDP, education, inequality)
- **Flexible Format**: Supports CSV, TXT, and JSON data formats
- **No Database Required**: Uses file-based storage with pandas for processing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this project**
   ```bash
   # Download the files to your local machine
   git clone https://github.com/Vasishta03/EconoVisionAi
   ```

2. **Install dependencies**
   ```bash
   # Using the provided script (Linux/Mac)
   chmod +x install.sh
   ./install.sh

   # Or manually install
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
EconoVisionAI/
├── main.py                 # Main GUI application
├── requirements.txt        # Python dependencies
├── install.sh             # Installation script
├── README.md              # This file
├── data/                  # CSV datasets folder
│   ├── gdp.csv           # GDP data for various countries
│   ├── education.csv     # Education spending and metrics
│   └── inequality.csv    # Income inequality indicators
├── reports/               # Report summaries folder
│   ├── india_2022.txt    # India economic report (text)
│   ├── brazil_2023.txt   # Brazil economic report (text)
│   ├── germany_2023.json # Germany data (JSON format)
│   └── usa_2023.json     # USA analysis (JSON format)
└── utils/                 # Utility functions
    ├── __init__.py
    └── search_utils.py    # Advanced search functionality
```

## 🔍 How to Use

### 1. Search CSV Data
- Enter keywords like "GDP India", "education Brazil", or "inequality"
- Click **"🔍 Search Data (CSV)"** to search through economic datasets
- View matching records with country, year, and indicator values

### 2. Search Reports
- Use keywords like "policy", "growth", "development", or country names
- Click **"📄 Search Reports"** to search through text and JSON reports
- Get contextual results with highlighted matches

### 3. Clear Results
- Click **"🗑️ Clear Results"** to reset the search interface

### Example Searches

| Search Type | Keywords | Expected Results |
|-------------|----------|------------------|
| GDP Data | "GDP India", "United States 2022" | GDP figures, growth rates |
| Education | "education spending", "enrollment" | Education metrics by country |
| Inequality | "gini", "poverty", "income share" | Inequality indicators |
| Country Reports | "Brazil policy", "Germany innovation" | Report excerpts and analysis |

## 📊 Sample Data Included

### CSV Datasets
- **GDP Data**: 24 countries with GDP, per capita income, growth rates
- **Education Data**: 20 countries with spending, enrollment rates
- **Inequality Data**: 20 countries with Gini coefficients, poverty rates

### Reports
- **India 2022**: Comprehensive economic survey with growth analysis
- **Brazil 2023**: Economic outlook with social development focus
- **Germany 2023**: Detailed economic indicators and policy recommendations (JSON)
- **USA 2023**: Economic analysis with education and inequality data (JSON)

## 🛠️ Customization

### Adding Your Own Data

1. **CSV Files**: Place in `data/` folder
   - Must have headers in first row
   - Searchable columns: Country, Year, any text/numeric fields
   - Example: `data/your_data.csv`

2. **Report Files**: Place in `reports/` folder
   - Text files: `.txt` format with any content
   - JSON files: `.json` format with structured data
   - Example: `reports/your_report.txt`

### Modifying the Interface

- Edit `main.py` to customize the GUI layout
- Modify colors, fonts, and button styles using CustomTkinter options
- Add new search filters in the `search_utils.py` module

## 🎨 Interface Themes

The application supports CustomTkinter themes:
- **Dark Mode** (default): Modern dark interface
- **Light Mode**: Change in `main.py`: `ctk.set_appearance_mode("light")`
- **Color Themes**: blue (default), dark-blue, green

## 💡 Technical Details

### Libraries Used
- **CustomTkinter**: Modern GUI framework
- **Pandas**: Data processing and CSV handling
- **JSON**: Built-in JSON parsing
- **OS/Glob**: File system operations

### Search Capabilities
- Case-insensitive keyword matching
- Multi-column search in CSV files
- Context-aware text search in reports
- JSON structure traversal for nested data
- Relevance scoring for better results

### Performance
- Optimized for datasets up to 10,000 rows
- Lazy loading of data files
- Efficient pandas filtering
- Responsive UI with progress feedback

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add more sample data**: Create additional CSV files with economic indicators
2. **Improve search functionality**: Enhance the search algorithms
3. **UI improvements**: Suggest better layouts or features
4. **Documentation**: Help improve this README or add code comments

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

## 🌟 Acknowledgments

- **OECD**: Data structure inspired by OECD economic indicators
- **CustomTkinter**: Amazing modern GUI framework for Python
- **Pandas**: Powerful data manipulation library
- **Python Community**: For excellent documentation and support

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Verify your Python version (3.8+ required)
3. Ensure all dependencies are properly installed
4. Check file permissions for data and reports folders

---
*EconoVisionAI - Making economic data exploration simple and interactive*
