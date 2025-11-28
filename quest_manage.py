from pico2d import *
import world

class QuestManage:
    def __init__(self):
        self.quests = {
            "npc_corn": {
                "state": "not_started",
                "required": 5,
                "progress": 0,
                "reward_given": False
            }
        }

    def start_quest(self, quest_id):
        q = self.quests[quest_id]
        if q["state"] == "not_started":
            q["state"] = "in_progress"

    def add_progress(self, quest_id, amount=1):
        q = self.quests[quest_id]
        if q["state"] != "in_progress":
            return
        q["progress"] += amount
        if q["progress"] >= q["required"]:
            q["state"] = "completed"

    def is_completed(self, quest_id):
        return self.quests[quest_id]["state"] == "completed"
