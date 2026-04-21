# zbj-services

> 猪八戒平台服务交付工具集

三个核心产品的完整代码，可直接用于客户交付。

---

## 产品目录

### 1. AI数字人定制 (`heygen-digital-human/`)

调用 HeyGen API，根据客户文案自动生成数字人视频。

**核心文件：**
- `heygen_client.py` — 单条视频生成（主模块）
- `batch_generate.py` — 批量视频生成
- `.env.example` — 环境变量配置示例

**快速开始：**
```bash
pip install requests python-dotenv

# 复制环境变量
cp .env.example .env
# 填入你的 HeyGen API Key

# 查看可用数字人形象
python heygen_client.py --list-avatars

# 生成视频
python heygen_client.py \
  --script "欢迎来到我们的企业介绍..." \
  --avatar "avatar_id_here" \
  --voice "voice_id_here" \
  --output my_video.mp4 \
  --quality 1080p
```

**定价参考：**
| 套餐 | 内容 | 报价 |
|------|------|------|
| 基础版 | 60秒/1080P | ¥299 |
| 标准版 | 3分钟/1080P | ¥599 |
| 商务版 | 5分钟/4K | ¥1299 |
| 企业版 | 10分钟+ | ¥2999起 |

---

### 2. 跨境电商自动化 (`ecommerce-automation/`)

n8n 工作流 JSON，可直接导入 n8n 使用。

**工作流清单：**
- `01_order_processing.json` — 新订单自动处理（通知供应商+更新库存+微信推送）
- `02_daily_sales_report.json` — 每日早8点自动发送销售日报
- `03_bad_review_alert.json` — 每2小时巡检差评，发现立即预警

**导入方法：**
1. 打开你的 n8n 实例
2. 进入 Workflows → Import
3. 选择对应的 `.json` 文件
4. 配置 Credentials 和环境变量

**需要配置的环境变量：**
```
SHOPIFY_API_URL=https://your-store.myshopify.com/admin/api/2024-01
SHOPIFY_TOKEN=your_shopify_token
SUPPLIER_API_URL=https://your-supplier-api.com
INVENTORY_API_URL=https://your-inventory-api.com
NOTIFY_CHAT_ID=your_wechat_or_telegram_chat_id
AMAZON_SP_API_URL=https://sellingpartnerapi-na.amazon.com
AMAZON_TOKEN=your_amazon_sp_token
```

**定价参考：**
| 套餐 | 内容 | 报价 |
|------|------|------|
| 单流程 | 1个工作流 | ¥599 |
| 标准版 | 3个工作流 | ¥1499 |
| 专业版 | 全套6个+看板 | ¥2999 |
| 旗舰版 | 全定制 | ¥4999起 |

---

### 3. 企业自动化诊断 (`biz-diagnosis/`)

根据客户填写的问卷，自动生成专业诊断报告 PDF。

**核心文件：**
- `diagnosis_report.py` — 报告生成器
- `survey_example.json` — 问卷示例

**快速开始：**
```bash
pip install reportlab

# 填写客户问卷（基于示例修改）
cp survey_example.json client_survey.json
# 修改 client_survey.json 中的内容

# 生成报告
python diagnosis_report.py \
  --input client_survey.json \
  --output diagnosis_report.pdf
```

**问卷字段说明：**
| 字段 | 说明 | 示例值 |
|------|------|--------|
| company_name | 公司名称 | "示例科技有限公司" |
| team_size | 团队规模 | 15 |
| tools_used | 在用工具列表 | ["微信", "钉钉", "Excel"] |
| tool_integration_level | 工具整合程度 1-5 | 2 |
| repetitive_work_hours_per_week | 每周重复工作小时数 | 25 |
| data_silos_count | 数据孤岛数量 | 4 |
| automation_awareness | 自动化意识 1-5 | 3 |
| has_crm | 是否有CRM | false |
| report_generation_hours_per_week | 每周报表制作小时数 | 8 |

**定价参考：**
| 套餐 | 内容 | 报价 |
|------|------|------|
| 轻咨询 | 问卷+书面建议 | ¥299 |
| 标准咨询 | 视频沟通+完整报告 | ¥599 |
| 深度咨询 | 2次沟通+实施计划 | ¥999 |
| 陪跑服务 | 咨询+搭建+培训 | ¥2999起 |

---

## 获客策略

三个产品形成完整漏斗：

```
产品三（¥299轻咨询）→ 建立信任 → 产品一/二（高价交付）
产品一（快速出单）→ 积累好评 → 引流至产品二/三
```

## 上架建议

1. 先上产品三（门槛最低，最容易获客）
2. 同步上产品一（最容易出单）
3. 前5单降价冲好评
4. 产品二作为高价转化漏斗

---

*Made by 迈巴赫 🏎️*
