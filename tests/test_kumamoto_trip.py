"""Offline checks for the Kumamoto 3-night candidate; no live inventory claims.

Run from the repository root: python -m unittest discover -s tests -v
Place name, hours and map links were checked on 2026-11-16. These checks validate
the record's structure and rules only; they do not replace live re-verification.
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ID = '2026-11-16-kumamoto-small-town'
COURSE = ROOT / 'courses/2026' / ID


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.day_cards = 0
        self.stay_cards = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a':
            self.links.append(a)
        if tag == 'article':
            classes = a.get('class', '').split()
            if 'day-card' in classes:
                self.day_cards += 1
            if 'kuma-card' in classes:
                self.stay_cards += 1


class KumamotoTripTest(unittest.TestCase):
    def setUp(self):
        self.html = (COURSE / 'course-options.html').read_text(encoding='utf-8')
        self.md = (COURSE / 'README.md').read_text(encoding='utf-8')
        self.p = Parser()
        self.p.feed(self.html)

    def test_date_is_undecided_in_folder_and_page(self):
        self.assertIn('여행 날짜: 미정', self.md)
        self.assertIn('폴더 날짜는 조사일', self.md)
        for text in (self.html, self.md):
            self.assertIn('미정', text)
            self.assertIn('2027', text)
            self.assertIn('3월 말', text)
            self.assertIn('4월 중순', text)
        self.assertIn('2026-11-16', self.md)

    def test_prices_are_absent(self):
        for text in (self.html, self.md):
            self.assertNotRegex(text, r'\d[\d,]*\s*원(?!삼면)')
            self.assertNotRegex(text, r'[¥￥]\s*\d')
            self.assertNotRegex(text, r'\d[\d,]*\s*(?:엔|円)')
            for term in ['총예상경비', '가격 비교']:
                self.assertNotIn(term, text)

    def test_itinerary_days_and_stay_cards(self):
        self.assertEqual(self.p.day_cards, 4)
        self.assertEqual(self.p.stay_cards, 7)  # 료칸 3곳 + 보너스 1곳 + 시내 호텔 3곳
        for term in ['1일차', '2일차', '3일차', '4일차', '금요일', '월요일']:
            self.assertIn(term, self.html)

    def test_places_from_source_notes(self):
        for term in ['이치노이', '후모토', '오갸쿠야', '야마미즈키',
                     '구마모토 호텔 캐슬', '테르사', 'OMO5',
                     '구로카와', '구마모토성', '스이젠지 성취원',
                     '잇신교', '시라카와 수원', '다이칸보', '나베가타키', '아소 신사']:
            self.assertIn(term, self.html)
            self.assertIn(term, self.md)

    def test_unique_anchors_and_local_files(self):
        self.assertEqual(len(self.p.ids), len(set(self.p.ids)))
        for a in self.p.links:
            href = a['href']
            if href.startswith('#'):
                self.assertIn(href[1:], self.p.ids)
            elif not href.startswith('https:'):
                self.assertTrue((COURSE / href).is_file())

    def test_map_and_official_links_are_safe(self):
        maps = [a['href'] for a in self.p.links if 'map.naver.com' in a['href']]
        self.assertGreaterEqual(len(maps), 7)
        for url in maps:
            self.assertTrue(url.startswith('https://map.naver.com/p/search/'))
            self.assertEqual(urlsplit(url).query, '')
        for a in self.p.links:
            if a['href'].startswith('https:'):
                self.assertEqual(a.get('target'), '_blank')
                self.assertTrue({'noopener', 'noreferrer'} <= set(a.get('rel', '').split()))

    def test_responsive_and_sources(self):
        for term in ['name="viewport"', '@media(max-width:600px)', 'focus-visible',
                     'id="sources"', 'kumamoto-airport.co.jp', 'ichinoi.jp',
                     'fumotoryokan.com', 'okyakuya.jp', 'hotel-castle.co.jp',
                     'kumamoto-terrsa.com', 'hoshinoresorts.com', 'ogunitown.info']:
            self.assertIn(term, self.html)

    def test_wishlist_record_and_collections(self):
        data = (ROOT / 'assets/travel-records.js').read_text(encoding='utf-8')
        records = json.loads(data.split('window.travelRecords = ', 1)[1].strip().rstrip(';'))
        record = next(r for r in records if r['id'] == ID)
        self.assertEqual(record['group'], 'wishlist')
        self.assertEqual(record['region'], 'overseas')
        self.assertNotIn('start', record)
        self.assertEqual(record['ryokanCount'], 3)
        self.assertEqual(record['hotelCount'], 3)
        wishlist = [r for r in records if r['group'] == 'wishlist']
        self.assertEqual(len(wishlist), 20)
        self.assertEqual(sum(r['region'] == 'overseas' for r in wishlist), 2)
        for name in ['README.md', 'wishlist.html', 'index.html']:
            self.assertIn(ID, (ROOT / name).read_text(encoding='utf-8'))
        self.assertNotIn(f'data-record-id="{ID}"', (ROOT / 'history.html').read_text(encoding='utf-8'))
        versions = {re.search(r'travel-records\.js\?v=([^"]+)', (ROOT / name).read_text(encoding='utf-8')).group(1)
                    for name in ['index.html', 'history.html', 'wishlist.html']}
        self.assertEqual(len(versions), 1)


if __name__ == '__main__':
    unittest.main()
