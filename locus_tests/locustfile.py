from locust import HttpUser, task, between
import random
import uuid
from datetime import datetime

class TaskEventUser(HttpUser):
    wait_time = between(1, 3)  # simulate user "think time" between requests

    # Replace this with the actual cloud function endpoint if not using the default host
    def on_start(self):
        self.endpoint = "/notify_task_event"  # this is ignored when using full URL in host

    @task(2)
    def create_task(self):
        """Simulates creating a task"""
        self.client.post(
            url="https://us-central1-taskmanager-project-460020.cloudfunctions.net/notify_task_event",
            json={
                "task_id": str(uuid.uuid4()),
                "event": "created",
                "user_email": "kutluhan@example.com",
                "task_title": "Create API",
                "timestamp": datetime.utcnow().isoformat()
            },
            name="Create Task"
        )

    @task(1)
    def complete_task(self):
        """Simulates completing a task"""
        self.client.post(
            url="https://us-central1-taskmanager-project-460020.cloudfunctions.net/notify_task_event",
            json={
                "task_id": str(uuid.uuid4()),
                "event": "completed",
                "user_email": "kutluhan@example.com",
                "task_title": "Write tests",
                "timestamp": datetime.utcnow().isoformat()
            },
            name="Complete Task"
        )

    @task(1)
    def delete_task(self):
        """Simulates deleting a task"""
        self.client.post(
            url="https://us-central1-taskmanager-project-460020.cloudfunctions.net/notify_task_event",
            json={
                "task_id": str(uuid.uuid4()),
                "event": "deleted",
                "user_email": "kutluhan@example.com",
                "task_title": "Old task",
                "timestamp": datetime.utcnow().isoformat()
            },
            name="Delete Task"
        )
