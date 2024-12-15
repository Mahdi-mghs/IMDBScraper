from scraper import Scraper
import warnings

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    scraper = Scraper()
    scraper.extract_mainpage()
    scraper.iterating()
    scraper.save_file()
