import json
import logging
import datetime


class StackdriverJsonFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        # ref: https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
        # and https://cloud.google.com/logging/docs/agent/configuration#special-fields
        message_dict = {
            'timestamp': datetime.datetime.utcfromtimestamp(record.created).isoformat("T") + "Z",
            'severity': record.levelname, 'message': record.msg, 'logger': record.name,
            'sourceLocation': {
                'file': record.filename,
                'line': record.lineno,
                'function': record.funcName}
        }
        
        # Update message if message can parse by record.getMessage()
        try:
            msg = record.getMessage()
            message_dict['message'] = msg
        except TypeError:
            pass
        
        if len(record.args) > 0:
            if type(record.args) is dict:
                for key in record.args.keys():
                    message_dict[key] = record.args[key]
            elif len(record.args) == 1:
                message_dict['extra_info'] = record.args[0]
            else:
                message_dict['extra_info'] = record.args
        
        return json.dumps(message_dict)
