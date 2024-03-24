## Project Overview

This repository contains the source code for an API designed to perform sentiment analysis on Moroccan Darija language text data. The sentiment analysis model achieved an accuracy of 71% on the provided dataset.

## Project Structure

- **codeApi**: Contains the source code for the API.
  - **.idea**: Configuration files for IDE.
  - **__pycache__**: Cached Python files.
  - **DataAnalyste.py**: Module for data analysis.
  - **FaccebookScraper.py**: Module for scraping Facebook data.
  - **LaodedModel.py**: Module for loading the sentiment analysis model.
  - **Main.py**: Main script for running the API.
  - **NotoNaskhArabic-Regular.ttf**: Arabic font file.
  - **YouTubeCommentScraper.py**: Module for scraping YouTube comments.
- **model**: Directory containing the trained sentiment analysis model.
  - **SAMD.joblib**: Serialized model file.
- **data**: Directory containing data files used for training and testing.
  - **all_stop_words.json**: JSON file containing stop words for text preprocessing.
  - **data1.csv**: Dataset 1 in CSV format.
  - **data2.txt**: Dataset 2 in text format.
  - **data3.csv**: Dataset 3 in CSV format.
  - **data4.csv**: Dataset 4 in CSV format.
  - **dataMerge.csv**: Merged dataset in CSV format.
  - **emojis.csv**: CSV file containing emojis for sentiment analysis.
- **analysedes_sentiments[1].md**: Markdown file with sentiment analysis details.
- **app.py**: Main script for running the API.
- **jupyterCode.ipynb**: Jupyter Notebook containing code used for analysis.

## API Usage

To use the API, follow these steps:

1. Clone the repository.
2. Install the required dependencies.
3. Run the `app.py` script.
4. Make POST requests to the API endpoint to analyze text sentiment.

## Model Details

The sentiment analysis model was developed using Python and achieved an accuracy of 71% on the provided Moroccan Darija language dataset. It utilizes various data preprocessing techniques and machine learning algorithms to classify text into positive, negative, or neutral sentiments.

For further details, refer to the source code and the provided Markdown files.
