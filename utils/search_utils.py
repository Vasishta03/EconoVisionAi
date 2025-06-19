"""
Search utilities for EconoVisionAI
Provides advanced search and filtering functions for economic data
"""

import pandas as pd
import re
from typing import List, Dict, Tuple, Any
import json

class DataSearcher:
    """Advanced search functionality for CSV and report data"""

    def __init__(self):
        self.stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'a', 'an', 'this', 'that', 'these', 'those'
        }

    def preprocess_query(self, query: str) -> List[str]:
        """
        Preprocess search query by removing stop words and splitting into keywords
        """
        # Convert to lowercase and split
        words = re.findall(r'\b\w+\b', query.lower())

        # Remove stop words and short words
        keywords = [word for word in words if word not in self.stop_words and len(word) > 2]

        return keywords

    def search_dataframe(self, df: pd.DataFrame, query: str, fuzzy: bool = True) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Search DataFrame with advanced filtering
        Returns matching rows and match statistics
        """
        keywords = self.preprocess_query(query)
        if not keywords:
            return pd.DataFrame(), {}

        match_scores = {}
        all_matches = pd.DataFrame()

        for keyword in keywords:
            keyword_matches = pd.DataFrame()
            column_matches = {}

            # Search in each column
            for column in df.columns:
                column_data = df[column].astype(str).str.lower()

                if fuzzy:
                    # Fuzzy matching - contains keyword
                    mask = column_data.str.contains(keyword, na=False, regex=False)
                else:
                    # Exact matching
                    mask = column_data == keyword

                column_results = df[mask]
                if not column_results.empty:
                    column_matches[column] = len(column_results)
                    keyword_matches = pd.concat([keyword_matches, column_results]).drop_duplicates()

            if not keyword_matches.empty:
                match_scores[keyword] = column_matches
                all_matches = pd.concat([all_matches, keyword_matches]).drop_duplicates()

        return all_matches, match_scores

    def search_text_content(self, content: str, query: str, context_lines: int = 3) -> List[Dict[str, Any]]:
        """
        Search text content and return matches with context
        """
        keywords = self.preprocess_query(query)
        if not keywords:
            return []

        matches = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            line_lower = line.lower()

            for keyword in keywords:
                if keyword in line_lower:
                    # Get context around the match
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    context = lines[start:end]

                    # Highlight the keyword in the matching line
                    highlighted_line = re.sub(
                        f'({re.escape(keyword)})', 
                        r'**\1**', 
                        line, 
                        flags=re.IGNORECASE
                    )

                    matches.append({
                        'keyword': keyword,
                        'line_number': i + 1,
                        'matched_line': highlighted_line,
                        'context': context,
                        'relevance_score': self._calculate_relevance(line_lower, keyword)
                    })

        # Sort by relevance score
        matches.sort(key=lambda x: x['relevance_score'], reverse=True)
        return matches

    def search_json_content(self, json_data: Dict, query: str) -> List[Dict[str, Any]]:
        """
        Search JSON content recursively
        """
        keywords = self.preprocess_query(query)
        if not keywords:
            return []

        matches = []

        def search_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    search_recursive(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    search_recursive(item, current_path)
            else:
                # Search in the value
                str_value = str(obj).lower()
                for keyword in keywords:
                    if keyword in str_value:
                        matches.append({
                            'keyword': keyword,
                            'path': path,
                            'value': str(obj),
                            'relevance_score': self._calculate_relevance(str_value, keyword)
                        })

        search_recursive(json_data)

        # Sort by relevance and remove duplicates
        unique_matches = []
        seen = set()
        for match in sorted(matches, key=lambda x: x['relevance_score'], reverse=True):
            key = (match['path'], match['keyword'])
            if key not in seen:
                unique_matches.append(match)
                seen.add(key)

        return unique_matches

    def _calculate_relevance(self, text: str, keyword: str) -> float:
        """
        Calculate relevance score based on keyword frequency and position
        """
        # Count occurrences
        count = text.count(keyword)

        # Check if keyword appears at the beginning (higher relevance)
        position_bonus = 2.0 if text.startswith(keyword) else 1.0

        # Check if keyword appears as a whole word
        word_bonus = 1.5 if f' {keyword} ' in f' {text} ' else 1.0

        # Calculate final score
        score = count * position_bonus * word_bonus

        return score

    def filter_by_country(self, df: pd.DataFrame, country: str) -> pd.DataFrame:
        """
        Filter DataFrame by country name
        """
        if 'Country' in df.columns:
            mask = df['Country'].str.contains(country, case=False, na=False)
            return df[mask]
        return pd.DataFrame()

    def filter_by_year(self, df: pd.DataFrame, year: int) -> pd.DataFrame:
        """
        Filter DataFrame by year
        """
        if 'Year' in df.columns:
            return df[df['Year'] == year]
        return pd.DataFrame()

    def filter_by_range(self, df: pd.DataFrame, column: str, min_val: float, max_val: float) -> pd.DataFrame:
        """
        Filter DataFrame by numeric range
        """
        if column in df.columns:
            numeric_col = pd.to_numeric(df[column], errors='coerce')
            mask = (numeric_col >= min_val) & (numeric_col <= max_val)
            return df[mask]
        return pd.DataFrame()

    def get_summary_stats(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Get summary statistics for a numeric column
        """
        if column not in df.columns:
            return {}

        numeric_col = pd.to_numeric(df[column], errors='coerce')

        if numeric_col.empty:
            return {}

        return {
            'count': len(numeric_col.dropna()),
            'mean': numeric_col.mean(),
            'median': numeric_col.median(),
            'std': numeric_col.std(),
            'min': numeric_col.min(),
            'max': numeric_col.max(),
            'q25': numeric_col.quantile(0.25),
            'q75': numeric_col.quantile(0.75)
        }

# Utility functions for data formatting
def format_large_number(num: float) -> str:
    """Format large numbers with appropriate suffixes"""
    if abs(num) >= 1e12:
        return f"{num/1e12:.1f}T"
    elif abs(num) >= 1e9:
        return f"{num/1e9:.1f}B"
    elif abs(num) >= 1e6:
        return f"{num/1e6:.1f}M"
    elif abs(num) >= 1e3:
        return f"{num/1e3:.1f}K"
    else:
        return f"{num:.1f}"

def format_percentage(num: float) -> str:
    """Format percentage values"""
    return f"{num:.1f}%"

def highlight_text(text: str, keywords: List[str]) -> str:
    """Highlight keywords in text"""
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(f"**{keyword.upper()}**", text)
    return text
