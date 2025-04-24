"""
message.py 定义消息基类及信标/紧急消息类型
"""
from RBG import RBG

class Message:
    def __init__(self, mtype, mdelay, mgeneration_time, mserved_RBG):
        # 消息类型，如 0 表示 Beacon
        self.mtype = mtype
        # 报文时延（ms）
        self.mdelay = mdelay
        # 生成时间（时隙编号）
        self.mgeneration_time = mgeneration_time
        # 分配到的 RBG 对象
        self.mserved_RBG = mserved_RBG

    def serve_RBG(self, timeslot, subchannel):
        """
        在 timeslot/subchannel 上标记本条消息被分配的资源
        """
        self.mserved_RBG = RBG(timeslot, subchannel)

    def set_sensing_window(self, sensing_duration):
        """
        设置感知窗口，以便车辆判断最近多少时隙数据可用
        """
        self.sensing_duration = sensing_duration
        self.sensing_window = [
            self.mgeneration_time - self.sensing_duration,
            self.mgeneration_time
        ]


class Beacon(Message):
    def __init__(self, mtype, mdelay, mgeneration_time, mserved_RBG, rate):
        super().__init__(mtype, mdelay, mgeneration_time, mserved_RBG)
        # 发送速率 (packets per second)
        self.rate = rate
        # 计算信标发送间隔（ms）
        self.interval = 1000 * (1 / self.rate)

    def set_selection_window(self, selection_window):
        """
        设置资源选择窗口 [start, end]
        """
        self.selection_window = [
            self.mgeneration_time,
            self.mgeneration_time + self.interval
        ]


class Emergency(Message):
    """
    紧急消息类型，可按需扩展
    """
    pass


