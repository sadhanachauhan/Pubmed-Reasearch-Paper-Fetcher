PubMed Research Paper Fetcher

This script fetches research papers from PubMed, filters out non-academic authors, and extracts relevant details such as company affiliations and corresponding author emails. The results can be saved in a CSV file or displayed in the terminal.

Features

Fetches PubMed IDs for research papers based on a query.

Retrieves details for each paper, including title, publication date, and authors.

Identifies non-academic authors and their affiliations.

Extracts corresponding author emails if available.

Saves results to a CSV file (optional).

Prerequisites

Ensure you have Python installed (version 3.x recommended) and install the required dependencies using:

pip install requests pandas argparse

Usage

Run the script with a query string to fetch research papers:

python script.py "cancer research"

Optional Arguments

-f, --file : Specify an output CSV file name to save results.

-d, --debug : Enable debug mode to print additional information.

Example:

python script.py "cancer research" -f results.csv -d

Output Format

The script outputs a table with the following columns:

PubmedID: Unique ID of the paper.

Title: Title of the research paper.

Publication Date: Date of publication.

Non-academic Author(s): Names of non-academic authors.

Company Affiliation(s): Companies associated with non-academic authors.

Corresponding Author Email: Email of the corresponding author (if available).

Example Output

PubmedID  | Title                         | Publication Date | Non-academic Author(s) | Company Affiliation(s) | Corresponding Author Email
-----------|-------------------------------|------------------|------------------------|------------------------|---------------------------
123456789 | Advances in Cancer Research  | 2024-06-01      | John Doe               | ABC Biotech            | john.doe@example.com

Notes

The script fetches up to 10 papers per query (modifiable in fetch_papers function).

It uses the NCBI PubMed API to retrieve data.

Non-academic authors are identified if they are not affiliated with universities or labs.

License

This project is open-source and available under the MIT License.

Author

Developed by [Sadhana Chauhan].

