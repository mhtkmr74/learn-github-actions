import unittest
from unittest.mock import patch
from email_handler.email_processor import filter_rules, check_if_all_condition_matches


class TestCheckIfAllConditionMatches(unittest.TestCase):

    def test_all_conditions_match(self):
        email = {"subject": "Facebook interview"}
        conditions = [
            {
                "field": "subject",
                "predicate": "contains",
                "value": "Facebook"
            },
            {
                "field": "subject",
                "predicate": "contains",
                "value": "interview"
            }
        ]
        result = check_if_all_condition_matches(email, conditions)
        self.assertTrue(result)

    def test_one_condition_does_not_match(self):
        email = {"subject": "Facebook interview"}
        conditions = [
            {
                "field": "subject",
                "predicate": "contains",
                "value": "Facebook"
            },
            {
                "field": "subject",
                "predicate": "contains",
                "value": "social"
            }
        ]
        result = check_if_all_condition_matches(email, conditions)
        self.assertFalse(result)

    def test_empty_conditions(self):
        email = {"subject": "Facebook interview"}
        conditions = []
        result = check_if_all_condition_matches(email, conditions)
        self.assertTrue(result)

    def test_empty_email_field(self):
        email = {"subject": ""}
        conditions = [
            {
                "field": "subject",
                "predicate": "contains",
                "value": "Facebook"
            }
        ]
        result = check_if_all_condition_matches(email, conditions)
        self.assertFalse(result)


class TestFilterRules(unittest.TestCase):

    @patch('email_handler.email_processor.get_rules')
    def test_filter_rules(self, mock_get_rules):
        mock_get_rules.return_value = [
            {"id": 1, "collection_predicate": "All", "conditions": []},
            {"id": 2, "collection_predicate": "Any", "conditions": []},
            {"id": 3, "collection_predicate": "All", "conditions": []},
            {"id": 4, "collection_predicate": "Any", "conditions": []}
        ]

        all_collection, any_collection = filter_rules()

        expected_all_collection = [
            {"id": 1, "collection_predicate": "All", "conditions": []},
            {"id": 3, "collection_predicate": "All", "conditions": []}
        ]
        expected_any_collection = [
            {"id": 2, "collection_predicate": "Any", "conditions": []},
            {"id": 4, "collection_predicate": "Any", "conditions": []}
        ]

        self.assertEqual(all_collection, expected_all_collection)
        self.assertEqual(any_collection, expected_any_collection)

    @patch('email_handler.email_processor.get_rules')
    def test_filter_rules_empty(self, mock_get_rules):
        mock_get_rules.return_value = []

        all_collection, any_collection = filter_rules()

        expected_all_collection = []
        expected_any_collection = []

        self.assertEqual(all_collection, expected_all_collection)
        self.assertEqual(any_collection, expected_any_collection)

    @patch('email_handler.email_processor.get_rules')
    def test_filter_rules_only_all(self, mock_get_rules):
        mock_get_rules.return_value = [
            {"id": 1, "collection_predicate": "All", "conditions": []},
            {"id": 2, "collection_predicate": "All", "conditions": []}
        ]

        all_collection, any_collection = filter_rules()

        expected_all_collection = [
            {"id": 1, "collection_predicate": "All", "conditions": []},
            {"id": 2, "collection_predicate": "All", "conditions": []}
        ]
        expected_any_collection = []

        self.assertEqual(all_collection, expected_all_collection)
        self.assertEqual(any_collection, expected_any_collection)

    @patch('email_handler.email_processor.get_rules')
    def test_filter_rules_only_any(self, mock_get_rules):
        mock_get_rules.return_value = [
            {"id": 1, "collection_predicate": "Any", "conditions": []},
            {"id": 2, "collection_predicate": "Any", "conditions": []}
        ]

        all_collection, any_collection = filter_rules()

        expected_all_collection = []
        expected_any_collection = [
            {"id": 1, "collection_predicate": "Any", "conditions": []},
            {"id": 2, "collection_predicate": "Any", "conditions": []}
        ]

        self.assertEqual(all_collection, expected_all_collection)
        self.assertEqual(any_collection, expected_any_collection)
