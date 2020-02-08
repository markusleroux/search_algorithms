import unittest
from string_search_algorithms import naiveSearch, KMPSearch

def makeTest(function):

    class Test_Search(unittest.TestCase):

        def test_noMatch(self):
            pat = "abc"
            txt = "defghijk"
            self.assertEqual(function(pat, txt), [])

        def test_empty(self):
            pat = "abc"
            txt = ""
            self.assertEqual(function(pat, txt), [])

        def test_last(self):
            pat = "olleh"
            txt = "hellolleh"
            self.assertEqual(function(pat, txt), [4])

        def test_overlap(self):
            pat = "aba"
            txt = "ababababac"
            self.assertEqual(function(pat, txt), [0,2,4,6])

    return Test_Search



class TestNaiveImplementation(makeTest(naiveSearch)):
    pass

class TestKMPImplementation(makeTest(KMPSearch)):
    pass



            