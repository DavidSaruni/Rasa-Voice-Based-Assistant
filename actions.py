# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionProcessDonation(Action):
    def name(self) -> Text:
        return "action_process_donation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        amount = tracker.get_slot('AMOUNT')
        phone_number = tracker.get_slot('PHONE_NUMBER')
        # Call your payment processing API here
        dispatcher.utter_message(template="utter_confirm_donation", amount=amount)
        return []

class ActionConfirmDonation(Action):
    def name(self) -> Text:
        return "action_confirm_donation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_thanks")
        return []

class ActionCancelDonation(Action):
    def name(self) -> Text:
        return "action_cancel_donation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_donation_cancelled")
        return [SlotSet("AMOUNT", None), SlotSet("PHONE_NUMBER", None)]
