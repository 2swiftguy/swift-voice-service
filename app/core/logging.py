import logging, sys, json, time
def setup_logging():
    h = logging.StreamHandler(sys.stdout)
    class JsonFmt(logging.Formatter):
        def format(self, r):
            data = {"ts": time.time(), "lvl": r.levelname, "msg": r.getMessage(), "logger": r.name}
            rid = getattr(r, "request_id", None)
            if rid: data["request_id"] = rid
            return json.dumps(data)
    h.setFormatter(JsonFmt())
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [h]