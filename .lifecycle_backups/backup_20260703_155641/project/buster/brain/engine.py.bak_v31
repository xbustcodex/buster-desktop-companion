from buster.brain.planner.planner import AIPlanner

class BrainEngine:
    def __init__(self, services, bus, logger):
        self.services = services
        self.bus = bus
        self.logger = logger
        self.planner = AIPlanner()

    def process(self, text: str):
        text = text.strip()
        if not text:
            return "I am online."
        self.services.get("memory").add("user", text)
        self.services.get("conversation").add_user(text)
        self.logger.info("User: " + text)

        plan = self.planner.make_plan(text)
        self.bus.emit("plan_updated", text=self.planner.describe())
        plan.status = "running"
        self.bus.emit("plan_updated", text=self.planner.describe())

        reply = self.execute(plan)
        plan.status = "done"
        self.bus.emit("plan_updated", text=self.planner.describe())

        self.services.get("memory").add("buster", reply)
        self.services.get("conversation").add_assistant(reply)
        return reply

    def execute(self, plan):
        s = self.services
        a = plan.action
        target = plan.target

        if a == "performance.status": return s.get("performance").report()
        if a == "services.status": return s.get("service_manager").status()
        if a == "threads.status": return s.get("thread_pool").status()
        if a == "ai.status": return s.get("ai").status()
        if a == "ai.provider": return s.get("ai").set_provider(target)
        if a == "ai.answer": return s.get("ai").complete(target, context=self.build_context())
        if a == "apps.open": return s.get("apps").open(target)
        if a == "memory.search": return s.get("memory").search_text(target)
        if a == "system.status": return s.get("system").summary()
        if a == "agents.status": return s.get("agents").summary()
        if a == "automation.move_mouse": return s.get("automation").move_mouse_from_text(target)
        if a == "automation.type_text": return s.get("automation").type_text(target)
        if a == "automation.click": return s.get("automation").click()
        if a == "voice.status": return s.get("voice").status()
        if a == "voice.start": return s.get("voice").start_conversation()
        if a == "voice.stop": return s.get("voice").stop_conversation()
        if a == "voice.listen_once": return s.get("voice").listen_once_async()
        if a == "vision.status": return s.get("vision").status()
        if a == "vision.start":
            result = s.get("vision").start()
            self.bus.emit("show_vision_window")
            return result
        if a == "vision.stop": return s.get("vision").stop()
        if a == "vision.photo": return s.get("vision").take_photo()
        if a == "vision.faces": return s.get("vision").detect_faces()
        if a == "vision.objects": return s.get("vision").detect_objects()
        if a == "vision.qr": return s.get("vision").scan_qr()
        if a == "vision.ocr": return s.get("vision").read_text()
        if a == "vision.learn_face": return s.get("vision").learn_face(target or "Adam")
        if a == "vision.identify_face": return s.get("vision").identify_face()
        if a == "vision.face_status": return s.get("vision").face_status()
        if a == "plugins.status": return s.get("plugins").status()
        if a == "hardware.status": return s.get("hardware").status()
        if a == "diagnostics.report": return s.get("diagnostics").full_report()
        if a == "agents.delegate": return s.get("agents").delegate(plan.agent, target)
        return s.get("ai").complete(target, context=self.build_context())

    def build_context(self):
        parts = []
        try: parts.append(self.services.get("system").summary())
        except Exception: pass
        try: parts.append(self.services.get("apps").status())
        except Exception: pass
        try: parts.append("Recent conversation:\n" + self.services.get("conversation").summary())
        except Exception: pass
        return "\n".join(parts)
