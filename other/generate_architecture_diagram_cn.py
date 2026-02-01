from PIL import Image, ImageDraw, ImageFont
import os

def create_diagram():
    # 画布设置
    width, height = 1200, 900
    background_color = (255, 255, 255)
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    # 尝试加载中文字体
    font_paths = [
        "msyh.ttc",     # 微软雅黑
        "simhei.ttf",   # 黑体
        "simsun.ttc",   # 宋体
        "arial.ttf"     # 备用字体（对中文支持不佳，但能防止崩溃）
    ]
    
    title_font = None
    header_font = None
    text_font = None
    
    for font_name in font_paths:
        try:
            # 尝试从默认 Windows 字体目录加载（如果当前目录未找到）
            # PIL ImageFont.truetype 通常会在 Windows 系统路径中搜索
            title_font = ImageFont.truetype(font_name, 36)
            header_font = ImageFont.truetype(font_name, 24)
            text_font = ImageFont.truetype(font_name, 18)
            print(f"Loaded font: {font_name}")
            break
        except IOError:
            continue
            
    if title_font is None:
        print("Warning: No suitable font found. Chinese characters may not render correctly.")
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # 颜色定义
    box_fill = (240, 248, 255) # 爱丽丝蓝
    box_outline = (70, 130, 180) # 钢蓝
    layer_bg = (250, 250, 250)
    layer_outline = (200, 200, 200)
    text_color = (0, 0, 0)
    arrow_color = (100, 100, 100)

    # 绘制圆角矩形的辅助函数
    def draw_box(x, y, w, h, text, title=None):
        draw.rectangle([x, y, x+w, y+h], fill=box_fill, outline=box_outline, width=2)
        
        if title:
            # 在顶部绘制居中标题
            bbox = draw.textbbox((0, 0), title, font=header_font)
            tx = x + (w - (bbox[2] - bbox[0])) // 2
            ty = y + 10
            draw.text((tx, ty), title, fill=text_color, font=header_font)
            
            # 在下方绘制内容文本
            lines = text.split('\n')
            curr_y = y + 45
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=text_font)
                tx = x + (w - (bbox[2] - bbox[0])) // 2
                draw.text((tx, curr_y), line, fill=text_color, font=text_font)
                curr_y += 25
        else:
            # 文本垂直水平居中
            lines = text.split('\n')
            total_h = len(lines) * 25
            curr_y = y + (h - total_h) // 2
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=text_font)
                tx = x + (w - (bbox[2] - bbox[0])) // 2
                draw.text((tx, curr_y), line, fill=text_color, font=text_font)
                curr_y += 25
                
    def draw_layer_box(x, y, w, h, title):
        draw.rectangle([x, y, x+w, y+h], fill=layer_bg, outline=layer_outline, width=1)
        draw.text((x + 10, y + 10), title, fill=(50, 50, 50), font=header_font)

    def draw_arrow(x1, y1, x2, y2):
        draw.line([(x1, y1), (x2, y2)], fill=arrow_color, width=2)
        # 简单箭头
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 15
        x_arrow1 = x2 - arrow_len * math.cos(angle - math.pi / 6)
        y_arrow1 = y2 - arrow_len * math.sin(angle - math.pi / 6)
        x_arrow2 = x2 - arrow_len * math.cos(angle + math.pi / 6)
        y_arrow2 = y2 - arrow_len * math.sin(angle + math.pi / 6)
        draw.polygon([(x2, y2), (x_arrow1, y_arrow1), (x_arrow2, y_arrow2)], fill=arrow_color)

    # 标题
    draw.text((400, 30), "python-autotest-trae 测试框架架构图", fill=text_color, font=title_font)

    # 1. 测试层 (顶部)
    draw_layer_box(350, 100, 500, 150, "测试层 (Test Layer)")
    draw_box(380, 150, 130, 80, "测试用例\n(Pytest)", "测试逻辑")
    draw_box(530, 150, 130, 80, "测试夹具\n(Conftest)", "依赖注入")
    draw_box(680, 150, 130, 80, "Allure\n测试报告", "报告生成")

    # 2. 业务逻辑层 (中部)
    draw_layer_box(350, 300, 500, 150, "业务逻辑层 (Business Layer)")
    draw_box(450, 350, 300, 80, "用户业务\n(operation/User.py)", "业务逻辑")

    # 3. 接口层 (中下部)
    draw_layer_box(350, 500, 500, 150, "接口层 (API Layer)")
    draw_box(450, 550, 300, 80, "用户接口\n(api/User.py)", "接口定义")

    # 4. 核心层 (底部)
    draw_layer_box(350, 700, 500, 150, "核心层 (Core Layer)")
    draw_box(400, 750, 180, 80, "Rest客户端\n(requests)", "HTTP客户端")
    draw_box(620, 750, 180, 80, "基础结果对象", "响应封装")

    # 5. 基础层 (左侧)
    draw_layer_box(50, 100, 250, 750, "基础层 (Infrastructure)")
    draw_box(80, 180, 190, 80, "配置加载\n(env_*.ini)", "配置管理")
    draw_box(80, 330, 190, 80, "数据加载\n(YAML/Excel)", "数据驱动")
    draw_box(80, 480, 190, 80, "数据库操作\n(PyMySQL)", "数据库")
    draw_box(80, 630, 190, 80, "日志记录\n(logging)", "日志管理")

    # 连接线 (箭头)
    
    # 测试层 -> 业务逻辑层
    draw_arrow(600, 230, 600, 300) 
    
    # 业务逻辑层 -> 接口层
    draw_arrow(600, 450, 600, 500)
    
    # 接口层 -> 核心层
    draw_arrow(600, 650, 500, 750) 
    draw_arrow(500, 830, 620, 830) 
    
    # 基础层 -> 其他层
    draw_arrow(270, 220, 350, 220) 
    draw_arrow(270, 370, 350, 370) 
    draw_arrow(270, 520, 350, 520) 
    
    # 保存
    image.save("架构图.png")
    print("架构图.png generated successfully.")

if __name__ == "__main__":
    create_diagram()
