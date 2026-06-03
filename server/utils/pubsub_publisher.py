import os
import json
from google.cloud import pubsub_v1
from dotenv import load_dotenv

load_dotenv()

class PubSubPublisher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PubSubPublisher, cls).__new__(cls)
            cls._instance.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
            cls._instance.topic_id = os.getenv("TOPIC_ID")
            
            if cls._instance.project_id and cls._instance.topic_id:
                try:
                    cls._instance.publisher = pubsub_v1.PublisherClient()
                    cls._instance.topic_path = cls._instance.publisher.topic_path(
                        cls._instance.project_id, cls._instance.topic_id
                    )
                except Exception as e:
                    print(f"[PUBSUB] Failed to initialize PublisherClient: {e}", flush=True)
                    cls._instance.publisher = None
            else:
                cls._instance.publisher = None
        return cls._instance

    def publish_shutdown_event(self):
        """Publishes the shutdown event to the topic to scale the service to 0."""
        if not self.publisher or not self.project_id or not self.topic_id:
            print("[PUBSUB] Cannot publish event: PublisherClient not initialized or missing env vars.", flush=True)
            return False

        payload = {"trusted": True}
        data_str = json.dumps(payload)
        data = data_str.encode("utf-8")

        try:
            future = self.publisher.publish(self.topic_path, data)
            message_id = future.result(timeout=10)
            print(f"[PUBSUB] Published shutdown event message ID: {message_id}", flush=True)
            return True
        except Exception as e:
            print(f"[PUBSUB] Failed to publish shutdown event: {e}", flush=True)
            return False

pubsub_publisher = PubSubPublisher()
