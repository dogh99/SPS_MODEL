"""
Channel.py 模拟物理层信道，维护时隙内可用的 RBG 列表
"""
import RBG

class Channel():
    def __init__(self, num_subch, interval):
        # 子信道数量
        self.num_subch = num_subch
        # 新时隙生成的 RBG 列表
        self.RBGs_in_new_slot = []
        # 资源重选周期（时隙数）
        self.interval = interval
        # 每次资源重选窗口中的 RBG 总数量
        self.num_RBGs_in_one_RRI = int(num_subch * interval)

    def create_new_RBGs(self, num_subch, timeslot):
        """
        在给定 timeslot 上生成 num_subch 条新的 RBG 实例
        """
        self.RBGs_in_new_slot = []
        for j in range(num_subch):
            RB = RBG.RBG(timeslot, j)
            self.RBGs_in_new_slot.append(RB)

