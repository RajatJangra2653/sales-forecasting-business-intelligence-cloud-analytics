import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

class DashboardTests(unittest.TestCase):
    def test_demo_and_forecast_render(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=60)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.metric), 4)
        app.toggle[0].set_value(True).run(timeout=120)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.success), 1)
        app.slider[0].set_value(10).run(timeout=120)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.success), 1)

if __name__ == '__main__': unittest.main()
