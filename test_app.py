import unittest
import app
import threading
import urllib.request
import urllib.error

class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.c = app.config()
        self.model = app.fit([r for r in app.rows() if r['order_datetime'][:7] < '2026-09'])

    def test_normalization(self):
        self.assertEqual(app.outcome({'final_status': ' Rto '}), 1)
        self.assertEqual(app.outcome({'final_status': 'delivered'}), 0)
        self.assertIsNone(app.outcome({'final_status': 'IN_TRANSIT'}))

    def test_identical_csv_duplicates_are_counted_once(self):
        records = app.rows()
        self.assertEqual(len(records), 1988)
        self.assertEqual(sum(r['order_id'] == 'KT100329' for r in records), 1)

    def test_boundaries(self):
        for p, bucket in [(0.249,0),(0.25,1),(0.35,2),(0.60,3)]:
            self.assertEqual(app.decide({}, {'new':p}, self.c)['bucket'], bucket)

    def test_segment_and_hold_economics(self):
        d = app.decide({'customer_prior_orders':'3','customer_prior_rto':'2'}, {'prior_rto_2plus':0.7}, self.c)
        self.assertEqual(d['bucket'], 3)
        s,l,cost=app.impact(d, 649, self.c)
        self.assertAlmostEqual(s, 0.7*169.4)
        self.assertAlmostEqual(l, 0.3*649*0.62)
        self.assertEqual(cost, 0)

    def test_no_key_not_verified(self):
        from unittest.mock import patch
        with patch.dict('os.environ', {}, clear=True):
            self.assertIn('Not checked', app.llm_check({'address':'test'}))

    def test_latest_month(self):
        data=[r for r in app.rows() if r['order_datetime'][:7]=='2026-09' and app.outcome(r) is not None]
        self.assertEqual(len(data),329)
        self.assertEqual(sum(app.report(data, self.model, self.c)['counts']),329)

    def test_page_has_keyboard_skip_link_and_main_landmark(self):
        rendered = app.page('Test', '<p>Content</p>').decode('utf-8')
        self.assertIn('href="#main"', rendered)
        self.assertIn('<main id="main"', rendered)

    def test_prepaid_nonconverters_follow_confirmation_scenario(self):
        d = {'risk': 0.5, 'bucket': 2}
        s, loss, discount = app.impact(d, 100, self.c)
        # 30% prepaid; remaining 70% require confirmation.
        expected_rto = .30*.04 + .70*.70*.5*.65
        expected_delivered = .30*.96 + .70*.70*(1-.5*.65)
        self.assertAlmostEqual(s, (.5 - expected_rto)*169.4)
        self.assertAlmostEqual(loss, (.5 - expected_delivered)*62)
        self.assertAlmostEqual(discount, 9)

    def test_confirmation_can_increase_expected_delivered_contribution(self):
        c = dict(self.c, confirmation_reply_rate=1, confirmed_rto_multiplier=.5)
        s, loss, discount = app.impact({'risk': .5, 'bucket': 1}, 100, c)
        self.assertAlmostEqual(loss, -15.5)

    def test_address_review_escalates_ship_to_confirmation(self):
        model = {'repeat': .10}
        row = {'customer_prior_orders': '1', 'customer_prior_rto': '0'}
        d = app.decide(row, model, self.c, address_review='needs_clarification')
        self.assertEqual(d['bucket'], 1)
        self.assertIn('address', d['reason'].lower())

    def test_unavailable_address_review_does_not_invent_a_flag(self):
        d = app.decide({'customer_prior_orders':'1'}, {'repeat': .10}, self.c, address_review='unavailable')
        self.assertEqual(d['bucket'], 0)

class SampleOrdersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = app.ThreadingHTTPServer(('127.0.0.1', 0), app.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_sample_list_displays_csv_and_allows_search(self):
        with urllib.request.urlopen(self.base + '/samples?q=KT100193') as response:
            body = response.read().decode()
        self.assertIn('KT100193', body)
        self.assertIn('DELIVERED', body)
        self.assertNotIn('KT101714', body)

    def test_sample_detail_explains_recommendation_without_logging(self):
        before = (app.ROOT / 'decisions.jsonl').read_bytes() if (app.ROOT / 'decisions.jsonl').exists() else None
        with urllib.request.urlopen(self.base + '/samples?order=KT100193') as response:
            body = response.read().decode()
        self.assertIn('KT100193', body)
        self.assertIn('Ship after confirmation', body)
        self.assertIn('DELIVERED', body)
        after = (app.ROOT / 'decisions.jsonl').read_bytes() if (app.ROOT / 'decisions.jsonl').exists() else None
        self.assertEqual(before, after)

if __name__ == '__main__': unittest.main()
