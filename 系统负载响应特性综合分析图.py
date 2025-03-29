import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import AutoMinorLocator

# 设置全局样式参数
plt.rcParams.update({'font.size': 10})
sns.set_style("whitegrid")

# 创建主图及内嵌图的画布
fig = plt.figure(figsize=(12, 8))

# 定义数据
# X轴: 并发请求数
concurrent_requests = np.array([10, 25, 50, 75, 100, 125, 150, 175, 200])

# 吞吐量数据: 随着并发请求增加系统实际处理的请求数
throughput = np.array([10, 25, 49.5, 74, 98.5, 123, 147, 170, 185])

# 延迟数据: 随负载增加的认证延迟(ms)
latency = np.array([33.1, 33.5, 34.2, 35.4, 37.2, 39.8, 42.5, 45.3, 48.7])

# 定义资源利用率数据
memory_usage = np.array([13.1, 15.3, 19.8, 24.5, 29.2, 34.0, 38.7, 43.5, 48.2])  # MB
cpu_usage = np.array([15, 22, 35, 48, 60, 72, 83, 91, 97])  # %

# 创建主图: 负载压力响应曲线
ax1 = fig.add_subplot(111)

# 绘制吞吐量曲线
color1 = '#3498db'  # 蓝色
line1, = ax1.plot(concurrent_requests, throughput, 'o-', color=color1, linewidth=2, label='Throughput (req/s)')
ax1.set_xlabel('Concurrent Requests per Second')
ax1.set_ylabel('Throughput (requests/s)', color=color1)
ax1.tick_params(axis='y', labelcolor=color1)

# 区域着色标识系统稳定运行区间
ax1.fill_between(concurrent_requests, throughput, alpha=0.2, color=color1)
ax1.axhline(y=185, color='blue', linestyle='--', alpha=0.7)
ax1.annotate('Stable processing threshold: 185 req/s',
            xy=(200, 185),
            xytext=(160, 165),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# 创建次轴: 显示延迟数据
ax2 = ax1.twinx()
color2 = '#e74c3c'  # 红色
line2, = ax2.plot(concurrent_requests, latency, 's-', color=color2, linewidth=2, label='Authentication Latency (ms)')
ax2.set_ylabel('Authentication Latency (ms)', color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

# 标注基准延迟和高负载延迟
ax2.axhline(y=32.4, color=color2, linestyle=':', alpha=0.7)
ax2.annotate('Baseline latency: 32.4ms',
            xy=(10, 32.4),
            xytext=(30, 30),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

ax2.annotate('High load latency: 48.7ms (+50.3%)',
            xy=(200, 48.7),
            xytext=(150, 50),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# 添加表示丢包率的标注
ax1.annotate('Packet loss < 0.5%',
            xy=(185, 185),
            xytext=(140, 140),
            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# 创建内嵌图: 资源利用率相关性分析
# 确定内嵌图在主图中的位置和大小
left, bottom, width, height = 0.25, 0.25, 0.3, 0.3
ax3 = fig.add_axes([left, bottom, width, height])

# 绘制内存使用量与并发请求数的线性关系
ax3.scatter(concurrent_requests, memory_usage, color='#2ecc71', label='Memory Usage')

# 计算线性回归
z = np.polyfit(concurrent_requests, memory_usage, 1)
p = np.poly1d(z)
ax3.plot(concurrent_requests, p(concurrent_requests), "r--", alpha=0.8)

# 计算相关系数
correlation = np.corrcoef(concurrent_requests, memory_usage)[0, 1]

# 添加线性回归方程和相关系数
equation = f"y = {z[0]:.2f}x + {z[1]:.2f}"
ax3.text(0.05, 0.95, equation + f"\nr = {correlation:.3f}", transform=ax3.transAxes,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

# CPU使用率添加到第二Y轴
ax4 = ax3.twinx()
ax4.plot(concurrent_requests, cpu_usage, 'p-', color='#9b59b6', label='CPU Usage (%)')
ax4.set_ylabel('CPU Usage (%)')

# 设置内嵌图标题和轴标签
ax3.set_title('Resource Utilization Correlation', fontsize=9)
ax3.set_xlabel('Concurrent Requests', fontsize=8)
ax3.set_ylabel('Memory Usage (MB)', fontsize=8)

# 合并图例
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

# 内嵌图上的图例
handles1, labels1 = ax3.get_legend_handles_labels()
handles2, labels2 = ax4.get_legend_handles_labels()
ax3.legend(handles1 + handles2, labels1 + labels2, loc='lower right', fontsize=6)

# 添加次要网格线增强可读性
ax1.xaxis.set_minor_locator(AutoMinorLocator())
ax1.yaxis.set_minor_locator(AutoMinorLocator())
ax1.grid(which='minor', linestyle=':')

# 设置主图标题
plt.suptitle('KGG Protocol: Performance and Resource Utilization Under Dynamic Load', fontsize=16, y=0.98)

# 调整布局
fig.tight_layout(rect=[0, 0, 1, 0.95])

# 保存高分辨率图像
plt.savefig('kgg_load_testing_performance.png', dpi=300, bbox_inches='tight')
plt.close()