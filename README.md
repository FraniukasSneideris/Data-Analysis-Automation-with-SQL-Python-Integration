# Data-Analysis-Automation-with-SQL-Python-Integration
![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)


This project aims to show how to automate an analysis task using SQL-Python integration, user input and CLI. 

Lab results analysis automation was used in this case to show the script functionality, but the script can be easily adapted to other types of data analysis. By using Python and SQL, it integrates database management and data analysis, offering an efficient way to handle data that meets specific conditions. The script reads a CSV file containing lab results, performs checks for missing data and out-of-range results, and allows the user to download these results as CSV files.

## Code Overview

The core of this script is built around 4 functions which perform the following tasks:
- **Read a CSV file** containing data for analysis.
- **Store data in an SQLite database** using SQLAlchemy, which allows SQL queries to be run on the data.
- **Analyze the data** by identifying missing values and out-of-range results using SQL queries.
- **Download the results** as CSV files based on user input.

## The code

```python
from sqlalchemy import create_engine
import pandas as pd
import argparse


def read_file(file):
    df = pd.read_csv(file)
    return df


def store_in_sqlite(df, engine):
    df.to_sql("lab_results", con=engine, index=False, if_exists="replace")


def analyze_lab_results(engine):
    query_a = "SELECT * FROM lab_results WHERE result IS NULL"
    query_b = "SELECT * FROM lab_results WHERE lower_ref IS NULL OR upper_ref IS NULL"
    query_c = "SELECT * FROM lab_results WHERE result < lower_ref OR result > upper_ref"
    
    blank_results = pd.read_sql(query_a, con=engine)
    missing_range = pd.read_sql(query_b, con=engine)
    out_of_range_results = pd.read_sql(query_c, con=engine)

    if blank_results.empty:
        print("There are no empty results.\n")
    else:
        print("The following rows are missing results values:")
        print(blank_results, "\n")

    if missing_range.empty:
        print("There are no missing normal ranges.\n")
    else:
        print("The following rows are missing normal ranges:")
        print(missing_range, "\n")

    if out_of_range_results.empty:
        print("No out of range results were found.\n")
    else:
        print("The following results are out of range:")
        print(out_of_range_results, "\n")

    return blank_results, missing_range, out_of_range_results  


def download_results(blank_results, missing_range, out_of_range_results):
    if not (blank_results.empty and missing_range.empty and out_of_range_results.empty):
        choice = input("Download results? y/n: ").strip().lower()

        if choice == "y":
            to_save = {
                "blank_results.csv": blank_results,
                "missing_range.csv": missing_range,
                "out_of_range_results.csv": out_of_range_results
            }

            for filename, df in to_save.items():
                if not df.empty:
                    df.to_csv(filename, index=False)
                    print(f"{filename} saved.")

            print("All files downloaded.")
        
        else:
            print("Download skipped.")
    
    else:
        print("Nothing to download.")


engine = create_engine("sqlite://", echo=False)


def main(file):
    df = read_file(file)  
    store_in_sqlite(df, engine)
    blank_results, missing_range, out_of_range_results = analyze_lab_results(engine)  
    download_results(blank_results, missing_range, out_of_range_results)  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab results analysis. \
                                     Returns rows with blank results, missing ranges and out of range results. \
                                     Offers the option to download these results as CSV files.")
    parser.add_argument("file", help="Path to the lab_results data file.")
    args = parser.parse_args()

    main(args.file)
```

### Key Features
- **SQL-Python Integration**: The script stores data in an SQLite database and uses SQL queries to perform checks on the data, making it easier to handle larger datasets.
- **Data Analysis**: The script analyzes the data for:
  - Blank results (missing result values).
  - Missing reference ranges (missing lower or upper reference values).
  - Out-of-range results (results that fall outside the specified reference ranges).
- **CLI-Based Interaction**: The user interacts with the script via the command line, and is prompted whether to download any identified issues.
- **Selective Download**: The user can download only the relevant CSV files (blank results, missing ranges, or out-of-range results), depending on the issues identified.

## Libraries Used
- **pandas**: Used for data manipulation and handling CSV files.
- **argparse**: Used for command-line argument parsing.
- **SQLite (via SQLAlchemy)**: Used for storing data in a lightweight database and executing SQL queries.

To install, please run the following on your terminal:
```bash
pip install pandas argparse sqlalchemy
```

## How it works

1) Read Data: The script reads a CSV file containing lab results (or any other data).
2) Store in SQLite Database: The data is stored in an SQLite database, allowing for easier querying and analysis.
3) Data Analysis: The script checks for:
   - Blank results (result IS NULL)
   - Missing reference ranges (lower_ref or upper_ref IS NULL)
   - Out of range results (result < lower_ref OR result > upper_ref)
4) Download Results: If any issues are found, the user can choose to download CSV files containing these rows.

## How to use

Run the script on the terminal of your prefered IDE using the following format:
```bash
python automated_analysis.py "filename.csv"
```

Where "filename.csv" should contain the lab results (I am providing a wide range of CSV files in this repository to try the script).

## Input and Output
- Input: The script expects a CSV file containing lab results (or other data). The file should have columns similar to sample_id, result, lower_ref, and upper_ref.
- Output: If any issues are detected (missing results, missing reference ranges, or out-of-range results), the script will save the relevant rows as CSV files (blank_results.csv, missing_range.csv, out_of_range_results.csv) in the same directory as the script.

### Example output
```bash
The following rows are missing results values:
   sample_id result  lower_ref  upper_ref
0          1    NaN       4.5       10.0

The following rows are missing normal ranges:
   sample_id result  lower_ref  upper_ref
1          2    7.0       NaN       10.0

The following results are out of range:
   sample_id result  lower_ref  upper_ref
2          3    15.0       5.0       10.0

Download results? y/n: y      # User gets to decide if to download results or not
blank_results.csv saved.
missing_range.csv saved.
out_of_range_results.csv saved.
All files downloaded.
```
## Customization
You can modify the script for different types of analysis. Change the SQL queries in the analyze_lab_results function to fit the specific dataset you are working with. For example, if you're working with financial data, you could modify the queries to check for missing or out-of-range values relevant to that domain. 

This script is also applicable for KPI/KRI (Key Performance/Risk Indicators) identification: if said KPI/KRI stem from value exceeding or not reaching certain thresholds, the SQL queries can be modified, or more can be added, so that this KPI/KRi are identified.

## Conclusion
This script demonstrates a powerful yet simple approach to automating data analysis tasks using Python and SQL. It’s designed to help identify and manage missing or problematic data in lab results, but can easily be adapted to other types of data analysis. By leveraging SQL queries for efficient filtering and offering user control over which data to download, the project provides flexibility and efficiency. With the ability to integrate seamlessly with CSV files and SQLite, this tool can be a valuable addition to any data processing workflow.

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

