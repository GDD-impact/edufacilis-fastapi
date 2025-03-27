from .celery_app import celery_app

@celery_app.task(name="send_email_task")
def send_email_task(email: str, subject: str, body: str):
    """Send an email (Example Task)"""
    print(f"Sending email to {email} with subject: {subject}")
    return f"Email sent to {email}"

@celery_app.task(name="generate_report_task")
def generate_report_task(report_type: str):
    """Generate a report (Example Task)"""
    print(f"Generating {report_type} report...")
    return f"{report_type} report generated."


@celery_app.task(name="user_initialized_task")
def user_initialized_task(task_name: str):
    """Run a user-initialized task."""
    print(f"Running user-initialized task: {task_name}")
    return f"Task {task_name} completed successfully."

