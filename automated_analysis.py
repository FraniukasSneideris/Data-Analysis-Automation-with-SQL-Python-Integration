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
