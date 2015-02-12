#!/usr/bin/env python
# encoding: utf-8

from doxx.utilities.fuzzysearch import FuzzySearcher

possibilities = ["license-mit", "license-gpl", "license-apache", "license-apacho", "html-initializr", "bogus-stuff", "another-tool", "meager-banish", "test-code", "test-code-thing", "test-code-longstring", "either-or", "project-good", "tapas-food", "pizza-beer", "coke-soda", "monster-blue", "longer-string-sample", "bad-string-sample-error", "big-sample-string-tester", "test-mit-license", "bogus-mit-string"]
match_attempt = "sample string"

print("Match String: '" + match_attempt + "'")
print(" ")

fuzzy = FuzzySearcher(match_attempt)
for test_string in possibilities:
    print(test_string + " : " + str(fuzzy.partial_set_ratio(test_string)))
    