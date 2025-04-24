"""
RBG.py 定义资源块组类，用作时隙与子信道组合的标识
"""
class RBG:
    def __init__(self, timeslot, subchannel):
        # 时隙编号
        self.timeslot = timeslot
        # 子信道编号
        self.subchannel = subchannel

    def __eq__(self, other):
        # 两个 RBG 相等需时隙和子信道同时匹配
        return (self.timeslot == other.timeslot and
                self.subchannel == other.subchannel)

    def __hash__(self):
        # 支持用作字典或集合键
        return hash((self.timeslot, self.subchannel))

    def __repr__(self):
        return f"RBG(ts={self.timeslot}, sc={self.subchannel})"

    def RBG_vehicle_mapping(self, vehicle_list, vehicle):
        self.vehicle_list.append(vehicle)

    def generate_RBGs(num_slot, num_subch):
        RBG_intance_list = []
        for i in range(num_slot):
            RBG_intance_each_slot = []
            for j in range(num_subch):
                RBG_intance_each_slot.append(RBG(i, j))
            RBG_intance_list.append(RBG_intance_each_slot)

class RGBs_set():
    def __init__(self, timeslot, subchannel):
        self.timeslot = timeslot
        self.subchannel = subchannel