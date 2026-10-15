from dataclasses import dataclass
from typing import Any

from infrai_email import InfraiEmail


@dataclass(frozen=True)
class MatterIntake:
    matter_id: str
    client_email: str
    client_name: str
    signed_document_id: str | None = None
    deadline_due: bool = False


def choose_stage(matter: MatterIntake) -> tuple[str, str]:
    if matter.deadline_due:
        return "deadline", f"Deadline follow-up for matter {matter.matter_id}"
    if matter.signed_document_id:
        return "signed-document", f"Signed document for matter {matter.matter_id}"
    return "intake", f"Matter intake received: {matter.matter_id}"


def process_matter(matter: MatterIntake, client: InfraiEmail) -> dict[str, Any]:
    stage, subject = choose_stage(matter)
    result = client.send({"to": matter.client_email, "subject": subject,
                          "html": f"<p>Hello {matter.client_name},</p><p>{subject}.</p>"},
                         idempotency_key=f"matter:{matter.matter_id}:{stage}")
    message_id = result["data"]["message_id"]
    client.get(message_id)
    events = client.events(message_id)
    return {"matter_id": matter.matter_id, "stage": stage, "message_id": message_id,
            "events": events.get("data", [])}
