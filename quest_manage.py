from pico2d import *
import world

class QuestManage:
    def __init__(self):
        self.quests = {
            "quest_corn": {
                "type": "collect",
                "target": "corn",
                "required": 5,
                "progress": 0,
                "state": "not_started",
                "reward_given": False
            },

            "quest_slime": {
                "type": "kill",
                "target": "slime",
                "required": 10,
                "progress": 0,
                "state": "not_started",
                "reward_given": False
            },
        }

    def start_quest(self, quest_id):
        q = self.quests[quest_id]
        q["state"] = "in_progress"

    def add_progress(self, quest_id, amount=1):
        q = self.quests[quest_id]
        if q["state"] != "in_progress":
            return

        q["progress"] += amount
        if q["progress"] >= q["required"]:
            q["state"] = "completed"

    def check_inventory_quests(self):
        for quest_id, q in self.quests.items():
            if q["state"] != "in_progress":
                continue
            if q["type"] != "collect":
                continue

            total = 0
            for item in world.inventory.items:
                if item and item["id"] == q["target"]:
                    total += item["count"]

            if total >= q["required"]:
                q["state"] = "completed"

    def complete(self, quest_id):
        self.quests[quest_id]["state"] = "completed"

