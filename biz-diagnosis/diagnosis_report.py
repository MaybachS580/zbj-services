"""
企业自动化诊断报告生成器
猪八戒服务：企业自动化诊断咨询

使用方法：
  python diagnosis_report.py --input survey.json --output report.pdf

依赖：
  pip install reportlab python-dotenv requests
"""

import os
import json
import argparse
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ========= 颜色定义 =========
COLOR_PRIMARY = HexColor("#1E40AF")    # 深蓝
COLOR_ACCENT = HexColor("#3B82F6")     # 亮蓝
COLOR_SUCCESS = HexColor("#10B981")    # 绿
COLOR_WARNING = HexColor("#F59E0B")    # 黄
COLOR_DANGER = HexColor("#EF4444")     # 红
COLOR_LIGHT_BG = HexColor("#F8FAFC")  # 浅灰背景
COLOR_TEXT = HexColor("#1F2937")       # 深文字
COLOR_GRAY = HexColor("#6B7280")       # 灰色


def setup_fonts():
    """注册中文字体（需要系统有SimHei或微软雅黑）"""
    font_paths = [
        ("C:/Windows/Fonts/simhei.ttf", "SimHei"),
        ("C:/Windows/Fonts/msyh.ttc", "MicrosoftYaHei"),
        ("C:/Windows/Fonts/simsun.ttc", "SimSun"),
    ]
    for path, name in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                return name
            except Exception:
                continue
    return "Helvetica"  # fallback


def calculate_score(survey: dict) -> dict:
    """根据问卷计算各维度得分"""
    scores = {}

    # 工具整合度（0-25分）
    tools = survey.get("tools_used", [])
    tool_score = min(len(tools) * 3, 15)
    integration = survey.get("tool_integration_level", 1)  # 1-5
    scores["tool_integration"] = tool_score + integration * 2

    # 重复工作占比（0-25分）
    repetitive_hours = survey.get("repetitive_work_hours_per_week", 20)
    scores["repetitive_work"] = max(0, 25 - repetitive_hours)

    # 自动化意识（0-25分）
    awareness = survey.get("automation_awareness", 3)  # 1-5
    scores["automation_awareness"] = awareness * 5

    # 数据互通（0-25分）
    data_silos = survey.get("data_silos_count", 3)
    scores["data_connectivity"] = max(0, 25 - data_silos * 5)

    total = sum(scores.values())
    scores["total"] = total
    scores["level"] = _get_level(total)

    return scores


def _get_level(score: int) -> dict:
    if score >= 80:
        return {"label": "优秀", "color": "success", "desc": "贵公司已具备较强的数字化能力，建议在现有基础上进行精细化优化"}
    elif score >= 60:
        return {"label": "良好", "color": "accent", "desc": "整体自动化水平良好，存在部分提升空间，建议优先攻克核心瓶颈"}
    elif score >= 40:
        return {"label": "待提升", "color": "warning", "desc": "存在明显的效率损耗点，系统化引入自动化工具可显著降本增效"}
    else:
        return {"label": "急需改善", "color": "danger", "desc": "当前运营模式手工程度较高，自动化改造空间大，ROI回报率极高"}


def identify_pain_points(survey: dict) -> list:
    """识别核心痛点"""
    pain_points = []

    if survey.get("repetitive_work_hours_per_week", 0) > 15:
        pain_points.append({
            "icon": "⚡",
            "title": "重复工作占比过高",
            "detail": f"每周约 {survey.get('repetitive_work_hours_per_week')} 小时花在重复操作上，"
                      f"按人力成本¥150/小时计算，每月浪费约 "
                      f"¥{survey.get('repetitive_work_hours_per_week', 0) * 4 * 150:,}",
            "priority": "P0"
        })

    if survey.get("data_silos_count", 0) >= 3:
        pain_points.append({
            "icon": "🔗",
            "title": "数据孤岛严重",
            "detail": f"使用了 {survey.get('data_silos_count')} 个相互隔离的系统，"
                      f"数据手动同步耗时且易出错，建议通过 n8n/Zapier 打通数据流",
            "priority": "P0"
        })

    if not survey.get("has_crm", False):
        pain_points.append({
            "icon": "👥",
            "title": "缺少客户管理系统",
            "detail": "没有统一的客户数据管理，线索流失风险高，建议引入轻量CRM（如飞书CRM/销售易）",
            "priority": "P1"
        })

    if survey.get("report_generation_hours_per_week", 0) > 5:
        pain_points.append({
            "icon": "📊",
            "title": "报表制作耗时",
            "detail": f"每周花约 {survey.get('report_generation_hours_per_week')} 小时制作报表，"
                      f"可用自动化数据看板完全替代，建议引入 Metabase 或 Power BI",
            "priority": "P1"
        })

    return pain_points


def generate_recommendations(survey: dict, scores: dict) -> list:
    """生成具体建议"""
    recs = []

    # 按得分和痛点生成优先级建议
    if scores["repetitive_work"] < 15:
        recs.append({
            "phase": "第一阶段（1-2周）",
            "title": "消灭重复操作",
            "tools": ["n8n", "Zapier", "Make"],
            "actions": [
                "梳理每天重复3次以上的操作，制成清单",
                "选择1个最耗时的流程，用n8n搭建自动化",
                "上线后持续监测节省的工时"
            ],
            "expected_roi": "预计节省 40-60% 重复工作时间"
        })

    if scores["data_connectivity"] < 15:
        recs.append({
            "phase": "第二阶段（2-4周）",
            "title": "打通数据孤岛",
            "tools": ["n8n", "飞书多维表格", "Airtable"],
            "actions": [
                "盘点所有在用工具，画出数据流向图",
                "识别最高频的跨系统数据同步需求",
                "用n8n搭建数据桥接管道"
            ],
            "expected_roi": "减少 80% 手动数据录入，降低人为错误率"
        })

    recs.append({
        "phase": "第三阶段（1-2个月）",
        "title": "构建数据看板",
        "tools": ["Metabase", "飞书仪表盘", "Google Data Studio"],
        "actions": [
            "确定老板每天需要关注的5个核心指标",
            "搭建自动更新的数据看板",
            "配置关键指标异常告警"
        ],
        "expected_roi": "老板每天节省 1-2 小时数据查看时间，决策效率提升"
    })

    return recs


def build_pdf(survey: dict, output_path: str) -> None:
    """生成PDF诊断报告"""
    font_name = setup_fonts()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    story = []

    def p_style(name, parent="Normal", **kwargs):
        return ParagraphStyle(name=name, parent=styles[parent],
                              fontName=font_name, **kwargs)

    title_style = p_style("Title", fontSize=24, textColor=COLOR_PRIMARY,
                          alignment=TA_CENTER, spaceAfter=6)
    subtitle_style = p_style("Subtitle", fontSize=12, textColor=COLOR_GRAY,
                             alignment=TA_CENTER, spaceAfter=20)
    h1_style = p_style("H1", fontSize=16, textColor=COLOR_PRIMARY,
                       spaceBefore=16, spaceAfter=8)
    h2_style = p_style("H2", fontSize=13, textColor=COLOR_ACCENT,
                       spaceBefore=12, spaceAfter=6)
    body_style = p_style("Body", fontSize=10, textColor=COLOR_TEXT,
                         leading=18, spaceAfter=8)
    small_style = p_style("Small", fontSize=9, textColor=COLOR_GRAY, spaceAfter=4)

    # ========= 封面 =========
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("企业自动化诊断报告", title_style))
    story.append(Paragraph("Automation Diagnosis Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_ACCENT))
    story.append(Spacer(1, 0.5*cm))

    company = survey.get("company_name", "贵公司")
    date_str = datetime.now().strftime("%Y年%m月%d日")
    story.append(Paragraph(f"客户：{company}", p_style("C1", fontSize=12, textColor=COLOR_TEXT)))
    story.append(Paragraph(f"报告日期：{date_str}", p_style("C2", fontSize=12, textColor=COLOR_GRAY)))
    story.append(Paragraph(f"报告出具：迈巴赫自动化咨询", p_style("C3", fontSize=12, textColor=COLOR_GRAY)))
    story.append(Spacer(1, 1*cm))

    # ========= 综合评分 =========
    scores = calculate_score(survey)
    level = scores["level"]
    story.append(Paragraph("01  综合评分", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_LIGHT_BG))
    story.append(Spacer(1, 0.3*cm))

    score_data = [
        ["评估维度", "得分", "满分"],
        ["工具整合度", str(scores["tool_integration"]), "25"],
        ["重复工作控制", str(scores["repetitive_work"]), "25"],
        ["自动化意识", str(scores["automation_awareness"]), "25"],
        ["数据互通程度", str(scores["data_connectivity"]), "25"],
        ["综合总分", str(scores["total"]), "100"],
    ]
    score_table = Table(score_data, colWidths=[9*cm, 3*cm, 3*cm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, -1), (-1, -1), COLOR_ACCENT),
        ("TEXTCOLOR", (0, -1), (-1, -1), HexColor("#FFFFFF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [COLOR_LIGHT_BG, HexColor("#FFFFFF")]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"综合评级：{level['label']}", h2_style))
    story.append(Paragraph(level["desc"], body_style))

    # ========= 痛点分析 =========
    story.append(PageBreak())
    story.append(Paragraph("02  核心痛点分析", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_LIGHT_BG))
    story.append(Spacer(1, 0.3*cm))

    pain_points = identify_pain_points(survey)
    if not pain_points:
        story.append(Paragraph("未发现明显痛点，建议持续优化现有流程。", body_style))
    else:
        for pp in pain_points:
            story.append(Paragraph(
                f"{pp['icon']} [{pp['priority']}] {pp['title']}",
                p_style(f"PP_{pp['title']}", fontSize=12, textColor=COLOR_TEXT,
                        spaceBefore=8, spaceAfter=4)
            ))
            story.append(Paragraph(pp["detail"], body_style))

    # ========= 改善建议 =========
    story.append(PageBreak())
    story.append(Paragraph("03  改善建议与实施路径", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_LIGHT_BG))
    story.append(Spacer(1, 0.3*cm))

    recs = generate_recommendations(survey, scores)
    for rec in recs:
        story.append(Paragraph(f"📌 {rec['phase']}：{rec['title']}", h2_style))
        story.append(Paragraph(
            f"推荐工具：{' / '.join(rec['tools'])}",
            p_style("ToolList", fontSize=10, textColor=COLOR_ACCENT, spaceAfter=4)
        ))
        for action in rec["actions"]:
            story.append(Paragraph(f"• {action}", body_style))
        story.append(Paragraph(
            f"预期效果：{rec['expected_roi']}",
            p_style("ROI", fontSize=10, textColor=COLOR_SUCCESS, spaceAfter=12)
        ))

    # ========= 结语 =========
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_ACCENT))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "如需进一步了解具体实施方案，欢迎联系我们进行深度咨询。",
        p_style("Footer", fontSize=10, textColor=COLOR_GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    print(f"[✓] 诊断报告已生成：{output_path}")


def main():
    parser = argparse.ArgumentParser(description="企业自动化诊断报告生成器")
    parser.add_argument("--input", required=True, help="调查问卷JSON文件路径")
    parser.add_argument("--output", default="diagnosis_report.pdf", help="输出PDF路径")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        survey = json.load(f)

    build_pdf(survey, args.output)


if __name__ == "__main__":
    main()
