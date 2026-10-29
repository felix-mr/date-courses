"""Offline regression checks for the October 29 pasta guide.

Run: python -m unittest discover -s tests -v
Live opening hours and availability must be rechecked separately.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ID = '2026-10-29-sanghyeon-pasta'
COURSE = ROOT / 'courses' / '2026' / ID
PLACES = {
    'contenente': '1044133099', 'winefine': '1553731183',
    'forkner': '2097653986', 'rootstay': '1239797531',
    'snail': '1241304381', 'onyou': '1110613449',
}


class GuideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.cards = {}
        self.links = []
        self.card = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'article':
            self.card = attrs['id']
            self.cards[self.card] = []
        if tag == 'a':
            self.links.append(attrs)
            if self.card:
                self.cards[self.card].append(attrs)

    def handle_endtag(self, tag):
        if tag == 'article':
            self.card = None


class PastaGuideTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (COURSE / 'course-options.html').read_text()
        cls.md = (COURSE / 'README.md').read_text()
        cls.parser = GuideParser()
        cls.parser.feed(cls.html)

    def test_six_verified_map_targets(self):
        self.assertEqual(set(self.parser.cards), set(PLACES))
        for card, place in PLACES.items():
            maps = [a['href'] for a in self.parser.cards[card]
                    if urlsplit(a['href']).hostname == 'map.naver.com']
            expected = f'https://map.naver.com/p/entry/place/{place}'
            self.assertEqual(maps, [expected])
            self.assertIn(expected, self.md)

    def test_unique_ids_and_working_anchors(self):
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))
        for link in self.parser.links:
            href = link['href']
            if href.startswith('#'):
                self.assertIn(href[1:], self.parser.ids)

    def test_external_links_are_safe(self):
        for link in self.parser.links:
            if link['href'].startswith('https://'):
                self.assertEqual(link.get('target'), '_blank')
                self.assertTrue({'noopener', 'noreferrer'} <= set(link.get('rel', '').split()))

    def test_uncertainties_and_price_ranges_are_explicit(self):
        for text in [self.html, self.md]:
            for term in ['예약 확정', '라스트오더 미확인', '출처 상충',
                         '외부 케이크', '25,800–31,800원', '13:33 KST',
                         '13:44 KST', '13:46 KST', '좌석을 준비하지 못할 수 있음']:
                self.assertIn(term, text)

    def test_schedule_metadata_and_collection_coverage(self):
        data = (ROOT / 'assets/travel-records.js').read_text()
        records = json.loads(data.split('window.travelRecords = ', 1)[1].rstrip().rstrip(';'))
        ids = [r['id'] for r in records]
        self.assertEqual(len(ids), len(set(ids)))
        record = next(r for r in records if r['id'] == ID)
        self.assertEqual(record['end'], '2026-10-29')
        self.assertEqual(record['restaurantCount'], 6)
        self.assertEqual(record['reservationStatus'], 'undecided')
        for name in ['index.html', 'history.html']:
            text = (ROOT / name).read_text()
            self.assertEqual(text.count(f'data-record-id="{ID}"'), 1)
        for name in ['index.html', 'history.html', 'wishlist.html']:
            self.assertIn('travel-records.js?v=20261029-pasta', (ROOT / name).read_text())


if __name__ == '__main__':
    unittest.main()
