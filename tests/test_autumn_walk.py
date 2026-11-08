"""Offline checks for the November walking candidates; no live inventory claims."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, unittest
ROOT=Path(__file__).resolve().parents[1]
ID='2026-11-08-gyeonggi-autumn-walk'
COURSE=ROOT/'courses/2026'/ID
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.ids=[];self.links=[];self.cards=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a':self.links.append(a)
  if tag=='article' and 'walk-card' in a.get('class','').split():self.cards+=1
class AutumnWalkTest(unittest.TestCase):
 def setUp(self):
  self.html=(COURSE/'course-options.html').read_text();self.md=(COURSE/'README.md').read_text();self.p=Parser();self.p.feed(self.html)
 def test_four_cards_and_uncertainty(self):
  self.assertEqual(self.p.cards,4)
  self.assertRegex(self.md,r'날짜:? 미정')
  for text in [self.html,self.md]:
   for term in ['물향기수목원','남한산성','용인자연휴양림','용인농촌테마파크','미확인','추정','2026','16:30','16:00']:
    self.assertIn(term,text)
   self.assertNotRegex(text,r'\d[\d,]*\s*원(?!삼면)')
 def test_unique_anchors_and_local_files(self):
  self.assertEqual(len(self.p.ids),len(set(self.p.ids)))
  for a in self.p.links:
   h=a['href']
   if h.startswith('#'):self.assertIn(h[1:],self.p.ids)
   elif not h.startswith('https:'):self.assertTrue((COURSE/h).is_file())
 def test_map_details_and_safe_external_links(self):
  map_urls=[a['href'] for a in self.p.links if 'map.naver.com' in a['href']]
  self.assertEqual(set(map_urls),{'https://map.naver.com/p/entry/place/'+id for id in ['35195643','18292884','13179328','13327760']})
  for a in self.p.links:
   if a['href'].startswith('https:'):
    self.assertEqual(a.get('target'),'_blank');self.assertTrue({'noopener','noreferrer'}<=set(a.get('rel','').split()))
 def test_wishlist_and_home_links(self):
  records=json.loads((ROOT/'assets/travel-records.js').read_text().split('window.travelRecords = ',1)[1].strip().rstrip(';'))
  record=next(r for r in records if r['id']==ID)
  self.assertEqual(record['group'],'wishlist');self.assertNotIn('start',record);self.assertEqual(record['placeCount'],4)
  self.assertEqual(sum(r['group']=='wishlist' for r in records),19)
  for path in ['README.md','wishlist.html','index.html']:self.assertIn(ID,(ROOT/path).read_text())
  self.assertNotIn('data-record-id="'+ID+'"',(ROOT/'history.html').read_text())
 def test_responsive_and_sources(self):
  for term in ['name="viewport"','@media(max-width:600px)','focus-visible','id="sources"','forest.gg.go.kr','foresttrip.go.kr','yongin.go.kr','kh.or.kr']:
   self.assertIn(term,self.html)
if __name__=='__main__':unittest.main()
