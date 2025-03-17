import pytest
from get_papers_list.get_papers import fetch_papers, get_paper_details, is_non_academic

def test_fetch_papers():
    papers = fetch_papers("cancer")
    assert isinstance(papers, list)
    assert len(papers) > 0

def test_is_non_academic():
    author = {"name": "John Doe", "affiliation": "Pharma Inc."}
    assert is_non_academic(author) == True

    author = {"name": "Jane Doe", "affiliation": "University of California"}
    assert is_non_academic(author) == False