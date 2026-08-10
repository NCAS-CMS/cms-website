import argparse
import csv
import os
import re
import sys
import yaml
import requests
import bibtexparser

from pathlib import Path

# Find repo root relative to this script (scripts/ is one level down)
REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "_config.yml"

# Strict load: Fail if file is missing or 'email' key doesn't exist
if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

if not config or "email" not in config or not config["email"]:
    raise KeyError("Missing required 'email' key in _config.yml")

SITE_EMAIL = config["email"]

ORCID_BASE_URL = "https://pub.orcid.org/v3.0"


def clean_title(title):
    """Normalize title string for robust matching."""
    return re.sub(r'[\{\}\s\W]+', '', title).lower()


def load_pubsignore(primary_path="_bibliography/.pubsignore"):
    """Load case-insensitive keyword blacklists from .pubsignore file."""
    target_path = primary_path
    if not os.path.exists(target_path):
        if os.path.exists(".pubsignore"):
            target_path = ".pubsignore"
        else:
            return []

    ignored_keywords = []
    with open(target_path, 'r', encoding='utf-8') as f:
        for line in f:
            clean_line = line.strip()
            if clean_line and not clean_line.startswith("#"):
                ignored_keywords.append(clean_line.lower())

    if ignored_keywords:
        print(f"Loaded {len(ignored_keywords)} title filter keyword(s) from '{target_path}'.")

    return ignored_keywords


def is_ignored(title, ignore_list):
    """Check if any ignored keyword appears in the publication title."""
    if not title or not ignore_list:
        return False

    title_lower = title.lower()
    return any(keyword in title_lower for keyword in ignore_list)


def fetch_bibtex_by_doi(doi):
    """Fetch BibTeX entry directly for a given DOI via DOI content negotiation or DataCite API."""
    clean_doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE).strip()
    url = f"https://doi.org/{clean_doi}"
    headers = {
        "Accept": "application/x-bibtex; charset=utf-8",
        "User-Agent": f"NCAS-CMS-BibFetcher/1.0 (mailto:{SITE_EMAIL})"
    }

    # Attempt 1: Official DOI Content Negotiation
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        if response.status_code == 200 and "@" in response.text:
            parsed = bibtexparser.loads(response.text)
            if parsed.entries:
                entry = parsed.entries[0]
                if not entry.get("url"):
                    entry["url"] = f"https://doi.org/{clean_doi}"
                return entry
    except Exception:
        pass

    # Attempt 2: DataCite REST API (handles Figshare DOIs specifically)
    try:
        dc_url = f"https://api.datacite.org/dois/{clean_doi}"
        dc_headers = {"User-Agent": f"NCAS-CMS-BibFetcher/1.0 (mailto:{SITE_EMAIL})"}
        resp = requests.get(dc_url, headers=dc_headers, timeout=10)
        if resp.status_code == 200:
            attrs = resp.json().get("data", {}).get("attributes", {})
            titles = attrs.get("titles", [{}])
            title = titles[0].get("title", "Untitled") if titles else "Untitled"
            pub_year = attrs.get("publicationYear", "")

            creators = attrs.get("creators", [])
            author_names = []
            for c in creators:
                if "name" in c and c["name"]:
                    author_names.append(c["name"])
                elif c.get("givenName") or c.get("familyName"):
                    author_names.append(f"{c.get('givenName', '')} {c.get('familyName', '')}".strip())
            authors = " and ".join(author_names) if author_names else ""

            publisher = attrs.get("publisher", "Figshare")
            clean_key_title = re.sub(r'\W+', '', title)[:15]
            cite_key = f"doi_{pub_year or '0000'}_{clean_key_title}"

            return {
                'ENTRYTYPE': 'article',
                'ID': cite_key,
                'title': title,
                'author': authors,
                'authors': authors,
                'year': str(pub_year),
                'journal': publisher,
                'location': publisher,
                'url': f"https://doi.org/{clean_doi}"
            }
    except Exception:
        pass

    return None


def get_orcid_work_groups(orcid_id):
    """Fetch all work groups from ORCID."""
    url = f"{ORCID_BASE_URL}/{orcid_id}/works"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"   [!] Error fetching works for ORCID {orcid_id} (Status: {response.status_code})")
        return []

    data = response.json()
    return data.get("group", [])


def extract_year(work_summary):
    """Extract numeric publication year from ORCID work summary."""
    pub_date = work_summary.get("publication-date")
    if pub_date and pub_date.get("year"):
        try:
            return int(pub_date["year"]["value"])
        except (ValueError, TypeError):
            pass
    return None


def fetch_authors_from_crossref(doi):
    """Fetch full ordered author list from Crossref API if ORCID missing contributors."""
    if not doi:
        return ""
    clean_doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    url = f"https://api.crossref.org/works/{clean_doi}"
    headers = {
        "User-Agent": f"NCAS-CMS-BibFetcher/1.0 (mailto:{SITE_EMAIL})"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            authors_data = data.get("message", {}).get("author", [])
            names = []
            for a in authors_data:
                given = a.get("given", "").strip()
                family = a.get("family", "").strip()
                if given and family:
                    names.append(f"{given} {family}")
                elif family:
                    names.append(family)
            if names:
                return " and ".join(names)
    except Exception:
        pass
    return ""


def extract_authors(detail, owner_name="", doi=None):
    """Extract author list, fallback to Crossref via DOI, or fallback to neutral text."""
    if not isinstance(detail, dict):
        detail = {}

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

    if author_names:
        return " and ".join(author_names)

    # Fallback 1: Try Crossref API using DOI
    if doi:
        crossref_authors = fetch_authors_from_crossref(doi)
        if crossref_authors:
            return crossref_authors

    # Fallback 2: Neutral group member statement
    return f"Authors include {owner_name}" if owner_name else ""


def fetch_bulk_work_details(orcid_id, put_codes):
    """Fetch full details for multiple put_codes in a single HTTP request."""
    if not put_codes:
        return {}

    codes_str = ",".join(str(code) for code in put_codes[:100])
    url = f"{ORCID_BASE_URL}/{orcid_id}/works/{codes_str}"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {}

    data = response.json()
    details_map = {}

    bulk_list = data.get("bulk", [])
    for item in bulk_list:
        work = item.get("work")
        if work and "put-code" in work:
            details_map[work["put-code"]] = work

    return details_map


def extract_doi_from_detail(detail):
    """Extract DOI from full work detail, checking external-ids and citation text."""
    if not isinstance(detail, dict):
        return ""

    ext_ids_obj = detail.get("external-ids") or {}
    external_ids = ext_ids_obj.get("external-id") or []
    for ext_id in external_ids:
        if isinstance(ext_id, dict):
            ext_type = str(ext_id.get("external-id-type", "")).lower().strip()
            ext_val = str(ext_id.get("external-id-value", "")).strip()
            ext_url = str(ext_id.get("external-id-url", {}).get("value", "") if isinstance(ext_id.get("external-id-url"), dict) else "").strip()

            if ext_type in ("doi", "doi-resolver") or ext_val.startswith("10."):
                clean_doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', ext_val, flags=re.IGNORECASE)
                return f"https://doi.org/{clean_doi}"
            elif "doi.org/10." in ext_url.lower():
                clean_doi = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', ext_url)
                if clean_doi:
                    return f"https://doi.org/{clean_doi.group(0)}"

    citation = detail.get("citation") or {}
    citation_val = citation.get("citation-value", "")
    if citation_val:
        doi_match = re.search(r'doi\s*=\s*[\{"]?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)[\}"]?', citation_val, re.IGNORECASE)
        if doi_match:
            return f"https://doi.org/{doi_match.group(1)}"

    return ""


def extract_orcid_url(detail):
    """Extract URL fallback if no DOI is present."""
    if not isinstance(detail, dict):
        return ""

    doi = extract_doi_from_detail(detail)
    if doi:
        return doi

    url_obj = detail.get("url") or {}
    url_val = url_obj.get("value", "").strip() if isinstance(url_obj, dict) else ""
    if url_val:
        return url_val

    ext_ids_obj = detail.get("external-ids") or {}
    external_ids = ext_ids_obj.get("external-id") or []
    for ext_id in external_ids:
        if isinstance(ext_id, dict):
            ext_val = str(ext_id.get("external-id-value", "")).strip()
            if ext_val.startswith("http://") or ext_val.startswith("https://"):
                return ext_val

    return ""


def generate_fallback_bibtex(detail, put_code, year, forced_doi=None, owner_name=""):
    """Generate BibTeX entry if raw BibTeX text is missing."""
    if not isinstance(detail, dict):
        detail = {}

    title_obj = (detail.get("title") or {}).get("title") or {}
    title = title_obj.get("value", "Untitled")

    subtitle_obj = (detail.get("title") or {}).get("subtitle") or {}
    subtitle = subtitle_obj.get("value", "").strip() if isinstance(subtitle_obj, dict) else ""

    if subtitle and subtitle.lower() not in title.lower():
        title = f"{title}: {subtitle}"

    url = forced_doi if forced_doi else extract_orcid_url(detail)
    authors = extract_authors(detail, owner_name=owner_name, doi=url)

    journal_obj = detail.get("journal-title") or {}
    journal = journal_obj.get("value", "")

    if not journal:
        pub_obj = detail.get("publisher") or {}
        publisher_val = pub_obj.get("value", "") if isinstance(pub_obj, dict) else ""
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


def process_orcid_group(orcid_id, group):
    """Fetch all items in a group via Bulk API, locate DOIs, and return best item."""
    summaries = group.get("work-summary", [])
    if not summaries:
        return None, None, None, None

    year = extract_year(summaries[0])
    put_codes = [s.get("put-code") for s in summaries if s.get("put-code")]

    details_map = fetch_bulk_work_details(orcid_id, put_codes)

    group_doi = None
    best_detail = None
    best_put_code = None

    for put_code, detail in details_map.items():
        doi = extract_doi_from_detail(detail)
        if doi:
            group_doi = doi
            if not best_detail:
                best_detail = detail
                best_put_code = put_code

    if not best_detail:
        for summary in summaries:
            p_code = summary.get("put-code")
            if p_code in details_map:
                best_detail = details_map[p_code]
                best_put_code = p_code
                if str(summary.get("display-index")) == "0":
                    break

    return best_detail, best_put_code, year, group_doi


def process_orcid(orcid_id, owner_name, existing_db, title_to_index, start_year, end_year, ignore_list=None):
    """Fetch and merge publications for a single ORCID ID into existing_db."""
    groups = get_orcid_work_groups(orcid_id)
    print(f"   Found {len(groups)} unique work groups in profile.")

    added_count = 0

    for group in groups:
        detail, put_code, year, group_doi = process_orcid_group(orcid_id, group)
        if not detail:
            continue

        if start_year and (year is None or year < start_year):
            continue
        if end_year and (year is None or year > end_year):
            continue

        title_obj = (detail.get("title") or {}).get("title") or {}
        title_raw = title_obj.get("value", "Untitled")

        subtitle_obj = (detail.get("title") or {}).get("subtitle") or {}
        subtitle_raw = subtitle_obj.get("value", "").strip() if isinstance(subtitle_obj, dict) else ""

        full_title = title_raw
        if subtitle_raw and subtitle_raw.lower() not in title_raw.lower():
            full_title = f"{title_raw}: {subtitle_raw}"

        # FILTER VIA .pubsignore
        if is_ignored(full_title, ignore_list):
            print(f"   [-] Skipping ignored paper: {full_title[:50]}...")
            continue

        title_norm = clean_title(full_title)

        if title_norm in title_to_index:
            continue

        print(f"   + Fetching ({year or 'N/A'}): {full_title[:50]}...")

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
            parsed_entry = generate_fallback_bibtex(detail, put_code, year, forced_doi=group_doi, owner_name=owner_name)
        else:
            if group_doi:
                parsed_entry["url"] = group_doi
            elif not parsed_entry.get("url"):
                parsed_entry["url"] = extract_orcid_url(detail)

        # Ensure title retains subtitle if missing
        if subtitle_raw and subtitle_raw.lower() not in parsed_entry.get("title", "").lower():
            parsed_entry["title"] = f"{parsed_entry.get('title', title_raw)}: {subtitle_raw}"

        # Guarantee year field is populated
        if not parsed_entry.get("year") and year:
            parsed_entry["year"] = str(year)

        # Ensure author field is populated
        current_authors = parsed_entry.get("author") or parsed_entry.get("authors") or ""
        if not current_authors.strip():
            fallback_authors = extract_authors(detail, owner_name=owner_name, doi=parsed_entry.get("url"))
            parsed_entry['author'] = fallback_authors
            parsed_entry['authors'] = fallback_authors
        else:
            parsed_entry['authors'] = current_authors

        existing_db.entries.append(parsed_entry)
        title_to_index[title_norm] = len(existing_db.entries) - 1
        added_count += 1

    return added_count


def load_dois_from_csv(filepath):
    """Extract dicts with clean DOIs and output_type descriptions from a CSV file."""
    if not os.path.exists(filepath):
        return []

    doi_records = []
    seen_dois = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue

            # Skip comment lines starting with #
            first_cell = row[0].strip() if row[0] else ""
            if first_cell.startswith('#'):
                continue

            doi_val = None
            doi_col_idx = -1

            # Search for DOI string in the row
            for idx, cell in enumerate(row):
                match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', cell)
                if match:
                    doi_val = match.group(0).rstrip('.,;')
                    doi_col_idx = idx
                    break

            if doi_val and doi_val not in seen_dois:
                seen_dois.add(doi_val)
                output_type = ""
                # Get description from the column immediately following the DOI (usually column 2)
                desc_idx = doi_col_idx + 1 if doi_col_idx != -1 else 1
                if len(row) > desc_idx:
                    output_type = row[desc_idx].strip(" '\"")

                doi_records.append({'doi': doi_val, 'output_type': output_type})

    return doi_records


def process_csv_dois(csv_path, existing_db, title_to_index, start_year, end_year, ignore_list=None):
    """Process additional DOIs listed in a CSV file."""
    records = load_dois_from_csv(csv_path)
    if not records:
        return 0

    print(f"\nProcessing {len(records)} extra DOI(s) from '{csv_path}'...")
    added_count = 0

    for rec in records:
        doi = rec['doi']
        output_type = rec['output_type']
        clean_doi_url = f"https://doi.org/{re.sub(r'^https?://(dx\.)?doi\.org/', '', doi, flags=re.IGNORECASE)}"

        # Check if already present by exact DOI URL
        if any(e.get('url') == clean_doi_url for e in existing_db.entries):
            continue

        entry = fetch_bibtex_by_doi(doi)
        if not entry:
            print(f"   [!] Could not fetch metadata for DOI: {doi}")
            continue

        title = entry.get("title", "")
        if not title:
            continue

        # Override location/journal with free text output type from Column 2 if provided
        if output_type:
            entry['journal'] = output_type
            entry['location'] = output_type
            entry['type'] = output_type

        # Extract year integer if possible
        year_str = entry.get("year", "")
        try:
            year = int(year_str) if year_str else None
        except ValueError:
            year = None

        if start_year and (year is None or year < start_year):
            continue
        if end_year and (year is None or year > end_year):
            continue

        # Check .pubsignore
        if is_ignored(title, ignore_list):
            print(f"   [-] Skipping ignored DOI paper: {title[:50]}...")
            continue

        title_norm = clean_title(title)
        if title_norm in title_to_index:
            continue

        print(f"   + Fetching DOI ({year or 'N/A'}): {title[:50]}...")

        authors = entry.get("author") or entry.get("authors") or ""
        entry["author"] = authors
        entry["authors"] = authors

        existing_db.entries.append(entry)
        title_to_index[title_norm] = len(existing_db.entries) - 1
        added_count += 1

    return added_count


def load_orcids_from_people_file(filepath):
    """Extract list of dicts with name & orcid from people.yml."""
    if not os.path.exists(filepath):
        print(f"Error: People file '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        people = yaml.safe_load(f) or []

    records = []
    for person in people:
        if isinstance(person, dict) and person.get('orcid'):
            name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
            orcid_str = str(person['orcid']).strip()
            records.append({'name': name, 'orcid': orcid_str})
    return records


def update_bibtex_file(orcid_list, start_year, end_year, output_path, clean_file=False, dois_file=None):
    if clean_file and os.path.exists(output_path):
        os.remove(output_path)
        print(f"Cleaned existing output file '{output_path}'.")

    ignore_list = load_pubsignore()

    existing_db = bibtexparser.bibdatabase.BibDatabase()

    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            parser = bibtexparser.bparser.BibTexParser(common_strings=True)
            existing_db = bibtexparser.load(f, parser=parser)

    title_to_index = {clean_title(e.get('title', '')): i for i, e in enumerate(existing_db.entries)}

    total_added = 0
    for idx, item in enumerate(orcid_list, 1):
        name = item.get('name', 'Unknown')
        orcid_id = item['orcid']
        print(f"\n[{idx}/{len(orcid_list)}] Processing {name} ({orcid_id})...")
        added = process_orcid(orcid_id, name, existing_db, title_to_index, start_year, end_year, ignore_list=ignore_list)
        total_added += added

    # Process standalone DOIs from CSV if present
    default_dois_path = Path(__file__).resolve().parent / "dois.csv"
    target_dois_path = dois_file if dois_file else default_dois_path

    if os.path.exists(target_dois_path):
        total_added += process_csv_dois(target_dois_path, existing_db, title_to_index, start_year, end_year, ignore_list=ignore_list)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        bibtexparser.dump(existing_db, f)

    print(f"\nFinished! Added {total_added} total new entries to '{output_path}'. Total database count: {len(existing_db.entries)}")


def main():
    parser = argparse.ArgumentParser(description="Fetch citations from ORCID profiles/DOIs and build/update a .bib file.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--orcid", help="Single ORCID iD (e.g. 0000-0002-1825-0097)")
    group.add_argument("--people-file", help="Path to YAML people file (e.g. _data/people.yml)")

    parser.add_argument("--dois-file", help="Path to CSV file containing DOIs (default: dois.csv in script dir)")
    parser.add_argument("--start-year", type=int, help="Start year (inclusive)")
    parser.add_argument("--end-year", type=int, help="End year (inclusive)")
    parser.add_argument("--clean", action="store_true", help="Delete output .bib file first and start fresh")
    parser.add_argument("--output", "-o", default="_bibliography/references.bib", help="Path to output .bib file")

    args = parser.parse_args()

    if args.people_file:
        orcid_list = load_orcids_from_people_file(args.people_file)
        print(f"Loaded {len(orcid_list)} ORCID profiles from '{args.people_file}'.")
    elif args.orcid:
        orcid_list = [{'name': 'Single Target', 'orcid': args.orcid}]
    else:
        orcid_list = []

    update_bibtex_file(
        orcid_list,
        args.start_year,
        args.end_year,
        args.output,
        clean_file=args.clean,
        dois_file=args.dois_file
    )


if __name__ == '__main__':
    main()
