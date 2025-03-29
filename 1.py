from graphviz import Digraph

# 创建有向图
dot = Digraph(name='KGG_Authentication', format='png', 
              graph_attr={'rankdir': 'TB', 'fontname': 'Arial'},
              node_attr={'fontname': 'Arial', 'fontsize': '12'},
              edge_attr={'fontname': 'Arial', 'fontsize': '10'})

# 设备层子图
with dot.subgraph(name='cluster_device') as c:
    c.attr(label='设备层', style='filled', color='lightgrey')
    
    # 设备层节点
    c.node('ni', '传感器设备\nn_i', shape='box3d', fillcolor='white', style='filled')
    c.node('trusted_module', '可信模组\n(密钥生成/PUF/签名)', shape='component', fillcolor='#E0FFFF')
    c.node('ir', '注册请求\nIR_i = ⟨ID_i, PK_i, H(PUF_i), σ_SK_i⟩', 
           shape='note', fillcolor='#F0FFF0')
    
    # 设备层连接
    c.edge('ni', 'trusted_module', label='生成请求')
    c.edge('trusted_module', 'ir', label='构建请求')

# 区块链网络层子图
with dot.subgraph(name='cluster_blockchain') as c:
    c.attr(label='区块链网络层', style='filled', color='#F0E68C')
    
    c.node('kgg', 'KGG组\n（高信誉节点集群）', shape='oval', fillcolor='white')
    c.node('consensus', '改进的拜占庭共识协议\n|G| ≥ 3f+1', shape='ellipse', fillcolor='#FFE4E1')
    
    # 验证模块子图
    with c.subgraph(name='cluster_validation') as sub:
        sub.attr(label='验证模块', color='black')
        sub.node('physical', '物理特征验证\nH(PUF_i)比对', shape='diamond')
        sub.node('behavior', '行为分析引擎\n信号强度/采样频率', shape='diamond')
        sub.node('trust', '信任网络评估\nT(n_i)=Σ(Q(v_j)/dist)', shape='diamond')

# 证书管理层子图
with dot.subgraph(name='cluster_cert') as c:
    c.attr(label='证书管理层', style='filled', color='#D8BFD8')
    
    c.node('threshold', '(t,n)门限签名协议', shape='tab')
    c.node('cert', '设备证书\nCert_i = ⟨ID_i, PK_i, T_expire, ∏σ_KGG⟩', 
           shape='note')
    c.node('verkle', 'Verkle树存储结构\n（证书哈希锚定）', shape='folder')
    c.node('crl', '动态证书管理\nCRL列表/跨链互认', shape='cylinder')

# 威胁防御标注节点
dot.node('threat', '安全机制\n• 物理特征绑定防御替换攻击\n• 定理1: |G| ≥ 3f+1',
         shape='note', fillcolor='#FFFACD')

# 数据流向连接
dot.edge('ir', 'kgg', color='blue', label='广播请求')
dot.edge('kgg', 'consensus', color='purple', label='共识启动')

dot.edge('consensus', 'physical', color='green', label='验证阶段')
dot.edge('consensus', 'behavior', color='green', label='验证阶段')
dot.edge('consensus', 'trust', color='green', label='验证阶段')

dot.edge('physical', 'threshold', color='orange', label='通过验证')
dot.edge('behavior', 'threshold', color='orange', label='通过验证')
dot.edge('trust', 'threshold', color='orange', label='通过验证')

dot.edge('threshold', 'cert', color='red', label='签发证书')
dot.edge('cert', 'verkle', color='darkgreen', label='链上存储')
dot.edge('cert', 'crl', color='red', label='状态更新')

# 生成图片
dot.render(filename='kgg_authentication', cleanup=True, format='png')
print("流程图已生成：kgg_authentication.png")