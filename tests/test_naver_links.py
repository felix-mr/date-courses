"""Regression checks for the October 14 dinner guide's verified Naver places.

Run from the repository root: python -m unittest discover -s tests -v
Place IDs were checked against names and addresses on Naver Maps on 2026-10-13.
These offline checks validate our links; they do not replace live map verification.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'courses/2026/2026-10-14-sanghyeon-gwanggyo-dinner'
# card ID: (display name, verified Naver place ID)
PLACES = {
    'yeomwon': ('염원', '2069833282'),
    'moromi': ('모로미쿠시 광교카페거리점', '37093123'),
    'hurahura': ('후라후라', '1852482619'),
    'baekjubang': ('백주방', '37209085'),
    'jutan': ('쥬탄', '2043795260'),
    'kitaya': ('키타야 수원광교점', '1369234214'),
    'suljipsanghyeon': ('술집상현', '1478986425'),
    'realpork': ('진짜돼지 광교상현점', '1515414659'),
    'lamb': ('화로양미 광교상현역점', '1709031061'),
    'chicken': ('신현리 숯불닭갈비', '1027336347'),
}


def place_url(place_id):
    return f'https://map.naver.com/p/entry/place/{place_id}'


class CardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = {}
        self.map_links = []
        self.card = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article' and 'food-card' in attrs.get('class', '').split():
            self.card = attrs['id']
            self.cards[self.card] = []
        if tag == 'a' and urlsplit(attrs.get('href', '')).hostname == 'map.naver.com':
            self.map_links.append(attrs)
            if self.card:
                self.cards[self.card].append(attrs)

    def handle_endtag(self, tag):
        if tag == 'article':
            self.card = None


class NaverLinksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (COURSE / 'course-options.html').read_text(encoding='utf-8')
        cls.readme = (COURSE / 'README.md').read_text(encoding='utf-8')
        cls.parser = CardParser()
        cls.parser.feed(cls.html)

    def test_each_card_targets_its_verified_place(self):
        self.assertEqual(set(self.parser.cards), set(PLACES))
        for card, (_, place_id) in PLACES.items():
            with self.subTest(card=card):
                links = self.parser.cards[card]
                self.assertEqual(len(links), 1)
                self.assertEqual(links[0]['href'], place_url(place_id))

    def test_readme_targets_the_same_place_by_restaurant(self):
        for name, place_id in PLACES.values():
            with self.subTest(restaurant=name):
                section = self.readme.split(f'### {name}\n', 1)[1].split('\n### ', 1)[0]
                links = re.findall(r'\[네이버 지도\]\(([^)]+)\)', section)
                self.assertEqual(links, [place_url(place_id)])

    def test_all_ten_map_links_are_direct_and_unique(self):
        for text in (self.html, self.readme):
            links = re.findall(r'https://map\.naver\.com/[^\s"\)<>]+', text)
            self.assertEqual(len(links), 10)
            self.assertEqual(len(set(links)), 10)
            for link in links:
                self.assertRegex(link, r'^https://map\.naver\.com/p/entry/place/\d+$')
                self.assertEqual(urlsplit(link).query, '')

    def test_external_map_buttons_are_safe(self):
        for link in self.parser.map_links:
            self.assertEqual(link.get('target'), '_blank')
            self.assertTrue({'noopener', 'noreferrer'} <= set(link.get('rel', '').split()))

    def test_guide_explains_direct_links(self):
        for text in (self.html, self.readme):
            self.assertNotIn('매장명과 주소를 포함한 검색 링크', text)
            self.assertIn('매장 상세로 바로 연결', text)


if __name__ == '__main__':
    unittest.main()
