import requests
import pandas as pd
import argparse
from typing import List, Dict, Optional

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_papers(query: str) -> List[str]:
    """Fetch PubMed IDs for papers matching the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def get_paper_details(pubmed_id: str) -> Optional[Dict]:
    """Fetch details for a specific paper using its PubMed ID."""
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "json"
    }
    response = requests.get(PUBMED_DETAILS_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("result", {}).get(pubmed_id, {})

def is_non_academic(author: Dict) -> bool:
    """Check if an author is affiliated with a non-academic institution."""
    affiliations = author.get("affiliation", "").lower()
    return "university" not in affiliations and "lab" not in affiliations

def main():
    """Main function to fetch and filter papers."""
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", help="PubMed query string")
    parser.add_argument("-f", "--file", help="Output CSV file name")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    args = parser.parse_args()

    papers = fetch_papers(args.query)
    results = []

    for pubmed_id in papers:
        details = get_paper_details(pubmed_id)
        if not details:
            continue

        non_academic_authors = []
        company_affiliations = set()
        corresponding_email = ""

        for author in details.get("authors", []):
            if is_non_academic(author):
                non_academic_authors.append(author.get("name", ""))
                affiliations = author.get("affiliation", "").split(";")
                for aff in affiliations:
                    if "pharma" in aff.lower() or "biotech" in aff.lower():
                        company_affiliations.add(aff.strip())

            if author.get("corresponding", "N") == "Y":
                corresponding_email = author.get("email", "")

        if non_academic_authors:
            results.append({
                "PubmedID": pubmed_id,
                "Title": details.get("title", ""),
                "Publication Date": details.get("pubdate", ""),
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            })

    df = pd.DataFrame(results)
    if args.file:
        df.to_csv(args.file, index=False)
        if args.debug:
            print(f"Results saved to {args.file}")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()