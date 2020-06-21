"""后台任务"""
import json
import copy
import asyncio

from loggers import record_weather_msg
from helpers import api

global TASK_DATA
def get_task_json():
    global TASK_DATA
    with open("./task_background_app/task_config.json") as api_file:
        TASK_DATA = json.load(api_file)

get_task_json()

def get_city_weather(task_config: dict, citys: iter):
    """实况天气"""
    datas = []
    for c in citys:
        if not c.leaderZh in task_config["aim"]:
            continue
        data = copy.copy(task_config["params"])
        infos = {"city_id": f"CN{c.id}"}
        for k, v in data.items():
            data[k] = v.format(**infos)
        datas.append(data)
    results = {}
    if "paths" not in task_config:
        task_config["paths"] = ['']

    path_data_list = []
    for path in task_config["paths"]:
        url = task_config["host"] + path
        resps = api.get_all_weather(url, datas)
        for resp in resps:
            key = eval(task_config["resp"]["key"])
            weather_data = eval(task_config["resp"]["data"])
            if key not in results:
                results[key] = {}
            results[key].update(weather_data)
    record_weather_msg(results)
    return True

def in_todo_list(task_id):
    global TASK_DATA
    if task_id in TASK_DATA:
        return True
    else:
        return False

def to_nothing(*args, **kwargs):
    pass

def do_work(task_id: str, citys: iter):
    task_config = globals()["TASK_DATA"][task_id]
    worker_name = task_config.get("woker") or ''
    worker = globals().get(worker_name) or to_nothing
    worker(task_config, citys)
    return True
