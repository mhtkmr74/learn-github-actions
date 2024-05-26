import json 
from constants import RULES_FILENAME
from email_handler.fetch_email import fetch_service_object
from email_db_handler.email_db_utils import fetch_email_from_db

def get_rules():
    all_rules = []
    file = open(RULES_FILENAME)
    rules = json.load(file)
    for rule in rules:
        all_rules.append(rule)
    return all_rules


def filter_rules():
    rules = get_rules()
    rules_with_all_collection_match = []
    rules_with_any_collection_match = []
    for rule in rules:
        if rule["collection_predicate"] == "All":
            rules_with_all_collection_match.append(rule)
        else:
            rules_with_any_collection_match.append(rule)
    return rules_with_all_collection_match, rules_with_any_collection_match


def take_action_on_email(email, actions):
    service = fetch_service_object()
    service.users().messages().modify(
        userId='me',
        id=email["email_id"],
        body={
            'removeLabelIds': ['INBOX'],
            'addLabelIds': actions["move_to_folder"]
        }).execute()


def check_if_all_condition_matches(email, conditions):
    for condition in conditions:
        if condition["predicate"] == "contains":
            if condition["value"] in email[condition["field"]]:
                continue
            else:
                return False
    return True 


def apply_all_predicate_rule_on_email(email, all_mandatory_match_rules):
    for rule in all_mandatory_match_rules:
        condition = rule["conditions"]
        if check_if_all_condition_matches(email, condition):
            take_action_on_email(email, rule["actions"])
    return
            

def check_if_any_condition_matches(email, conditions):
    for condition in conditions:
        if condition["predicate"] == "contains":
            if condition["value"] in email[condition["field"]]:
                return True
            else:
                continue
    return False 


def apply_any_predicate_rule_on_email(email, all_mandatory_match_rules):
    for rule in all_mandatory_match_rules:
        condition = rule["conditions"]
        if check_if_any_condition_matches(email, condition):
            take_action_on_email(email, rule["actions"])
    return


def apply_rules_on_email(email):
    all_mandatory_match_rules, any_optional_match_rule = filter_rules()
    apply_all_predicate_rule_on_email(email, all_mandatory_match_rules)
    apply_any_predicate_rule_on_email(email, any_optional_match_rule)


def get_emails():
    emails = fetch_email_from_db()
    for email in emails:
        apply_rules_on_email(email)

