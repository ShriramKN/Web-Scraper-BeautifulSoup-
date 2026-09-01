# 📁 Password Manager (Encryption)
**CodTech IT Solutions — Python Programming Internship**  
Task name : Web Scraper (BeautifulSoup)   
Intern : SHRIRAM K N  
Intern ID  : CITS8258  
Domain : Python Programming  
Duration : 4 Weeks  
Internship Period : 22 June 2026 - 20 July 2026

## 📌 Project Overview🖥️ GUI Interface

The **Web Scraper (BeautifulSoup)**, this project automates the collection of web data by parsing HTML tags and attributes. It aims to efficiently gather targeted public information from a website and organize it into a readable, local file, demonstrating the practical applications of data mining and web automation.

## ✨ Features
| Feature | Description |
|---------|-------------|
| 🎯 Data Extraction | Precisely pulls targeted information (e.g., text, links, titles, prices) from web pages. |
| 🔍 HTML Parsing | Utilizes BeautifulSoup to easily navigate and search through complex HTML structures. |
| 💾 Data Export | Automatically saves the extracted data into a structured .csv or .txt file for easy analysis. |
| ⚡ Automation | Scrapes multiple elements or pages rapidly, saving hours of manual data entry. |
| 🛡️ Error Handling | Gracefully handles missing HTML tags or connection timeouts without crashing. |


## 🛠️ Technologies Used

- **Language** : Python 3.x
- **Libraries** : requests — To send HTTP requests and fetch web page content.
-  bs4 (BeautifulSoup) — To parse and navigate the HTML/XML documents.
-  csv — (Built-in) To export the scraped data into a spreadsheet-friendly format.
```

```
##  Project Scope
This project automates the collection of web data by parsing HTML tags and attributes. It aims to efficiently gather targeted public information from a website and organize it into a readable, local file, demonstrating the practical applications of data mining and web automation.
```

```
##  Technologies Used
1.Python  
2.OS Module 
```

```
##  Features
1.Quickly pulls specific text, links, or prices from websites.
2.Navigates complex web page structures effortlessly using BeautifulSoup. 
3.Saves the gathered data directly into organized CSV files.
4.Automates repetitive manual data collection across multiple pages.
5.Handles missing data and connection errors smoothly without crashing.
```

```
## Project Structure
web-scraper/  
│  
├── scraper.py            ← Main Python scraping script  
├── scraped_data.csv      ← Auto-generated output file containing the data  
└── README.md             ← Project documentation
```

```
## How It Works (Step-by-Step)
Step 1 → Script takes the target website URL  
         ↓  
Step 2 → Sends an HTTP GET request using the `requests` library  
         ↓  
Step 3 → Website server responds with the page's HTML content  
         ↓  
Step 4 → BeautifulSoup parses the raw HTML structure  
         ↓  
Step 5 → Script searches for specific HTML tags/classes  
         ↓  
Step 6 → Targeted text or links are extracted and cleaned  
         ↓  
Step 7 → Data is written and saved to a local file (e.g., scraped_data.csv)
```

```
## Conclusion
This Web Scraper efficiently collects and organizes data from websites, significantly reducing manual effort and improving data collection pipelines. The project demonstrates strong skills in Python automation, working with HTTP requests, HTML parsing, and structured data extraction.
