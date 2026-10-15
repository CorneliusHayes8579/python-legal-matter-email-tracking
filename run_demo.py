import os

from infrai_email import InfraiEmail
from matter_followup import MatterIntake, process_matter


def main() -> None:
    recipient = os.environ["MATTER_EMAIL_TO"]
    matter = MatterIntake("MAT-104", recipient, "Alex Morgan", signed_document_id="DOC-7")
    summary = process_matter(matter, InfraiEmail())
    print(f"sent {summary['stage']} message {summary['message_id']}")
    print(f"events: {len(summary['events'])}")


if __name__ == "__main__":
    main()
