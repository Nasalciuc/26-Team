import json
import re
import csv
from datetime import datetime
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any, Optional, Set

from DrissionPage import SessionPage
from bs4 import BeautifulSoup, Tag

class UniversalSuperScraper:
    """
    A comprehensive web scraper designed to extract a wide variety of data points
    from a single URL, including metadata, text content, links, media, and more.

    The scraper uses DrissionPage to handle dynamic content and BeautifulSoup
    for efficient HTML parsing. The extracted data can be saved to both JSON
    and CSV formats.
    """

    def __init__(self):
        """Initializes the scraper with a SessionPage object."""
        self.page = SessionPage()

    def _clean_text(self, text: Optional[str]) -> str:
        """
        Cleans a string by removing extra whitespace.

        Args:
            text: The text to clean.

        Returns:
            The cleaned text.
        """
        if not text:
            return ""
        # Replace multiple whitespace characters with a single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def scrape(self, url: str) -> Dict[str, Any]:
        """
        The main method to perform the scraping of a given URL.

        It orchestrates the extraction of all data points and handles top-level
        errors, such as network issues or invalid URLs.

        Args:
            url: The URL of the website to scrape.

        Returns:
            A dictionary containing all the scraped data, or an error dictionary.
        """
        print(f"🔍 Starting to scrape {url}...")
        try:
            self.page.get(url)
            html = self.page.html
            soup = BeautifulSoup(html, 'html.parser')

            # Build the data dictionary step-by-step for clarity and better error handling
            data = {
                'url': url,
                'domain': urlparse(url).netloc,
                'scraped_at': datetime.now().isoformat(),
            }

            # A list of extraction methods to call. This makes the process modular.
            extraction_tasks = {
                'page_title': self._extract_page_title,
                'meta_tags': self._extract_meta_tags,
                'headings': self._extract_headings,
                'paragraphs': self._extract_paragraphs,
                'links': self._extract_links,
                'images': self._extract_images,
                'buttons': self._extract_buttons,
                'lists': self._extract_lists,
                'tables': self._extract_tables,
                'forms': self._extract_forms,
                'scripts': self._extract_scripts,
                'styles': self._extract_styles,
                'main_content': self._extract_main_content,
                'contact_info': self._extract_contact_info,
                'social_media': self._extract_social_media,
            }

            for key, func in extraction_tasks.items():
                try:
                    # Pass soup and base_url where needed
                    if key in ['links', 'images']:
                         data[key] = func(soup, url)
                    else:
                        data[key] = func(soup)
                except Exception as e:
                    print(f"⚠️ Warning: Could not extract '{key}'. Error: {e}")
                    data[key] = None # Ensure key exists even on failure

            print(f"✅ Scraping complete for {url}")
            return data

        except Exception as e:
            print(f"❌ Critical error scraping {url}: {str(e)}")
            return {'error': str(e), 'url': url}

    def _extract_page_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extracts the page title."""
        return self._clean_text(soup.title.get_text()) if soup.title else None

    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extracts meta tags from the page."""
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name', meta.get('property', ''))
            content = meta.get('content', '')
            if name and content:
                meta_tags[name.lower()] = content
        return meta_tags

    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extracts all headings (h1-h6) from the page."""
        headings = {f'h{i}': [] for i in range(1, 7)}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [self._clean_text(h.get_text()) for h in h_tags if self._clean_text(h.get_text())]
        return headings

    def _extract_paragraphs(self, soup: BeautifulSoup) -> List[str]:
        """Extracts all paragraphs from the page."""
        return [self._clean_text(p.get_text()) for p in soup.find_all('p') if self._clean_text(p.get_text())]

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extracts all links, resolving relative URLs."""
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = self._clean_text(link.get_text())
            full_url = urljoin(base_url, href)
            if text:
                links.append({'text': text, 'url': full_url})
        return links
        
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extracts all images, resolving relative URLs."""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if not src:
                continue
            alt = img.get('alt', '')
            full_src = urljoin(base_url, src)
            images.append({'src': full_src, 'alt': alt})
        return images

    def _extract_buttons(self, soup: BeautifulSoup) -> List[str]:
        """Extracts text from button and input[type=submit] elements."""
        buttons = []
        # Find all <button> elements and <input> elements of type submit, button, or reset
        for button in soup.find_all(['button', ('input', {'type': ['submit', 'button', 'reset']})]):
            text = ''
            if button.name == 'button':
                text = self._clean_text(button.get_text())
            elif button.name == 'input':
                text = self._clean_text(button.get('value', ''))
            
            if text:
                buttons.append(text)
        return list(set(buttons)) # Return unique button texts

    def _extract_lists(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extracts all ordered and unordered lists."""
        lists = []
        for list_tag in soup.find_all(['ul', 'ol']):
            items = [self._clean_text(li.get_text()) for li in list_tag.find_all('li', recursive=False) if self._clean_text(li.get_text())]
            if items:
                lists.append({'type': list_tag.name, 'items': items})
        return lists

    def _extract_tables(self, soup: BeautifulSoup) -> List[List[List[str]]]:
        """Extracts data from tables into a list of tables."""
        tables_data = []
        for table in soup.find_all('table'):
            rows_data = []
            for row in table.find_all('tr'):
                cells = [self._clean_text(cell.get_text()) for cell in row.find_all(['td', 'th'])]
                if any(cells):  # Only add row if it has content
                    rows_data.append(cells)
            if rows_data:
                tables_data.append(rows_data)
        return tables_data

    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extracts information about forms on the page."""
        forms = []
        for form in soup.find_all('form'):
            form_details = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'inputs': []
            }
            for inp in form.find_all(['input', 'textarea', 'select']):
                form_details['inputs'].append({
                    'tag': inp.name,
                    'type': inp.get('type', 'text'),
                    'name': inp.get('name', '')
                })
            forms.append(form_details)
        return forms

    def _extract_scripts(self, soup: BeautifulSoup) -> List[str]:
        """Extracts source URLs from script tags."""
        return [script.get('src') for script in soup.find_all('script') if script.get('src')]

    def _extract_styles(self, soup: BeautifulSoup) -> List[str]:
        """Extracts URLs from stylesheet links."""
        return [style.get('href') for style in soup.find_all('link', rel='stylesheet') if style.get('href')]

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Attempts to extract the main text content of the page by looking for
        common semantic tags like <main>, <article>, or <section>.
        """
        main_content_areas = soup.find_all(['main', 'article', 'section'])
        if not main_content_areas:
             # Fallback to body if no semantic tags are found
            main_content_areas = [soup.body] if soup.body else []

        # Combine text from all found areas and clean it
        full_text = ' '.join([self._clean_text(area.get_text()) for area in main_content_areas])
        return full_text

    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extracts potential email addresses and phone numbers from the page."""
        contact_info = {'emails': [], 'phones': []}
        text = soup.get_text()
        
        # Regex for emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        contact_info['emails'] = list(set(emails))
        
        # A more robust regex for phone numbers, looking for longer digit sequences
        # This is still not perfect but reduces false positives from random numbers.
        phones = re.findall(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?(\d{3}[-.\s]?\d{4})', text)
        # Flatten and clean the found phone numbers
        cleaned_phones = [''.join(p).strip() for p in phones]
        contact_info['phones'] = list(set(cleaned_phones))
        
        return contact_info

    def _extract_social_media(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extracts links to common social media platforms."""
        social_media = {}
        social_platforms = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'tiktok', 'github']
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            for platform in social_platforms:
                if platform in href:
                    # Avoid adding multiple links for the same platform
                    if platform not in social_media:
                        social_media[platform] = link.get('href')
                        break # Move to the next link
        return social_media

    def _generate_filename(self, url: str, extension: str) -> str:
        """Generates a filename based on the domain and current timestamp."""
        domain = urlparse(url).netloc.replace('.', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{domain}_{timestamp}.{extension}"
        
    def save_to_json(self, data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Saves the scraped data to a JSON file."""
        if not filename:
            filename = self._generate_filename(data['url'], 'json')
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
            
        print(f"📄 JSON data saved to: {filename}")
        return filename

    def save_to_csv(self, data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Saves a flattened version of the scraped data to a CSV file."""
        if not filename:
            filename = self._generate_filename(data['url'], 'csv')

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['Category', 'Sub-Category', 'Content'])

            # A helper function to write rows, avoiding repetition
            def write_row(category, sub_category, content):
                if content: # Only write if there's content
                    writer.writerow([category, sub_category, content])

            # Iterate through the data dictionary
            for key, value in data.items():
                if isinstance(value, str) or value is None:
                    write_row(key.replace('_', ' ').title(), '', value)
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, list):
                            for item in sub_value:
                                write_row(key.replace('_', ' ').title(), sub_key, item)
                        else:
                            write_row(key.replace('_', ' ').title(), sub_key, sub_value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            # For complex lists like links/images, join dict values
                            content_str = ' | '.join(f"{k}: {v}" for k, v in item.items())
                            write_row(key.replace('_', ' ').title(), '', content_str)
                        else:
                             write_row(key.replace('_', ' ').title(), '', item)
        
        print(f"📄 CSV data saved to: {filename}")
        return filename


def main():
    """Main function to run the scraper from the command line."""
    scraper = UniversalSuperScraper()
    url_to_scrape = input("🌐 Enter the URL to scrape (or press Enter for default): ").strip()
    
    # Use a default URL for demonstration if none is provided
    if not url_to_scrape:
        url_to_scrape = "https://www.utm.md/"
        print(f"No URL entered. Using default: {url_to_scrape}")

    print(f"\n🚀 Starting universal scrape for: {url_to_scrape}")
    scraped_data = scraper.scrape(url_to_scrape)
    
    # Check if scraping was successful before saving
    if 'error' not in scraped_data:
        csv_file = scraper.save_to_csv(scraped_data)
        json_file = scraper.save_to_json(scraped_data)
        print(f"\n✅ Scraping complete! Files created:\n   📄 {csv_file}\n   📄 {json_file}")
    else:
        print(f"❌ Scraping failed. Error: {scraped_data['error']}")

if __name__ == '__main__':
    main()
