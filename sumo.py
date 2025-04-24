"""
sumo.py 将 SPS 与 SUMO (traci) 集成，实时获取车辆位置并调用 SPS.step()
"""
from Vehicle import Vehicle
from Channel import Channel
from SPS import SPS
import traci
import random

def main():
    # 1. 启动 SUMO GUI 并加载场景
    sumo_cmd = ["sumo-gui", "-c", "ramp.sumocfg"]
    traci.start(sumo_cmd)

    # 2. 第一个时隙，取初始车辆列表
    traci.simulationStep()
    sumo_ids = traci.vehicle.getIDList()
    num_vehicle = len(sumo_ids)

    # 3. 初始化 SPS 引擎
    sps = SPS(time_period=30000, target_distance=100)
    sps.num_vehicle = num_vehicle
    sps.RBG_list = sps.generate_RBGs(sps.time_period)
    sps.channel = Channel(sps.num_subch, sps.interval)
    sps.vehicle_list = []
    sps.current_step = 0
    sps.initialized = True

    # 4. 创建 Vehicle 实例并完成初始配置
    vehicle_dict = {}
    for vid in sumo_ids:
        pos = traci.vehicle.getPosition(vid)
        v = Vehicle(vid, pos, power=23,
                    p_resource_keeping=0.2,
                    RCrange=[5,25],
                    target_distance=100)
        vehicle_dict[vid] = v
        sps.vehicle_list.append(v)
    for v in sps.vehicle_list:
        v.message_list_ini(sps.time_period)
        v.generate_beacon(sps.interval, 200, sps.time_period)
        v.initial_RBGs_selection(sps.RBG_list, sps.interval)
        v.generate_neighbour_set(sps.vehicle_list)

    # 5. 主仿真循环：simulationStep → 获取新/移除车辆 → 更新位置 → SPS.step
    step = 1
    while step < sps.time_period:
        traci.simulationStep()
        curr_ids = traci.vehicle.getIDList()
        # 5.1 新增车辆检测 & 初始化
        for vid in curr_ids:
            if vid not in vehicle_dict:
                # 同上初始化逻辑...
                pass
        # 5.2 删除离场车辆
        # 5.3 更新所有车辆位置
        for vid in curr_ids:
            pos = traci.vehicle.getPosition(vid)
            vehicle_dict[vid].update_location(pos)
        # 5.4 执行 SPS 决策
        sps.current_step = step
        sps.step()
        step += 1

    traci.close()

if __name__ == "__main__":
    main()

