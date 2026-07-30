import argparse
import os
import re
import sys
import requests
import bibtexparser

ORCID_BASE_URL = "https://pub.orcid.org/v3.0"

def clean_title(title):
    """Normalize title string for robust matching."""
    return re.sub(r'[\{\}\s\W]+', '', title).lower()

def get_orcid_works(orcid_id):
    """Fetch all work summaries for an ORCID iD."""
    url = f"{ORCID_BASE_URL}/{orcid_id}/works"
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Unable to fetch works for ORCID iD {orcid_id} (Status: {response.status_code})")
        sys.exit(1)
        
    data = response.json()
    works = []
    for group in data.get("group", []):
        for summary in group.get("work-summary", []):
            works.append(summary)
    return works

def extract_year(work_summary):
    """Extract numeric publication year from ORCID work summary."""
    pub_date = work_summary.get("publication-date")
    if pub_date and pub_date.get("year"):
        try:
            return int(pub_date["year"]["value"])
        except (ValueError, TypeError):
            pass
    return None

def extract_authors(detail):
    """Extract and format contributor names into a BibTeX author string."""
    if not isinstance(detail, dict):
        return ""

    contrib_container = detail.get("contributors") or {}
    contributors = contrib_container.get("contributor") or []

    author_names = []
    for c in contributors:
        if not isinstance(c, dict):
            continue

        credit_name_obj = c.get("credit-name") or {}
        name = credit_name_obj.get("value", "").strip()

        if not name:
            given = (c.get("given-names") or {}).get("value", "").strip() if isinstance(c.get("given-names"), dict) else ""
            family = (c.get("family-name") or {}).get("value", "").strip() if isinstance(c.get("family-name"), dict) else ""
            name = f"{given} {family}".strip()

        if name:
            author_names.append(name)

    return " and ".join(author_names)

def fetch_work_detail(orcid_id, put_code):
    """Fetch full work detail from ORCID."""
    url = f"{ORCID_BASE_URL}/{orcid_id}/work/{put_code}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def generate_fallback_bibtex(detail, put_code, year):
    """Generate a valid BibTeX entry if ORCID lacks raw BibTeX text."""
    if not isinstance(detail, dict):
        detail = {}

    title_obj = (detail.get("title") or {}).get("title") or {}
    title = title_obj.get("value", "Untitled")

    authors = extract_authors(detail)

    url = ""
    ext_ids_obj = detail.get("external-ids") or {}
    external_ids = ext_ids_obj.get("external-id") or []
    for ext_id in external_ids:
        if isinstance(ext_id, dict) and ext_id.get("external-id-type") in ["doi", "DOI"]:
            url = f"https://doi.org/{ext_id.get('external-id-value')}"
            break
    if not url:
        url_obj = detail.get("url") or {}
        url = url_obj.get("value", "")

    # 1. Try to get standard journal title
    journal_obj = detail.get("journal-title") or {}
    journal = journal_obj.get("value", "")

    # 2. Fallback check for preprints & publisher metadata
    if not journal:
        # Check publisher field (ORCID often puts "EGUsphere" or "Copernicus GmbH" here)
        pub_obj = detail.get("publisher") or {}
        publisher_val = pub_obj.get("value", "") if isinstance(pub_obj, dict) else ""
        
        # Check work-type (e.g., PREPRINT)
        work_type = str(detail.get("type", "")).upper()

        if "EGUSPHERE" in url.upper() or "EGUSPHERE" in publisher_val.upper():
            journal = "EGUsphere (Preprint)"
        elif "ARXIV" in url.upper() or "ARXIV" in publisher_val.upper():
            journal = "arXiv (Preprint)"
        elif "BIORXIV" in url.upper() or "BIORXIV" in publisher_val.upper():
            journal = "bioRxiv (Preprint)"
        elif publisher_val:
            journal = publisher_val
        elif work_type == "PREPRINT":
            journal = "Preprint"

    clean_key_title = re.sub(r'\W+', '', title)[:15]
    cite_key = f"orcid_{year or '0000'}_{clean_key_title}_{put_code}"

    entry = {
        'ENTRYTYPE': 'article',
        'ID': cite_key,
        'title': title,
        'author': authors,
        'authors': authors,
        'year': str(year) if year else '',
        'journal': journal,
        'location': journal,
        'url': url
    }
    return entry

def update_bibtex_file(orcid_id, start_year, end_year, output_path, clean_file=False):
    # 1. Start completely fresh if --clean is requested
    if clean_file and os.path.exists(output_path):
        os.remove(output_path)
        print(f"Removed existing '{output_path}' file.")

    existing_db = bibtexparser.bibdatabase.BibDatabase()

    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            parser = bibtexparser.bparser.BibTexParser(common_strings=True)
            existing_db = bibtexparser.load(f, parser=parser)

    # Map normalized title -> index in existing_db.entries
    title_to_index = {clean_title(e.get('title', '')): i for i, e in enumerate(existing_db.entries)}

    print(f"Querying ORCID API for ID: {orcid_id}...")
    works = get_orcid_works(orcid_id)
    print(f"Found {len(works)} total works in profile.")

    added_count = 0

    for work in works:
        year = extract_year(work)

        # Date range filtering
        if start_year and (year is None or year < start_year):
            continue
        if end_year and (year is None or year > end_year):
            continue

        title_raw = work.get("title", {}).get("title", {}).get("value", "Untitled")
        title_norm = clean_title(title_raw)

        if title_norm in title_to_index:
            continue

        put_code = work.get("put-code")
        print(f"Fetching ({year or 'N/A'}): {title_raw[:60]}...")
        
        detail = fetch_work_detail(orcid_id, put_code)
        if not detail:
            continue

        citation = detail.get("citation")
        parsed_entry = None

        if citation and citation.get("citation-type") == "BIBTEX":
            bib_str = citation.get("citation-value")
            try:
                parsed = bibtexparser.loads(bib_str)
                if parsed.entries:
                    parsed_entry = parsed.entries[0]
            except Exception:
                pass

        if not parsed_entry:
            parsed_entry = generate_fallback_bibtex(detail, put_code, year)

        if 'authors' not in parsed_entry and 'author' in parsed_entry:
            parsed_entry['authors'] = parsed_entry['author']

        existing_db.entries.append(parsed_entry)
        title_to_index[title_norm] = len(existing_db.entries) - 1
        added_count += 1

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        bibtexparser.dump(existing_db, f)

    print(f"\nDone! Added {added_count} entries to '{output_path}'. Total records in .bib: {len(existing_db.entries)}")

def main():
    parser = argparse.ArgumentParser(description="Fetch citations from ORCID and build/update a .bib file.")
    parser.add_argument("orcid", help="ORCID iD (e.g. 0000-0002-1825-0097)")
    parser.add_argument("--start-year", type=int, help="Start year (inclusive)")
    parser.add_argument("--end-year", type=int, help="End year (inclusive)")
    parser.add_argument("--clean", action="store_true", help="Delete references.bib first and start fresh")
    parser.add_argument("--output", "-o", default="_bibliography/references.bib", help="Path to .bib file")
    
    args = parser.parse_args()
    update_bibtex_file(
        args.orcid,
        args.start_year,
        args.end_year,
        args.output,
        clean_file=args.clean
    )

if __name__ == '__main__':
    main()
