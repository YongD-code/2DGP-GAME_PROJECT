from pico2d import *
import world
import random

class QuestManage:
    def __init__(self):
        self.quests = {
            "quest_corn": {
                "type": "collect",
                "target": "corn",
                "required": 3,
                "progress": 0,
                "state": "not_started",
                "reward_given": False,
                "reward": {"gold": 100,"seeds": ["seed_corn"]}
            },

            "quest_slime": {
                "type": "kill",
                "target": "slime",
                "required": 3,
                "progress": 0,
                "state": "not_started",
                "reward_given": False,
                "reward": {"gold": 300,"seeds": ["seed_corn", "seed_pumpkin", "seed_potato", "seed_strawberry"]}
            },

            "quest_potato": {
                "type": "collect",
                "target": "potato",
                "required": 3,
                "progress": 0,
                "state": "not_started",
                "reward_given": False,
                "reward": {"gold": 150, "seeds": ["seed_corn", "seed_pumpkin", "seed_potato", "seed_strawberry"]}
            },
        }
        self.quest_cycle = ["quest_corn", "quest_slime", "quest_potato"]
        self.quest_index = 0
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

    def give_reward(self, quest_id):
        q = self.quests[quest_id]

        if q["reward_given"]:
            return

        reward = q.get("reward", {})
        if q["type"] == "collect":
            target = q["target"]
            required = q["required"]
            remaining = required

            for item in world.inventory.items:
                if item and item["id"] == target:
                    if item["count"] >= remaining:
                        item["count"] -= remaining
                        remaining = 0
                        break
                    else:
                        remaining -= item["count"]
                        item["count"] = 0

            for slot in world.inventory.slots:
                idx = slot["item"]
                if idx is not None:
                    item = world.inventory.items[idx]
                    if item["count"] <= 0:
                        slot["item"] = None

        if "gold" in reward:
            world.gold += reward["gold"]

            from text_ani import TextAni
            world.add_object(
                TextAni(world.player.x, world.player.y + 80,f"골드 + {reward['gold']}", (255,255,255)),3)

        if "seeds" in reward:

            seed_list = reward["seeds"]
            seed_id = random.choice(seed_list)
            fixed_count = 10


            for _ in range(fixed_count):
                world.inventory.add_item(seed_id)

            name_kr = {
                "seed_corn": "옥수수 씨앗",
                "seed_pumpkin": "호박 씨앗",
                "seed_potato": "감자 씨앗",
                "seed_strawberry": "딸기 씨앗",
            }

            world.add_object(
                TextAni(world.player.x, world.player.y + 120,
                        f"{name_kr.get(seed_id, seed_id)} +10",
                        (255, 255, 180)), 3
            )
        q["reward_given"] = True

        self.quest_index = (self.quest_index + 1) % len(self.quest_cycle)

        next_qid = self.quest_cycle[self.quest_index]

        self.quests[next_qid]["state"] = "not_started"
        self.quests[next_qid]["progress"] = 0
        self.quests[next_qid]["reward_given"] = False

    def complete(self, quest_id):
        self.quests[quest_id]["state"] = "completed"

