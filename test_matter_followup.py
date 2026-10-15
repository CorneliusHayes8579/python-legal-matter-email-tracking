from matter_followup import MatterIntake, choose_stage


def test_signed_document_takes_priority_over_intake():
    matter = MatterIntake("MAT-1", "client@example.com", "Sam", signed_document_id="DOC-1")
    assert choose_stage(matter) == ("signed-document", "Signed document for matter MAT-1")
