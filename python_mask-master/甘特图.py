import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 项目甘特图数据 - 基于Django二手商品交易平台任务安排
tasks = [
    '商品信息发布功能完善',
    '商品展示与详情页优化', 
    '分类筛选与状态管理',
    '管理员审核功能完善',
    '分页与频率限制优化',
    '测试用例编写与功能测试',
    '缺陷修复与系统优化',
    '文档整理与博客撰写'
]

# 任务开始日期（以项目开始为基准）
start_days = [0, 2, 4, 6, 7, 9, 11, 13]
durations = [2, 2, 2, 1, 2, 2, 2, 1]

# 创建图表
fig, ax = plt.subplots(figsize=(14, 8))

# 绘制甘特图 - 使用简单的条形图，不使用日期
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
for i, (task, start, dur) in enumerate(zip(tasks, start_days, durations)):
    ax.barh(i, dur, left=start, height=0.6, color=colors[i], edgecolor='black', linewidth=0.5)
    # 在条形图上添加任务标签
    ax.text(start + dur/2, i, f'T-{i+1}', 
            ha='center', va='center', fontweight='bold', color='white', fontsize=9)

# 设置y轴标签
ax.set_yticks(range(len(tasks)))
ax.set_yticklabels(tasks)

# 设置坐标轴标签
ax.set_xlabel('迭代天数（D1 - D14）', fontsize=12)
ax.set_ylabel('开发任务', fontsize=12)

# 设置x轴刻度为1, 2, 3...（数字）
max_day = max(start_days) + max(durations)
ax.set_xticks(np.arange(0, max_day + 1, 1))  # 每天一个刻度
ax.set_xticklabels([f'D{i+1}' for i in range(max_day + 1)])  # 标签为D1, D2, D3...

# 设置x轴范围
ax.set_xlim(0, max_day)

# 添加网格线
ax.grid(True, alpha=0.3, axis='x')

# 添加标题
plt.title('Django二手商品交易平台开发甘特图', fontsize=14, pad=20, fontweight='bold')

# 手动调整图表边距
plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1)

# 显示图表
plt.tight_layout()
plt.show()

# 保存图表到文件
plt.savefig('django_project_gantt_v2.png', dpi=300, bbox_inches='tight', facecolor='white')