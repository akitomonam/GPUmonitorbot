import argparse
import time
import settings

import slackweb

import subprocess

DEFAULT_ATTRIBUTES = (
    'index',
    'uuid',
    'name',
    'timestamp',
    'memory.total',
    'memory.free',
    'memory.used',
    'utilization.gpu',
    'utilization.memory'
)


class GPUMonitor2Slack():
    def __init__(self):
        self.webhook_url = settings.WEBHOOK_URL
        self.gpu_inf = list(dict())
        self.message = ""

    def slack_notify(self):
        self.slack = slackweb.Slack(url=self.webhook_url)
        self.slack.notify(text=self.message)

    def get_gpu_info(self, nvidia_smi_path='nvidia-smi', keys=DEFAULT_ATTRIBUTES, no_units=True):
        nu_opt = '' if not no_units else ',nounits'
        cmd = '%s --query-gpu=%s --format=csv,noheader%s' % (nvidia_smi_path, ','.join(keys), nu_opt)
        output = subprocess.check_output(cmd, shell=True)
        lines = output.decode().split('\n')
        lines = [line.strip() for line in lines if line.strip() != '']

        self.gpu_inf = [{k: v for k, v in zip(keys, line.split(', '))} for line in lines]
        # print("self.gpu_inf", self.gpu_inf)
        return

    def set_gpu_info_to_message(self):
        self.message = "\n".join(["\n".join([key + ": " + gpu_info[key] for key in gpu_info.keys()]) for gpu_info in self.gpu_inf])
        return

    def set_text_to_message(self, text):
        self.message = text
        return

    def check_master_gpu(self, thresh=100):
        return int(self.gpu_inf[0]["memory.used"]) < thresh


if __name__ == "__main__":
    # define argments
    p = argparse.ArgumentParser()
    p.add_argument("--interval", default="10")

    # parse argments
    args = p.parse_args()

    # Build a GPUMonitor2Slack instance
    gpumonitor2slack = GPUMonitor2Slack()

    # start GPU monitoring
    while True:
        # get current gpu information
        gpumonitor2slack.get_gpu_info()

        # set gpu information as string to notify
        gpumonitor2slack.set_gpu_info_to_message()

        # check notify or not
        if gpumonitor2slack.check_master_gpu():
            # Slack webhook notify
            gpumonitor2slack.slack_notify()

        # wait an interval time (minutes)
        time.sleep(int(args.interval) * 60)
