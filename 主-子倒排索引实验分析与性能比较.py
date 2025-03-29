import matplotlib.pyplot as plt
import numpy as np
import os

# 创建图表
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 三种方案的性能数据
solutions = ['No Index', 'Primary Index', 'Primary-Sub Index']
query_latency = [2450, 380, 18]  # 查询延迟(ms)
scanned_blocks = [10000, 256, 1]  # 扫描数据块数
cpu_usage = [98.7, 45.2, 9.8]  # CPU占用率(%)

# 绘制查询延迟对比
axes[0].bar(solutions, query_latency, color=['#FF9999', '#66B2FF', '#99CC99'])
axes[0].set_title('Query Latency (ms)')
axes[0].set_yscale('log')  # 使用对数刻度更好地显示差异
for i, v in enumerate(query_latency):
    axes[0].text(i, v + 5, str(v), ha='center')

# 绘制扫描数据块数对比
axes[1].bar(solutions, scanned_blocks, color=['#FF9999', '#66B2FF', '#99CC99'])
axes[1].set_title('Scanned Data Blocks')
axes[1].set_yscale('log')  # 使用对数刻度
for i, v in enumerate(scanned_blocks):
    axes[1].text(i, v + 5, str(v), ha='center')

# 绘制CPU占用率对比
axes[2].bar(solutions, cpu_usage, color=['#FF9999', '#66B2FF', '#99CC99'])
axes[2].set_title('CPU Usage (%)')
for i, v in enumerate(cpu_usage):
    axes[2].text(i, v + 1, str(v), ha='center')

# 设置图表标题和布局
fig.suptitle('Primary-Sub Inverted Index Performance Analysis', fontsize=16)
plt.tight_layout()
plt.subplots_adjust(top=0.85)

# 获取当前工作目录并保存图表
current_dir = os.getcwd()  # 获取当前代码运行的目录
save_path = os.path.join(current_dir, 'index_performance_comparison.png')
plt.savefig(save_path, bbox_inches='tight', dpi=300)

# 显示保存路径信息
print(f"图表已保存至: {save_path}")