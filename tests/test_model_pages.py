import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from housing_watch.db import connect, init_db
from housing_watch.model_pages import load_page, upsert_pages, export_model_pages, collect_model_pages
from housing_watch.model_pages_view import source_document, library_content, render_model_pages, document_hash, load_learning_links
from housing_watch.research_data import load_report_input
from housing_watch.model_publication import apply_model_publication


HTML = '<!doctype html><html><head><title>Model</title><link rel="stylesheet" href="guide.css"></head><body><h1>Aster</h1><table><tr><td>60</td></tr></table><a href="Other.html">Other</a><script src="guide.js"></script></body></html>'


def page():
    return {'slug':'aster','file':'Aster.html','title':'Aster model','description':'Costs and coding','category':'모델 리서치','tags':['Aster'],
            'updated_on':'2026-10-08','reference_date':'2026-10-07','source_url':'https://theo-s-han.github.io/research-analysis/materials/Aster.html',
            'source_sha256':hashlib.sha256(HTML.encode()).hexdigest(),'source_kind':'theo-authored','html':HTML,
            'assets':{'guide.css':'body{color:red}','guide.js':'window.ready=true;'}}


class ModelPagesTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(':memory:'); init_db(self.conn); self.addCleanup(self.conn.close)

    def test_source_hash_and_dependency_contract(self):
        entry={'slug':'aster','file':'Aster.html','title':'Aster model','description':'Costs','category':'모델 리서치',
               'sha256':hashlib.sha256(HTML.encode()).hexdigest()}
        def fetch(url):
            return HTML.encode() if url.endswith('.html') else b'/* asset */'
        with tempfile.TemporaryDirectory() as root:
            doc=load_page(entry,{'site_url':'https://theo-s-han.github.io/research-analysis/'},root,fetch)
            self.assertEqual(set(doc['assets']),{'guide.js','guide.css'})
            entry['sha256']='a'*64
            with self.assertRaisesRegex(ValueError,'hash mismatch'): load_page(entry,{'site_url':'https://theo-s-han.github.io/research-analysis/'},root,fetch)
            entry['file']='../Escape.html'
            with self.assertRaises(ValueError): load_page(entry,{'site_url':'https://theo-s-han.github.io/research-analysis/'},root,fetch)

    def test_changed_only_and_assets_have_immutable_editions(self):
        doc=page();self.assertEqual(upsert_pages(self.conn,[doc])['inserted'],1)
        self.assertEqual(upsert_pages(self.conn,[doc])['unchanged'],1)
        changed=copy.deepcopy(doc);changed['assets']['guide.js']='window.ready=2;'
        self.assertEqual(upsert_pages(self.conn,[changed])['updated'],1)
        result=export_model_pages(self.conn)
        self.assertEqual(len(result['history']),2)
        self.assertEqual(result['history'][0]['document'],doc)
        self.assertEqual(result['pages'][0]['revision'],2)
        upsert_pages(self.conn,[])
        self.assertEqual(len(export_model_pages(self.conn)['pages']),1)

    def test_duplicate_batch_leaves_old_content(self):
        upsert_pages(self.conn,[page()])
        with self.assertRaises(ValueError):upsert_pages(self.conn,[page(),page()])
        self.assertEqual(len(export_model_pages(self.conn)['history']),1)

    def test_partial_fetch_preserves_previous_page(self):
        doc=page();upsert_pages(self.conn,[doc])
        catalog={'documents':[{'slug':'aster','title':'Aster','description':'Costs','category':'모델 리서치','sha256':'a'*64}]}
        with tempfile.TemporaryDirectory() as root,patch('housing_watch.model_pages._read_catalog',return_value=json.dumps(catalog).encode()),patch('housing_watch.model_pages.load_page',side_effect=OSError('offline')):
            with self.assertRaises(ValueError): collect_model_pages(self.conn,root)
        self.assertEqual(export_model_pages(self.conn)['pages'][0]['document'],doc)
        self.assertIn('offline',export_model_pages(self.conn)['runs'][0]['failures'][0])

    def test_content_sources_and_all_editions_render(self):
        doc=page();upsert_pages(self.conn,[doc]);changed=copy.deepcopy(doc);changed['html']=HTML.replace('60','61');upsert_pages(self.conn,[changed])
        result=export_model_pages(self.conn)
        text=source_document(doc,{'Other.html':'other'},'aster-r1')
        self.assertNotIn('src="guide.js"',text);self.assertIn('window.ready=true',text)
        self.assertIn('../other.html',text);self.assertIn("connect-src &#x27;none&#x27;",text)
        self.assertIn('Aster',library_content(result))
        with tempfile.TemporaryDirectory() as root:
            render_model_pages(root,result,lambda title,description,content,*args,**kwargs:content)
            old=Path(root,'model-guides/content/aster-r1.html').read_text(encoding='utf-8')
            current=Path(root,'model-guides/content/aster-r2.html').read_text(encoding='utf-8')
            self.assertIn('<td>60</td>',old);self.assertIn('<td>61</td>',current)
            wrapper=Path(root,'model-guides/aster.html').read_text(encoding='utf-8')
            self.assertIn('sandbox="allow-scripts',wrapper);self.assertNotIn('allow-same-origin',wrapper)

    def test_learning_companion_is_bound_to_whole_source_edition(self):
        doc = page(); upsert_pages(self.conn, [doc])
        guide = copy.deepcopy(load_report_input()[0])
        guide['id'] = 'model-reading-aster'
        guide['title'] = 'Distinct learning explanation'
        guide['explanation'] = [{'id':'meaning','title':'Meaning','lead':'Read the unit',
            'blocks':[{'type':'paragraph','kind':'example','title':'Case','text':'Companion example only','source_ids':[]}]}]
        links = {'aster':{'source_slug':'aster','report_id':guide['id'],'source_document_hash':document_hash(doc)}}
        stored_hash = self.conn.execute('SELECT content_hash FROM model_pages WHERE slug=?', ('aster',)).fetchone()[0]
        self.assertEqual(stored_hash, document_hash(doc))
        before = copy.deepcopy(doc)
        with tempfile.TemporaryDirectory() as root:
            result = export_model_pages(self.conn)
            render_model_pages(root, result, lambda title,description,content,*a,**kw:content, [guide], links)
            current = Path(root,'model-guides/aster.html').read_text(encoding='utf-8')
            historical = Path(root,'model-guides/aster-r1.html').read_text(encoding='utf-8')
            self.assertIn('Companion example only',current)
            self.assertIn('../model-reading-aster.html',current)
            self.assertIn('id="model-original"',current)
            self.assertNotIn('Companion example only',historical)
            self.assertIn('이 판의 별도 해설',historical)
            self.assertEqual(doc,before)
            # Shared JS changes alter the source edition even if HTML is unchanged.
            changed = copy.deepcopy(doc); changed['assets']['guide.js']='window.ready=2;'
            upsert_pages(self.conn,[changed])
            render_model_pages(root,export_model_pages(self.conn),lambda t,d,c,*a,**kw:c,[guide],links)
            stale = Path(root,'model-guides/aster.html').read_text(encoding='utf-8')
            self.assertNotIn('Companion example only',stale)
            self.assertIn('model-learning-stale',stale)
            self.assertIn('aster-r1.html',stale)
            original = Path(root,'model-guides/content/aster-r2.html').read_text(encoding='utf-8')
            self.assertIn('window.ready=2;',original)
            self.assertNotIn('Distinct learning explanation',original)
            # An absent guide must not create a broken publication link.
            render_model_pages(root,export_model_pages(self.conn),lambda t,d,c,*a,**kw:c,[],links)
            missing = Path(root,'model-guides/aster.html').read_text(encoding='utf-8')
            self.assertNotIn('../model-reading-aster.html',missing)

    def test_learning_mapping_rejects_traversal_and_duplicate_sources(self):
        entry={'source_slug':'aster','report_id':'model-reading-aster','source_document_hash':'a'*64}
        with tempfile.TemporaryDirectory() as root:
            path = Path(root,'links.json')
            path.write_text(json.dumps({'schema_version':1,'links':[entry]}),encoding='utf-8')
            self.assertEqual(load_learning_links(path)['aster'],entry)
            path.write_text(json.dumps({'schema_version':1,'links':[entry,entry]}),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Duplicate'):load_learning_links(path)
            entry['report_id']='../../escape'
            path.write_text(json.dumps({'schema_version':1,'links':[entry]}),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'identifiers'):load_learning_links(path)

    def test_reviewed_facts_publication_persists_once_and_rejects_mutation(self):
        facts={'schema_version':1,'records':[{'id':'aster','model':'Aster','provider':'Example','source_url':'https://example.org/aster','checked_on':'2026-10-08','fields':{'kind':'사양','suite':'official-release','condition':'Direct API','context':128000}}]}
        with tempfile.TemporaryDirectory() as root:
            path=Path(root,'manifest.json');source=Path(root,'aster.json')
            path.write_text(json.dumps({'schema_version':1,'batches':[{'id':'aster-2026','path':'aster.json'}]}));source.write_text(json.dumps(facts))
            apply_model_publication(self.conn,path);apply_model_publication(self.conn,path)
            self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM model_observation_revisions').fetchone()[0],1)
            facts['records'][0]['fields']['context']=256000;source.write_text(json.dumps(facts))
            with self.assertRaisesRegex(ValueError,'immutable batch'):apply_model_publication(self.conn,path)
            self.assertEqual(self.conn.execute('SELECT COUNT(*) FROM model_observation_revisions').fetchone()[0],1)

    def test_official_guides_join_source_library_with_correct_relative_links(self):
        upsert_pages(self.conn,[page()])
        source=export_model_pages(self.conn)
        guide={'id':'new-model-guide','topic_path':['개발 동향','AI 모델·API','New'],
               'title':'New & model','description':'Official <facts>', 'checked_on':'2026-10-09'}
        unrelated=dict(guide,id='unrelated-model-guide',topic_path=['사업','영업'])
        html=library_content(source,'../../../preview/',[guide,unrelated])
        self.assertIn('href="../../../preview/new-model-guide.html"',html)
        self.assertIn('New &amp; model',html);self.assertIn('Official &lt;facts&gt;',html)
        self.assertIn('data-label="공식 원문 확인일">2026-10-09',html)
        self.assertIn('model-guides/aster.html',html)
        self.assertNotIn('unrelated-model-guide.html',html)
        with tempfile.TemporaryDirectory() as root:
            render_model_pages(root,source,lambda title,description,content,*args,**kwargs:content,[guide])
            rendered=Path(root,'ai-model-guides.html').read_text(encoding='utf-8')
            self.assertIn('href="new-model-guide.html"',rendered)

    def test_library_count_includes_official_guides_without_double_counting_topic(self):
        from housing_watch.editorial import _tree
        guide={'id':'new-model-guide','topic_id':'opportunities',
               'topic_path':['개발 동향','AI 모델·API','New']}
        html=_tree([guide],'',has_model_ledger=True,model_page_count=14,model_library_count=15)
        self.assertIn('모델별 가이드·평가 자료</span><small>15</small>',html)
        self.assertIn('AI 모델·API</span> <small>16</small>',html)

