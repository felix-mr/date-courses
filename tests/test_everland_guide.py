"""Offline structure and content checks; live app inventory is not tested."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'courses/2026/2026-11-03-yongin-everland'
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.cards=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a)
        if tag=='article' and 'option-card' in a.get('class','').split():self.cards+=1
class EverlandGuideTest(unittest.TestCase):
    def setUp(self):
        self.html=(COURSE/'course-options.html').read_text();self.md=(COURSE/'README.md').read_text()
        self.p=Parser();self.p.feed(self.html)
    def test_anchors_and_local_files(self):
        self.assertEqual(len(self.p.ids),len(set(self.p.ids)))
        for a in self.p.links:
            href=a['href']
            if href.startswith('#'):self.assertIn(href[1:],self.p.ids)
            elif not href.startswith('https:'):self.assertTrue((COURSE/href).is_file())
    def test_external_links(self):
        for a in self.p.links:
            if a['href'].startswith('https:'):
                self.assertEqual(a.get('target'),'_blank')
                self.assertTrue({'noopener','noreferrer'}<=set(a.get('rel','').split()))
    def test_existing_options_preserved(self):
        self.assertEqual(self.p.cards,30)
        for title in ['transport','entry','route','options','closing','tips','smart-queue']:self.assertIn(title,self.p.ids)
    def test_queue_content_and_sources(self):
        for s in [self.html,self.md]:
            for term in ['동반인','입장 완료','이용시간','현장 줄서기','2026','everedu_mobile_service_faq_2024.pdf','reservation.everland.com/web/main.do?method=guide']:
                self.assertIn(term,s)
        self.assertIn('name="viewport"',self.html)
        self.assertIn('@media(max-width:600px)',self.html)
