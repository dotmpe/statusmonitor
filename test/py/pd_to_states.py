from pprint import pformat
import sys

import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.g = {"__main__": "unittest"}
        self.l = {}
        execfile("./bin/pd-to-states.py", self.g, self.l)

    def test_1_new_state(self):
        state = self.l['new_state']("Foo")
        self.assertEquals(state['label'], "Foo")
        self.assertEquals(state['status'], None)
        self.assertEquals(state['states'], [])

    def test_2_init_state(self):
        data = self.l['new_state']("Foo")
        self.assertEquals(data['label'], "Foo")
        state = self.l['init_state'](data, "Foo/Bar")
        self.assertEquals(data['states'][0]['label'], "Bar")



if __name__ == '__main__':

    unittest.main()

