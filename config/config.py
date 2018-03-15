import json

settings = json.loads(open('config/bot_cfg.json').read())#, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
log_cfg = settings['Logging']
