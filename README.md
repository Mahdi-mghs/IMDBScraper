# IMDBScraper

## Description

IMDBScraper is a Python project designed to scrape data from IMDB's Top Movies list. It extracts key information about movies, such as title, rating, number of ratings, description, release year, parental rating, duration, genres, directors, creators, actors, and keywords. The tool processes and saves the scraped data in both JSON and CSV formats for further analysis.

## Features

- 🌟 Scrape IMDB Top Movies data.
- 📝 Extract movie details such as ratings, descriptions, genres, and more.
- 🔍 Fetch additional information from individual movie pages.
- 💾 Save data in JSON and CSV formats for convenience.

## Prerequisites

Ensure the following dependencies are installed in your Python environment:

- 🛠️ `requests`
- 🛠️ `json`
- 🛠️ `datetime`
- 🛠️ `fake-headers`
- 🛠️ `time`
- 🛠️ `tqdm`
- 🛠️ `re`
- 🛠️ `pandas`

Install the required packages using pip:

```bash
pip install requests fake-headers tqdm pandas
```

## Installation

1. 📥 Clone the repository:

   ```bash
   git clone https://github.com/yourusername/IMDBScraper.git
   cd IMDBScraper
   ```

2. ✅ Ensure Python 3.7 or higher is installed.

## Usage

### 1. Initialize the Scraper

```python
from scraper import Scraper
scraper = Scraper(browser="chrome", os="win")
```

### 2. Extract Main Page Data

Fetch data from the IMDB Top Movies page:

```python
scraper.extract_mainpage()
```

### 3. Extract Individual Movie Data

Iterate through the list of movies and extract detailed data for each:

```python
scraper.iterating()
```

### 4. Save Extracted Data

Save the scraped data to JSON and CSV files:

```python
scraper.save_file()
```

### Example Workflow

```python
from scraper import Scraper

# Initialize the scraper
scraper = Scraper(browser="chrome", os="win")

# Extract main page data
scraper.extract_mainpage()

# Extract detailed movie data
scraper.iterating()

# Save the data
scraper.save_file()
```

## Project Structure

```
IMDBScraper/
├── scraper.py       # Main scraping logic
├── requirements.txt # List of dependencies
├── ExtractedData/   # Directory to store output files
├── README.md        # Project documentation
```

## Output

Extracted data is stored in the `ExtractedData/` directory. The output includes:

1. 📄 A JSON file containing all scraped data.
2. 📊 A CSV file containing structured tabular data.

### Example Output

#### JSON

```json
{
    "movie_id": ["tt0111161", "tt0068646"],
    "title": ["The Shawshank Redemption", "The Godfather"],
    "rating": [9.3, 9.2],
    "No.rates": [2600000, 1800000],
    "description": [
        "Two imprisoned men bond over a number of years...",
        "The aging patriarch of an organized crime dynasty..."
    ],
    ...
}
```

#### CSV

| movie\_id | title                    | rating | No.rates | description                              | ... |
| --------- | ------------------------ | ------ | -------- | ---------------------------------------- | --- |
| tt0111161 | The Shawshank Redemption | 9.3    | 2600000  | Two imprisoned men bond over a number... | ... |
| tt0068646 | The Godfather            | 9.2    | 1800000  | The aging patriarch of an organized...   | ... |

## Notes

- ⏳ The scraper adheres to a delay between requests to prevent IP banning.
- 🌐 Ensure a stable internet connection during scraping.
- 🔧 For larger datasets, adjust the `iterating` logic to process all movies.

## Furthur More ?

Next Step I try analysis data with different Visualization tools, but in order I try tuning and more modularity about methods

So thanks for patient 🌛

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

