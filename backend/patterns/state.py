class WorkflowState:
    def close_incident(self, rca_data: dict):
        if not rca_data or not rca_data.get("root_cause_category") or not rca_data.get("fix_applied"):
            raise ValueError("Transition Failed: Mandatory RCA data is incomplete.")
        return "CLOSED"