import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from housing_watch.db import connect, init_db
from housing_watch.model_ledger import (FILES, SPEC_KEYS, collect_model_ledger, export_model_ledger,
    import_reviewed_models, parse_model_bundle, upsert_model_observations)
from housing_watch.model_research import CONFIG_PATH
from housing_watch.model_ledger_view import model_ledger_content


def bundle():
    cells = {"ordinal": "1", "provider": "Example", "model": "Aster", "kind": "모델", "context": "128K", "q4_ram": "32GB"}
    table = '<table id="tbl"><thead><tr>' + ''.join('<th>'+key+'</th>' for key in SPEC_KEYS) + '</tr></thead><tbody><tr>' + ''.join('<td>'+cells.get(key,'')+'</td>' for key in SPEC_KEYS) + '</tr></tbody></table>'
    model = {"sourceId": "aster-max", "model": "Aster", "name": "Aster (Max, Fallback)", "effort": "max", "provider": "Example", "contextTokens": 128000, "index": 58, "estimated": False,
             "automation": .7, "terminal": .6, "scicode": .5, "lcr": .8, "cost": 0, "source": "https://example.org/models/aster"}
    agent = {"sourceId": "agent-aster", "model": "Aster", "effort": "max", "provider": "Example", "harness": "CLI", "harnessVersion": "1.2", "index": 62, "deepSWE": 68, "terminalBench": 56, "sweAtlas": 62, "timeSeconds": 120, "totalTokens": 1000, "turns": 3, "costUsd": 2, "fallbackModels": ["Aster Small"]}
    documents = {
        "availability": {"verifiedAt": "2026-10-07", "scope": "CLI direct API", "models": [{"id": "aster", "name": "Aster", "provider": "Example", "tool": "cli", "status": "제한 제공", "context": "128K"}]},
        "models": {"suite": "AA v4.3.2", "benchmarkVersions": {"terminal": "4.0"}, "verifiedAt": "2026-10-07", "records": [model,dict(model,sourceId="aster-estimated",name="Aster (Low)",effort="low",estimated=True,index=30)]},
        "agents": {"suite": "Agent v1.5", "source": "https://example.org/agents", "verifiedAt": "2026-10-07", "benchmarkVersions": {"terminal": "4.0"}, "records": [agent]},
        "cursor": {"suite": "CursorBench 4.0", "source": "https://example.org/cursor", "verifiedAt": "2026-10-07", "records": [{"label": "Aster Max", "model": "Aster", "provider": "Example", "effort": "max", "score": 60, "costUsd": 3, "tokens": 400, "steps": 4}]},
        "workload": {"records": []},
    }
    guides = {"modelRows": [], "agentRows": []}
    bodies = {key: json.dumps(value).encode() for key,value in documents.items()}
    bodies["table"] = table.encode()
    bodies["guides"] = ('(function install(){})('+json.dumps(guides)+');').encode()
    return bodies


class ModelLedgerTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        init_db(self.conn)
        self.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        self.bodies = bundle()
        self.addCleanup(self.conn.close)

    def rows(self):
        return parse_model_bundle(self.bodies,self.config)

    def test_all_sources_keep_conditions_units_nulls_and_zero(self):
        records = self.rows()
        self.assertEqual(len(records),6)
        model = next(row for row in records if row["source_kind"]=="model" and row["fields"]["effort"]=="max")
        self.assertEqual(model["fields"]["automation"],70)
        self.assertEqual(model["fields"]["model_cost"],0)
        estimated = next(row for row in records if row["fields"].get("effort")=="low")
        self.assertIsNone(estimated["fields"]["intelligence"])
        self.assertEqual(estimated["fields"]["estimated_intelligence"],30)
        agent = next(row for row in records if row["source_kind"]=="agent")
        self.assertEqual(agent["fields"]["agent_minutes"],2)
        self.assertEqual(agent["fields"]["fallback_models"],["Aster Small"])
        cursor = next(row for row in records if row["source_kind"]=="cursor")
        self.assertEqual(cursor["fields"]["cursor_tokens"],400)
        self.assertNotIn("agent_tokens",cursor["fields"])
        spec = next(row for row in records if row["source_kind"]=="spec")
        self.assertIsNone(spec["fields"]["agent_index"])
        self.assertEqual(spec["fields"]["q4_ram"],"32GB")
        self.assertEqual(spec["checked_on"],"")

    def test_only_changed_record_revised_and_missing_preserved(self):
        rows = self.rows()
        first = upsert_model_observations(self.conn,rows,"2026-10-08T00:00:00Z")
        again = upsert_model_observations(self.conn,copy.deepcopy(rows),"2026-10-08T01:00:00Z")
        self.assertEqual((first["inserted"],again["unchanged"]),(6,6))
        changed = copy.deepcopy(rows)
        target=next(row for row in changed if row["source_kind"]=="cursor")
        target["fields"]["cursor_score"]=61
        result=upsert_model_observations(self.conn,changed,"2026-10-08T02:00:00Z")
        self.assertEqual((result["inserted"],result["updated"],result["unchanged"]),(0,1,5))
        history=export_model_ledger(self.conn)["history"]
        versions=[row for row in history if row["id"]==target["id"]]
        self.assertEqual([row["fields"]["cursor_score"] for row in sorted(versions,key=lambda row:row["revision"])],[60,61])
        result=upsert_model_observations(self.conn,changed[:-1],"2026-10-08T03:00:00Z")
        self.assertEqual(result["retained"],1)
        self.assertEqual(len(export_model_ledger(self.conn)["records"]),6)

    def test_new_suite_retains_previous_evaluation(self):
        upsert_model_observations(self.conn,self.rows())
        model=json.loads(self.bodies["models"])
        model["suite"]="AA v5.0"
        self.bodies["models"]=json.dumps(model).encode()
        result=upsert_model_observations(self.conn,self.rows())
        self.assertEqual((result["inserted"],result["retained"]),(2,2))
        self.assertEqual(len(export_model_ledger(self.conn)["records"]),8)

    def test_table_renumbering_does_not_create_model_changes(self):
        upsert_model_observations(self.conn,self.rows())
        self.bodies["table"]=self.bodies["table"].replace(b'<td>1</td>',b'<td>77</td>')
        result=upsert_model_observations(self.conn,self.rows())
        self.assertEqual((result["updated"],result["unchanged"]),(0,6))

    def test_workload_zero_denominators_and_unmeasured_are_distinct(self):
        row={"id":"workload-1","model":"Aster","effort":"max","harness":"CLI","workload":"sample repo","testSuite":"suite-1","measuredAt":"2026-10-07","source":"https://example.org/measurement","totalTasks":0,"completedTasks":0,"unassistedCompletedTasks":0,"regressionFreeCompletedTasks":0,"totalCostUsd":0}
        self.bodies["workload"]=json.dumps({"records":[row]}).encode()
        record=next(row for row in self.rows() if row["source_kind"]=="workload")
        self.assertIsNone(record["fields"]["unassisted"])
        self.assertIsNone(record["fields"]["success_cost"])
        row.update(totalTasks=10,completedTasks=5,unassistedCompletedTasks=3,regressionFreeCompletedTasks=4,totalCostUsd=20)
        self.bodies["workload"]=json.dumps({"records":[row]}).encode()
        record=next(row for row in self.rows() if row["source_kind"]=="workload")
        self.assertEqual((record["fields"]["unassisted"],record["fields"]["regression_free"],record["fields"]["success_cost"]),(30,40,4))

    def test_shared_json_change_detected_with_identical_html_and_generated_js(self):
        with tempfile.TemporaryDirectory() as directory,patch("housing_watch.model_ledger._read_material") as read:
            read.side_effect=[self.bodies[key] for key in FILES]
            first=collect_model_ledger(self.conn,directory)
            self.assertEqual(first["inserted"],6)
            agent=json.loads(self.bodies["agents"]);agent["records"][0]["costUsd"]=4
            self.bodies["agents"]=json.dumps(agent).encode()
            read.side_effect=[self.bodies[key] for key in FILES]
            result=collect_model_ledger(self.conn,directory)
            self.assertEqual((result["updated"],result["unchanged"]),(1,5))
            self.assertEqual(len(list(Path(directory).iterdir())),8)

    def test_bad_input_or_failure_leaves_entire_previous_snapshot(self):
        with tempfile.TemporaryDirectory() as directory,patch("housing_watch.model_ledger._read_material") as read:
            read.side_effect=[self.bodies[key] for key in FILES];collect_model_ledger(self.conn,directory)
            before=export_model_ledger(self.conn)["records"]
            self.bodies["table"]=b'<table id="tbl"><tr><td>changed columns</td></tr></table>'
            read.side_effect=[self.bodies[key] for key in FILES]
            with self.assertRaises(ValueError):collect_model_ledger(self.conn,directory)
            self.assertEqual(export_model_ledger(self.conn)["records"],before)
            self.assertFalse(export_model_ledger(self.conn)["runs"][0]["ok"])
            read.side_effect=OSError("offline")
            with self.assertRaises(ValueError):collect_model_ledger(self.conn,directory)
            self.assertEqual(export_model_ledger(self.conn)["records"],before)

    def test_duplicate_identity_rejected_before_change(self):
        document=json.loads(self.bodies["models"])
        document["records"].append(copy.deepcopy(document["records"][0]))
        self.bodies["models"]=json.dumps(document).encode()
        with self.assertRaises(ValueError):self.rows()

    def test_reviewed_facts_survive_upstream_sync_and_keep_revisions(self):
        document={"schema_version":1,"records":[{"id":"aster-official","model":"Aster","provider":"Example","source_url":"https://example.org/official","checked_on":"2026-10-08","fields":{"kind":"모델 사양","suite":"공식 사양","condition":"직접 API, 일반 제공","context":256000}}]}
        self.assertEqual(import_reviewed_models(self.conn,document)["inserted"],1)
        upsert_model_observations(self.conn,self.rows())
        row=next(item for item in export_model_ledger(self.conn)["records"] if item["source_kind"]=="reviewed")
        self.assertFalse(row["retained"])
        self.assertEqual(import_reviewed_models(self.conn,document)["unchanged"],1)
        document["records"][0]["fields"]["context"]=512000
        self.assertEqual(import_reviewed_models(self.conn,document)["updated"],1)
        document["records"][0]["source_url"]="javascript:alert(1)"
        with self.assertRaises(ValueError):import_reviewed_models(self.conn,document)

    def test_untrusted_text_stays_json_data_and_does_not_execute(self):
        upsert_model_observations(self.conn,self.rows())
        document=export_model_ledger(self.conn)
        document["records"][0]["model"]='</script><script>alert(1)</script>'
        content=model_ledger_content(document)
        self.assertNotIn('</script><script>alert(1)',content)
        self.assertIn('\\u003c/script>',content)


if __name__=="__main__":unittest.main()
