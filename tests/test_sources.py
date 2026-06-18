import unittest

from housing_watch.sources import parse_seoul_housing_table


class SourceParserTests(unittest.TestCase):
    def test_parse_lh_table_row(self):
        source = {
            "id": "seoul_lh_public_lease",
            "layout": "lh",
            "agency": "LH",
            "url": "https://housing.seoul.go.kr/site/main/lh/publicLease/list",
        }
        html = """
        <table><tbody>
          <tr>
            <td>2635</td><td>행복주택</td>
            <td>[정정공고]목포 행복주택 예비입주자 모집</td>
            <td>전라남도</td><td>2026-06-17</td><td>2026-07-02</td>
            <td>정정공고중</td>
            <td><a href="https://apply.lh.or.kr/detail">바로가기</a></td>
          </tr>
        </tbody></table>
        """
        items = parse_seoul_housing_table(source, html)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "행복주택")
        self.assertEqual(items[0]["region"], "전라남도")
        self.assertEqual(items[0]["deadline_at"], "2026-07-02")

    def test_parse_sh_table_row(self):
        source = {
            "id": "seoul_sh_public_lease",
            "layout": "sh",
            "agency": "SH",
            "region": "서울",
            "url": "https://housing.seoul.go.kr/site/main/sh/publicLease/07/list",
        }
        html = """
        <table><tbody>
          <tr>
            <td>8</td><td>행복주택</td>
            <td>2026년 1차 서울주택도시개발공사 행복주택 입주자 모집공고</td>
            <td>2026-05-28</td><td>2026-10-30</td>
            <td>모집중</td><td>공공주택공급부</td>
            <td><a href="https://www.i-sh.co.kr/notice">바로가기</a></td>
          </tr>
        </tbody></table>
        """
        items = parse_seoul_housing_table(source, html)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["agency"], "SH")
        self.assertEqual(items[0]["region"], "서울")
        self.assertEqual(items[0]["status"], "모집중")


if __name__ == "__main__":
    unittest.main()

