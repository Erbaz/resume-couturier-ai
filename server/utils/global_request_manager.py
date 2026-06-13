import os
import time
from threading import Lock
from google.cloud import firestore
from db.collections import daily_budget_collection
from classes.daily_budget import DailyBudget
from utils.get_la_start_of_day import get_la_start_of_day
from utils.pubsub_publisher import pubsub_publisher

class GlobalRequestManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GlobalRequestManager, cls).__new__(cls)
                    # Minute tracking
                    cls._instance.minute_start_time = time.time()
                    cls._instance.minute_request_count = 0
                    cls._instance.has_triggered_shutdown = False
                    
                    # Ensure document exists
                    cls._instance._init_daily_document()
        return cls._instance

    def _init_daily_document(self):
        docs = daily_budget_collection.limit(1).stream()
        doc_found = False
        for _ in docs:
            doc_found = True
            break
            
        if not doc_found:
            new_budget = DailyBudget()
            daily_budget_collection.add(new_budget.to_dict())

    def _get_daily_doc_ref(self):
        docs = daily_budget_collection.limit(1).stream()
        for doc in docs:
            return doc.reference, doc.to_dict()
        
        self._init_daily_document()
        docs = daily_budget_collection.limit(1).stream()
        for doc in docs:
            return doc.reference, doc.to_dict()
        return None, None

    def _check_and_reset_daily_budget(self, doc_data, doc_ref):
        current_la_start = get_la_start_of_day()
        # Firestore returns DatetimeWithNanoseconds which is a subclass of datetime
        doc_start = doc_data.get("starting_timestamp")
        
        # If dates differ, reset for the new day
        if not doc_start or doc_start.date() != current_la_start.date():
            new_budget = DailyBudget()
            doc_ref.update({
                "starting_timestamp": new_budget.starting_timestamp,
                "gemini_budget_utilized": 0.0,
                "number_of_requests": 0
            })
            return 0.0, 0 # Return reset values
        return doc_data.get("gemini_budget_utilized", 0.0), doc_data.get("number_of_requests", 0)

    def _check_limits_and_trigger(self, gemini_budget: float, num_requests: int):
        if self.has_triggered_shutdown:
            return True

        daily_budget_limit = float(os.getenv("DAILY_GEMINI_BUDGET", "0.5"))
        daily_req_limit = int(os.getenv("DAILY_TOTAL_REQUESTS", "5000"))
        minute_req_limit = int(os.getenv("MINUTE_RATE_LIMIT", "100"))


        # if gemini budget is exceeded, trigger shutdown
        # if daily total requests are exceeded, trigger shutdown
        # if minute rate limit is exceeded, trigger shutdown - suspicious because this many requests in one minute mean either a DDOS attack or a malicious actor trying to utilize the service with multiple accounts
        if (gemini_budget >= daily_budget_limit or 
            num_requests >= daily_req_limit or 
            self.minute_request_count >= minute_req_limit):
            
            print(f"[GLOBAL_LIMIT] Exceeded! Gemini: {gemini_budget}/{daily_budget_limit}, Daily Req: {num_requests}/{daily_req_limit}, Min Req: {self.minute_request_count}/{minute_req_limit}", flush=True)
            self.has_triggered_shutdown = True
            pubsub_publisher.publish_shutdown_event()
            return True

        print(f"[GLOBAL_LIMIT] Not Exceeded! Gemini: {gemini_budget}/{daily_budget_limit}, Daily Req={num_requests}/{daily_req_limit}, Min Req={self.minute_request_count}/{minute_req_limit}", flush=True)  
        return False

    def increment_global_request(self):
        """Increments minute and daily counters. Returns True if requests should be blocked."""
        with self._lock:
            current_time = time.time()
            if current_time - self.minute_start_time > 60:
                self.minute_start_time = current_time
                self.minute_request_count = 1
            else:
                self.minute_request_count += 1
                
        doc_ref, doc_data = self._get_daily_doc_ref()
        if not doc_ref:
            return False

        gemini_budget, num_requests = self._check_and_reset_daily_budget(doc_data, doc_ref)
        
        # Increment daily request
        doc_ref.update({"number_of_requests": firestore.Increment(1)})
        num_requests += 1

        return self._check_limits_and_trigger(gemini_budget, num_requests)

    def increment_gemini_budget(self, cost: float):
        """Increments the gemini utilized budget and checks limit."""
        doc_ref, doc_data = self._get_daily_doc_ref()
        if not doc_ref:
            return

        gemini_budget, num_requests = self._check_and_reset_daily_budget(doc_data, doc_ref)
        
        doc_ref.update({"gemini_budget_utilized": firestore.Increment(cost)})
        gemini_budget += cost
        
        self._check_limits_and_trigger(gemini_budget, num_requests)

    def get_current_state(self):
        """Returns the current gemini_budget_utilized and number_of_requests."""
        doc_ref, doc_data = self._get_daily_doc_ref()
        if not doc_ref:
            return 0.0, 0
        gemini_budget, num_requests = self._check_and_reset_daily_budget(doc_data, doc_ref)
        return gemini_budget, num_requests

global_request_manager = GlobalRequestManager()
