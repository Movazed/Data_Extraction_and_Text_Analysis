# Data_Extraction_and_Text_Analysis

## Overview

This project performs comprehensive text analysis on a set of web articles. It includes extracting titles and articles from URLs, tokenizing text, removing stop words, calculating sentiment scores, and computing various readability metrics.

## Directory Structure

- **Input Files**
  - `Input.xlsx`: Excel file containing URLs for web articles.

- **Output Directories**
  - `TitleText`: Directory where the extracted titles and texts from the URLs are stored.

- **Supporting Directories**
  - `StopWords`: Directory containing files with stop words to be removed during text processing.
  - `MasterDictionary`: Directory containing files with positive and negative words for sentiment analysis.

## Dependencies

- `requests`
- `beautifulsoup4`
- `pandas`
- `nltk`
- `openpyxl`
- `re`

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
