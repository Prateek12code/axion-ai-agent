from live_store import LiveStore
from agent import agent_reason

class AxionPipeline:
    def __init__(self, watch_folder: str):
        self.store = LiveStore(watch_folder)

    def refresh(self):
        return self.store.scan_once()

    def answer(self, query: str) -> str:
        evidence = self.store.search(query=query, top_k=3)
        return agent_reason(query=query, evidence=evidence)
