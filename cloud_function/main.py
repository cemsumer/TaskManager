import functions_framework
from flask import request, jsonify
import datetime

@functions_framework.http
def notify_task_event(request):
    """
    Cloud Function to handle task-related events.
    Supported events: created, updated, completed, deleted

    Expected JSON input:
    {
        "task_id": "abc123",
        "event": "created",
        "user_email": "someone@example.com",
        "task_title": "Submit Report",
        "timestamp": "2025-05-20T18:00:00"
    }
    """

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Missing JSON payload"}), 400

        # Required fields
        task_id = data.get("task_id")
        event = data.get("event")
        task_title = data.get("task_title")
        user_email = data.get("user_email")
        timestamp = data.get("timestamp", datetime.datetime.utcnow().isoformat())

        # Validate inputs
        if not task_id or not event or not task_title:
            return jsonify({"error": "Missing required task fields"}), 400

        # Supported events
        valid_events = ["created", "updated", "completed", "deleted"]
        if event not in valid_events:
            return jsonify({"error": f"Unsupported event '{event}'"}), 400

        # Simulate event logging (could be expanded to send email, push, etc.)
        print(f"[{timestamp}] Event: {event.upper()} | Task ID: {task_id} | Title: {task_title} | User: {user_email}")

        # Optionally simulate different actions per event
        response_message = {
            "created": f"Task '{task_title}' was created successfully.",
            "updated": f"Task '{task_title}' was updated.",
            "completed": f"Task '{task_title}' was marked as complete.",
            "deleted": f"Task '{task_title}' was deleted.",
        }.get(event, "Event processed.")

        return jsonify({
            "status": "success",
            "event": event,
            "task_id": task_id,
            "message": response_message
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500