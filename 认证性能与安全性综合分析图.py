import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configure visualization parameters
plt.rcParams.update({'font.size': 9, 'font.family': 'serif'})
sns.set_style("whitegrid")

# Create figure with optimal dimensions
fig, axs = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [1, 1.2]})

# Define core performance metrics
success_rate = 98.7
attack_types = ['Identity Forgery', 'Location Spoofing', 'Replay Attack']
air_values = [94.2, 98.8, 100.0]  # Attack interception rates
fpr_values = [0.3, 0.1, 0.0]      # False positive rates

# Panel A: Authentication latency breakdown (pie chart)
ax1 = axs[0]
components = ['BLS Signature (68%)', 'Request Processing (16%)', 'Network (12%)', 'Other (4%)']
values = [22.1, 5.2, 3.8, 1.3]  # Total: 32.4ms
colors = sns.color_palette("Blues", len(components))

wedges, texts = ax1.pie(values, colors=colors, startangle=90, 
                         wedgeprops={'edgecolor': 'w', 'linewidth': 1})

# Add custom legend with quantitative values
ax1.legend(components, title="Authentication Latency Components", 
           loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
ax1.text(0, 0, f"Total: 32.4ms\nASR: {success_rate}%\n(σ=0.8%)", 
         ha='center', va='center', fontsize=9, fontweight='bold')
ax1.set_title('A. Authentication Performance Metrics')

# Panel B: Security evaluation (dual metrics bar chart)
ax2 = axs[1]
x = np.arange(len(attack_types))
width = 0.35

# Plot attack interception rates
bars1 = ax2.bar(x - width/2, air_values, width, label='Attack Interception Rate', color='#3498db')
# Plot false positive rates (with adjusted scale)
bars2 = ax2.bar(x + width/2, fpr_values, width, label='False Positive Rate', color='#e74c3c')

# Add value annotations
for i, v in enumerate(air_values):
    ax2.text(i - width/2, v + 1, f'{v}%', ha='center', fontsize=8)
for i, v in enumerate(fpr_values):
    ax2.text(i + width/2, v + 1, f'{v}%', ha='center', fontsize=8)

# Configure axis properties
ax2.set_ylabel('Rate (%)')
ax2.set_ylim(0, 105)
ax2.set_xticks(x)
ax2.set_xticklabels(attack_types)
ax2.legend(loc='upper right', fontsize=8)

# Add annotation for entropy threshold issue
ax2.annotate('Entropy threshold: 3.8-4.0 bits/byte', xy=(0, 75), xytext=(0, 60),
             ha='center', bbox=dict(boxstyle='round', fc='#f9e79f', alpha=0.3),
             arrowprops=dict(arrowstyle="->"))

ax2.set_title('B. Security Evaluation Against Attack Types')

# Add resource consumption data as text table
props = dict(boxstyle='round', facecolor='white', alpha=0.5)
textstr = 'Resource Consumption:\nCPU: 28.5ms | Memory: 12.3MB'
ax2.text(0.98, 0.02, textstr, transform=ax2.transAxes, fontsize=8,
         verticalalignment='bottom', horizontalalignment='right', bbox=props)

# Configure layout
plt.tight_layout()
fig.suptitle('KGG Protocol: Performance and Security Assessment', fontsize=12, y=0.98)
plt.subplots_adjust(top=0.92)

# Save figure
plt.savefig('kgg_assessment.png', dpi=300, bbox_inches='tight')
plt.close()