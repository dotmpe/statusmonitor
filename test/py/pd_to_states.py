import pprint
from pprint import pformat
import sys

import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.g = globals()
        self.l = locals()

        if 'get_comp' not in self.l:
            self.g['__name__'] = "unittest"
            execfile("./bin/pd-to-states.py", self.g, self.l)
            globals().update(self.l)


    def test_1_new_state(self):

        state = new_state("Foo")
        self.assertEquals(state['label'], "Foo")
        self.assertEquals(state['status'], None)
        self.assertEquals(state['states'], [])

    def test_2_setup(self):

        data = new_state("Foo", [ new_state("Bar") ] )
        self.assertEquals( len(data['states']), 1 )
        self.assertEquals( data['label'], 'Foo' )

        comp = get_comp(data, 'Bar')
        self.assertEquals( comp['label'], 'Bar' )
        self.assertEquals( len(data['states']), 1 )
        self.assertEquals( len(comp['states']), 0 )

        new_comp = new_state("Baz")
        self.assertEquals( len(new_comp['states']), 0 )
        data['states'].append( new_comp )
        comp = get_comp(data, 'Baz')
        self.assertEquals( comp['label'], 'Baz' )
        self.assertEquals( len(comp['states']), 0 )
        self.assertEquals( len(data['states']), 2 )


    def test_3_set_path(self):

        data = new_state("Foo")

        self.assert_( data['label'] == 'Foo' )
        self.assert_( len(data['states']) == 0 )
        self.assert_( data['status'] == None )

        state = set_path(data, 'foo/bar', 'init', 0)
        self.assertEquals(state['label'], "Init")

        self.assert_( data['label'] == 'Foo' )
        self.assert_( len(data['states']) > 0 )
        self.assert_( data['states'][0]['label'] == 'Bar' )

        self.assert_( len(data['states'][0]['states']) == 1 )
        self.assert_( len(data['states']) == 1 )

        state = set_path(data, 'foo/bar', 'check', 0)
        self.assert_( len(data['states']) == 1 )
        self.assert_( len(data['states'][0]['states']) == 2 )


    def test_4_set_states(self):
        pass

    def test_5_init_state(self):

        data = new_state("Foo")
        self.assertEquals(data['label'], "Foo")

        state = init_state(data, "Bar")
        self.assertEquals(state['label'], "Bar")
        self.assert_( len(data['states']) == 1 )
        self.assertEquals(data['states'][0]['label'], "Bar")



if __name__ == '__main__':

    unittest.main()

