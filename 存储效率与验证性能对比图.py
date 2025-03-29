import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set scientific visualization style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'mathtext.fontset': 'stix',
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9
})
sns.set_style("whitegrid")

# Create figure with two panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Panel A: Storage Efficiency Comparison
# Data preparation
structures = ['Merkle Tree', 'Verkle Tree']
metadata_size = [1.28, 0.53]  # KB per block
total_storage = [131.0, 54.2]  # MB
compression_rate = [42.3, 58.6]  # %

# Set x positions
x = np.arange(len(structures))
width = 0.25

# Plot metadata size
bars1 = ax1.bar(x - width, metadata_size, width, label='Metadata Size (KB/block)', color='#3498db')
ax1.set_ylabel('Metadata Size (KB/block)')

# Create secondary y-axis for storage
ax1b = ax1.twinx()
# Plot total storage
bars2 = ax1b.bar(x, total_storage, width, label='Total Storage (MB)', color='#2ecc71')
ax1b.set_ylabel('Total Storage (MB)')

# Create tertiary y-axis for compression rate
ax1c = ax1.twinx()
# Adjust the position of the third y-axis
ax1c.spines['right'].set_position(('outward', 60))
# Plot compression rate
bars3 = ax1c.bar(x + width, compression_rate, width, label='Compression Rate (%)', color='#e74c3c')
ax1c.set_ylabel('Compression Rate (%)')

# Set x-axis properties
ax1.set_xticks(x)
ax1.set_xticklabels(structures)
ax1.set_title('A. Storage Efficiency Comparison')

# Create consolidated legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1b.get_legend_handles_labels()
lines3, labels3 = ax1c.get_legend_handles_labels()
ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, 
           loc='upper right', fontsize=8, frameon=True)

# Add percentage improvement annotations
ax1.annotate('58.6% reduction', xy=(1, 0.5), xytext=(0.3, 0.3),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

# Panel B: Verification Performance Comparison
# Data preparation
metrics = ['Path Gen Time\n(ms)', 'Verification Time\n(ms)', 'Proof Size\n(Bytes/256)']
merkle_values = [2.1, 1.8, 4.0]  # Normalized proof size: 1024/256=4
verkle_values = [1.7, 0.4, 1.0]  # Normalized proof size: 256/256=1
merkle_errors = [0.3, 0.2, 0]
verkle_errors = [0.2, 0.1, 0]

# Set bar positions
x = np.arange(len(metrics))
width = 0.35

# Plot Merkle tree metrics
bars4 = ax2.bar(x - width/2, merkle_values, width, yerr=merkle_errors,
               label='Merkle Tree', color='#3498db', capsize=4)
# Plot Verkle tree metrics
bars5 = ax2.bar(x + width/2, verkle_values, width, yerr=verkle_errors,
               label='Verkle Tree', color='#e74c3c', capsize=4)

# Configure axes
ax2.set_ylabel('Performance Metrics (normalized)')
ax2.set_xticks(x)
ax2.set_xticklabels(metrics)
ax2.set_title('B. Verification Performance Metrics')
ax2.legend(loc='upper right', fontsize=8)

# Add performance improvement annotations
ax2.annotate('77.8% faster', xy=(1, 0.4), xytext=(1.4, 1.0),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

ax2.annotate('75% smaller', xy=(2, 1.0), xytext=(1.5, 2.0),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

# Set common layout parameters
plt.tight_layout()
fig.suptitle('Comparative Analysis: Verkle Tree vs. Merkle Tree', fontsize=12, y=0.98)
plt.subplots_adjust(top=0.90)

# Save high-resolution figure
plt.savefig('verkle_merkle_comparison.png', dpi=300, bbox_inches='tight')
plt.close()