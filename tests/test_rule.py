import unittest
from safeGPT.rules import *
import os


class TestRules(unittest.TestCase):
    @unittest.skipIf(os.environ.get('OPENAI_KEY') is not None, 'OPENAI_KEY is not set')
    def setUp(self) -> None:
        from dotenv import load_dotenv
        load_dotenv()
        safeGPT.api_key=os.environ.get('OPENAI_KEY')

    def test_openai_moderation(self):
        rule = OpenAIModeration(categories=['hate'])
        self.assertTrue(rule.check('I hate people from Mars!'))
        self.assertFalse(rule.check('I love you!'))

    def test_keyword_detection(self):
        rule = KeywordDetection(keywords=['spam', 'coke'])
        self.assertTrue(rule.check('Buy cheap coke now!'))
        self.assertFalse(rule.check('This is not scam.'))

    def test_regex_match(self):
        rule = RegexSearch(regex=r'iPhone\s\d+')
        self.assertTrue(rule.check('s iPhone 1s ss'))
        self.assertFalse(rule.check('iPad Pro is expensive.'))

    def test_do_not_check(self):
        rule = DoNotFlag()
        self.assertFalse(rule.check('Anything'))

    def test_custom_rule_decorator(self):
        @custom_rule
        def some_rule(input_text: str) -> bool:
            return input_text == 'custom'
        self.assertTrue(some_rule.check('custom'))
        self.assertTrue(isinstance(some_rule, Rule))
        self.assertFalse(some_rule.check('anything'))

    def test_custom_rule_decorator_with_not_bool_return(self):
        @custom_rule
        def some_rule(input_text: str) -> str:
            return input_text
        with self.assertRaises(ValueError):
            some_rule.check('custom')

    def test_custom_rule_decorator_with_no_return(self):
        @custom_rule
        def some_rule(input_text: str):
            pass
        with self.assertRaises(ValueError):
            some_rule.check('custom')

    def test_custom_rule_decorator_with_improper_input(self):
        @custom_rule
        def some_rule(a, b):
            return a == b
        with self.assertRaises(ValueError):
            some_rule.check('custom')

    def test_sequential_check(self):
        rule1 = RegexSearch(regex=r'iPhone\s\d+')
        rule2 = KeywordDetection(keywords=['dog', 'cat'])
        rule3 = DoNotFlag()
        rule4 = OpenAIModeration()
        rule_seq = SequentialCheck([rule1, rule2, rule3, rule4])
        self.assertTrue(rule_seq.check('I love iPhone 12'))
        self.assertTrue(rule_seq.check('Buy cat with iPad now!'))
        self.assertFalse(rule_seq.check('I hate people!'))
        self.assertFalse(rule_seq.check('This is a good post.'))


    def test_invalid_openai_moderation_category(self):
        with self.assertRaises(ValueError):
            OpenAIModeration(categories=['invalid'])

    def test_invalid_sequential_check(self):
        with self.assertRaises(ValueError):
            SequentialCheck([DoNotFlag(), 'invalid'])

    def test_invalid_regex(self):
        with self.assertRaises(ValueError):
            RegexSearch(regex='(')


if __name__ == '__main__':
    unittest.main()