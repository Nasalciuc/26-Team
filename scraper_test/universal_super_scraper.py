from DrissionPage import SessionPage
from bs4 import BeautifulSoup
import json
import re
import csv
from datetime import datetime
from urllib.parse import urljoin, urlparse

class UniversalSuperScraper:
    def __init__(self):
        self.page = SessionPage()
        self.data = {}

    def clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_all_data(self, url: str) -> dict:
        print(f"🔍 Scraping {url}...")
        try:
            self.page.get(url)
            html = self.page.html
            soup = BeautifulSoup(html, 'html.parser')
            self.data = {
                'url': url,
                'domain': urlparse(url).netloc,
                'scraped_at': datetime.now().isoformat(),
                'page_title': self.clean_text(soup.title.get_text()) if soup.title else None,
                'meta_tags': self.extract_meta_tags(soup),
                'headings': self.extract_headings(soup),
                'paragraphs': self.extract_paragraphs(soup),
                'links': self.extract_links(soup, url),
                'images': self.extract_images(soup, url),
                'buttons': self.extract_buttons(soup),
                'lists': self.extract_lists(soup),
                'tables': self.extract_tables(soup),
                'forms': self.extract_forms(soup),
                'scripts': self.extract_scripts(soup),
                'styles': self.extract_styles(soup),
                'important_divs': self.extract_important_divs(soup),
                'important_spans': self.extract_important_spans(soup),
                'contact_info': self.extract_contact_info(soup),
                'social_media': self.extract_social_media(soup),
                'company_info': self.extract_company_info(soup),
                'statistics': self.extract_statistics(soup),
                'css_classes': self.extract_css_classes(soup),
                'element_ids': self.extract_element_ids(soup),
            }
            print(f"✅ Scraping complet pentru {url}")
            return self.data
        except Exception as e:
            print(f"❌ Eroare la scraping {url}: {str(e)}")
            return {'error': str(e), 'url': url}

    def extract_meta_tags(self, soup):
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name', meta.get('property', meta.get('http-equiv', '')))
            content = meta.get('content', '')
            if name and content:
                meta_tags[name] = content
        return meta_tags

    def extract_headings(self, soup):
        headings = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [self.clean_text(h.get_text()) for h in h_tags if self.clean_text(h.get_text())]
        return headings

    def extract_paragraphs(self, soup):
        return [self.clean_text(p.get_text()) for p in soup.find_all('p') if self.clean_text(p.get_text())]

    def extract_links(self, soup, base_url):
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = self.clean_text(link.get_text())
            if href.startswith('/') or not href.startswith('http'):
                href = urljoin(base_url, href)
            if href and text:
                links.append({'text': text, 'url': href})
        return links

    def extract_images(self, soup, base_url):
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src.startswith('/') or not src.startswith('http'):
                src = urljoin(base_url, src)
            if src:
                images.append({'src': src, 'alt': alt})
        return images

    def extract_buttons(self, soup):
        buttons = []
        for button in soup.find_all(['button', 'input']):
            if button.name == 'button':
                text = self.clean_text(button.get_text())
            else:
                text = button.get('value', '')
            if text:
                buttons.append({'text': text})
        return buttons

    def extract_lists(self, soup):
        lists = []
        for ul in soup.find_all(['ul', 'ol']):
            items = [self.clean_text(li.get_text()) for li in ul.find_all('li') if self.clean_text(li.get_text())]
            if items:
                lists.append({'type': ul.name, 'items': items})
        return lists

    def extract_tables(self, soup):
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [self.clean_text(td.get_text()) for td in tr.find_all(['td', 'th']) if self.clean_text(td.get_text())]
                if cells:
                    rows.append(cells)
            if rows:
                tables.append({'rows': rows})
        return tables

    def extract_forms(self, soup):
        forms = []
        for form in soup.find_all('form'):
            inputs = [{'type': inp.get('type', 'text'), 'name': inp.get('name', '')} for inp in form.find_all('input')]
            forms.append({'action': form.get('action', ''), 'inputs': inputs})
        return forms

    def extract_scripts(self, soup):
        return [script.get('src', '') for script in soup.find_all('script') if script.get('src', '')]

    def extract_styles(self, soup):
        return [style.get('href', '') for style in soup.find_all('link', rel='stylesheet') if style.get('href', '')]

    def extract_important_divs(self, soup):
        return [{'classes': div.get('class', []), 'text': self.clean_text(div.get_text())[:200]} for div in soup.find_all('div') if div.get('class', [])]

    def extract_important_spans(self, soup):
        return [{'class': span.get('class', []), 'text': self.clean_text(span.get_text())} for span in soup.find_all('span') if self.clean_text(span.get_text())]

    def extract_contact_info(self, soup):
        contact_info = {}
        text = soup.get_text()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if emails:
            contact_info['emails'] = list(set(emails))
        phones = re.findall(r'[\+]?[1-9][\d]{0,15}', text)
        if phones:
            contact_info['phones'] = list(set(phones))[:5]
        return contact_info

    def extract_social_media(self, soup):
        social_media = {}
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            for platform in ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'tiktok']:
                if platform in href:
                    social_media[platform] = link.get('href')
        return social_media

    def extract_company_info(self, soup):
        company_info = {}
        if soup.title:
            company_info['title'] = soup.title.get_text()
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            company_info['description'] = meta_desc.get('content', '')
        return company_info

    def extract_statistics(self, soup):
        text = soup.get_text()
        stats = re.findall(r'\d+%', text)
        stats += re.findall(r'\b\d{3,}\b', text)
        return list(set(stats))

    def extract_css_classes(self, soup):
        classes = set()
        for element in soup.find_all(class_=True):
            for c in element.get('class', []):
                classes.add(c)
        return list(classes)

    def extract_element_ids(self, soup):
        return [element.get('id') for element in soup.find_all(id=True)]

    def save_to_csv(self, data, filename=None):
        if not filename:
            domain = urlparse(data['url']).netloc
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{domain}_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Tip Informație', 'Conținut', 'URL', 'Data Scraping'])
            if data.get('page_title'):
                writer.writerow(['Titlu Pagină', data['page_title'], data['url'], data['scraped_at']])
            for heading_type, headings in data.get('headings', {}).items():
                for heading in headings:
                    writer.writerow([f'Heading {heading_type.upper()}', heading, data['url'], data['scraped_at']])
            for paragraph in data.get('paragraphs', []):
                writer.writerow(['Paragraf', paragraph, data['url'], data['scraped_at']])
            for link in data.get('links', []):
                writer.writerow(['Link', f"{link['text']} - {link['url']}", data['url'], data['scraped_at']])
            for img in data.get('images', []):
                writer.writerow(['Imagine', f"{img['alt']} - {img['src']}", data['url'], data['scraped_at']])
            for button in data.get('buttons', []):
                writer.writerow(['Buton', button['text'], data['url'], data['scraped_at']])
            for i, lista in enumerate(data.get('lists', [])):
                for item in lista['items']:
                    writer.writerow([f'Lista {i+1}', item, data['url'], data['scraped_at']])
            for key, value in data.get('contact_info', {}).items():
                if isinstance(value, list):
                    for item in value:
                        writer.writerow([f'Contact {key.title()}', item, data['url'], data['scraped_at']])
                else:
                    writer.writerow([f'Contact {key.title()}', value, data['url'], data['scraped_at']])
            for platform, url in data.get('social_media', {}).items():
                writer.writerow([f'Social {platform.title()}', url, data['url'], data['scraped_at']])
            for stat in data.get('statistics', []):
                writer.writerow(['Statistică', stat, data['url'], data['scraped_at']])
        print(f"📄 CSV salvat: {filename}")
        return filename

    def save_to_json(self, data, filename=None):
        if not filename:
            domain = urlparse(data['url']).netloc
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{domain}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        print(f"📄 JSON salvat: {filename}")
        return filename

def main():
    scraper = UniversalSuperScraper()
    url = input("🌐 Introdu URL-ul website-ului de scrapat: ").strip()
    if not url:
        url = "https://ahrefs.com/websites/libertatea.ro"
    print(f"\n🚀 Pornește scraping universal pentru: {url}")
    data = scraper.extract_all_data(url)
    if 'error' not in data:
        csv_file = scraper.save_to_csv(data)
        json_file = scraper.save_to_json(data)
        print(f"\n✅ Scraping complet! Fișiere create:\n   📄 {csv_file}\n   📄 {json_file}")
    else:
        print(f"❌ Eroare: {data['error']}")

if __name__ == '__main__':
    main() 