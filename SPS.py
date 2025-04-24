"""
SPS.py 实现感知型半持久调度(SPS)的核心仿真引擎
"""
import numpy as np
from Vehicle import Vehicle
from RBG import RBG
from Channel import Channel

class SPS:
    def __init__(self,
                 time_period=300000,
                 target_distance=200,
                 start_sampling_time=0,
                 interval=100,
                 RC_low=5,
                 RC_high=15,
                 RSRP_ratio_beacon=0.2):
        # 仿真总时隙数
        self.time_period = time_period
        # 目标通信距离
        self.target_distance = target_distance
        # 开始统计 PDR 的时隙
        self.start_sampling_time = start_sampling_time
        # SPS 资源保持/重选周期
        self.interval = interval
        # 重选计数器上下界
        self.RC_low = RC_low
        self.RC_high = RC_high
        # 候选资源比例阈值
        self.RSRP_ratio_beacon = RSRP_ratio_beacon

        # 物理层参数
        self.transmit_power = 200
        self.num_subch = 4
        self.RCrange = [RC_low, RC_high]
        self.p_resource_keeping = 0.4
        self.sensing_window = 1000
        self.sinr_th = 2**2.1602 - 1
        self.noise = 10**(-174/10) * (15e3*12*10)

        # 统计结果存储
        self.pdr_ratio_list = []
        self.transmission_condition = []
        self.add_loss_ratio_to_beacon_list = []

        # 以下属性由外部（如 sumo.py）初始化赋值
        self.vehicle_list = None
        self.RBG_list = None
        self.channel = None
        self.current_step = 0
        self.initialized = False

    def genearate_vehicles(self, num_vehicle, num_slot, vehicle_location):
        vehicle_instance_list = []
        for i in range(num_vehicle):
            vehicle_instance_list.append(Vehicle(i, vehicle_location[i], self.transmit_power,
                                                 self.p_resource_keeping, self.RCrange, self.target_distance))
        return vehicle_instance_list

    def generate_RBGs(self, num_slot):
        """
        按 时隙×子信道 生成二维 RBG 列表
        返回: [[RBG(ts=0,sc=0),...], [RBG(ts=1,sc=0),...], ...]
        """
        all_RBGs = []
        for ts in range(num_slot):
            slot_list = [RBG(ts, sc) for sc in range(self.num_subch)]
            all_RBGs.append(slot_list)
        return all_RBGs

    def step(self):
        """
        执行当前时隙的 SPS 流程：
        1. 如果 t==0，初始化资源选择和邻居发现
        2. 否则更新 RC 计数器
        3. 感知窗口更新、信道感知
        4. 信标消息发送/资源选择
        5. 接收统计 (PDR)
        6. 周期性统计 PDR
        """
        if not self.initialized:
            raise Exception("请先在 sumo.py 中完成初始化: vehicle_list, RBG_list, channel, initialized=True")
        t = self.current_step
        if t >= self.time_period:
            return

        # 每 100 时隙打印一次进度
        if t % 100 == 0:
            print("SPS step:", t)

        # 1. 初始或 RC 更新
        for v in self.vehicle_list:
            if t == 0:
                v.initial_RBGs_selection(self.RBG_list, self.interval)
                v.generate_neighbour_set(self.vehicle_list)
            else:
                v.update_reselection_counter(t, self.interval, self.RCrange)

        # 2. 感知 / 3. 发送 / 4. 接收
        for v in self.vehicle_list:
            v.generate_RBGlist_1100ms(t, self.RBG_list, self.sensing_window)
            v.update_sensing_result(t, self.vehicle_list, self.RBG_list, self.sensing_window)
            if t > 0 and v.message_list[t] is not None:
                v.generate_neighbour_set(self.vehicle_list)
                v.generate_RBGs_in_selection_window(t, self.RBG_list, self.interval)
                v.RBG_selection_beacon(self.RSRP_ratio_beacon, self.RBG_list, t, self.channel)
            if t > 0 and t == v.v_RBG.timeslot:
                v.statistic_for_reception(self.vehicle_list, self.sinr_th, self.noise, t, self.start_sampling_time)

        # 5. 周期性PDR统计
        if t > self.start_sampling_time and t % 1000 == 0:
            tx = sum(v.num_tran for v in self.vehicle_list)
            rx = sum(v.num_rec for v in self.vehicle_list)
            self.pdr_ratio_list.append(rx / tx if tx else 0)
            self.transmission_condition.append([rx, tx])
            for v in self.vehicle_list:
                v.num_tran = 0
                v.num_rec = 0

        self.current_step += 1

# __main__ 部分只保留提示
if __name__ == '__main__':
    print("请通过 sumo.py 初始化 SPS 后调用 step() 进行实时仿真")



