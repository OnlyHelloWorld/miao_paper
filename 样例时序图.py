from blockdiag import parser, builder, drawer
from blockdiag.imagedraw import png

diag_script = """
seqdiag {
    用户 -> 网关服务 [label = "发送查询请求"];
    网关服务 -> 消息队列 [label = "发送查询消息"];
    消息队列 -> 服务路由 [label = "订阅查询请求"];
    服务路由 -> 读写服务 [label = "处理查询任务"];
    读写服务 -> 资源层 [label = "读取数据"];
    资源层 -> 读写服务 [label = "返回查询结果"];
    读写服务 -> 服务路由 [label = "返回查询结果"];
    服务路由 -> 网关服务 [label = "返回查询结果"];
    网关服务 -> 用户 [label = "返回查询结果"];
}
"""

# 解析时序图
tree = parser.parse_string(diag_script)
diagram = builder.ScreenNodeBuilder.build(tree)

# 生成图片
draw = drawer.DiagramDraw("PNG", diagram, filename="sequence_diagram.png", fontmap=None)
draw.draw()
draw.save()
print("时序图已生成：sequence_diagram.png")
