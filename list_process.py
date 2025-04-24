"""
list_process.py 存放列表处理的通用函数
"""
def transfer_2Dlist_to_1Dlist(two_d_list):
    """
    将二维列表拍平成一维列表
    输入: [[a,b],[c,d]]  输出: [a,b,c,d]
    """
    flat = []
    for sublist in two_d_list:
        for item in sublist:
            flat.append(item)
    return flat
