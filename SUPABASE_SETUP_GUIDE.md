# Supabase purchase_intents 表创建指南

## 📋 前置条件
- 已拥有 Supabase 账户
- 已创建项目（项目 URL: `https://vlrdiajxxnangawfcgvk.supabase.co`）

## 🚀 创建步骤

### 方法一：使用 SQL Editor（推荐）

1. **登录 Supabase Dashboard**
   - 访问：https://app.supabase.com
   - 选择你的项目

2. **打开 SQL Editor**
   - 在左侧菜单栏点击 **"SQL Editor"**
   - 点击 **"New query"** 创建新查询

3. **执行 SQL 脚本**
   - 复制 `supabase_setup.sql` 文件中的全部内容
   - 粘贴到 SQL Editor 中
   - 点击 **"Run"** 或按 `Ctrl+Enter` 执行

4. **验证创建成功**
   - 在左侧菜单栏点击 **"Table Editor"**
   - 应该能看到 `purchase_intents` 表
   - 表结构应包含以下字段：
     - `id` (bigint, 主键)
     - `email` (text, 可为空)
     - `source` (text, 必填)
     - `created_at` (timestamptz, 默认当前时间)
     - `updated_at` (timestamptz, 默认当前时间)

### 方法二：使用 Table Editor（图形界面）

1. **打开 Table Editor**
   - 在左侧菜单栏点击 **"Table Editor"**
   - 点击 **"New table"**

2. **设置表名**
   - 表名：`purchase_intents`
   - Schema：`public`

3. **添加字段**
   - 点击 **"Add column"** 添加以下字段：
   
   | 字段名 | 类型 | 是否必填 | 默认值 | 说明 |
   |--------|------|----------|--------|------|
   | id | int8 (bigint) | ✅ | auto increment | 主键 |
   | email | text | ❌ | - | 用户邮箱 |
   | source | text | ✅ | - | 来源标识 |
   | created_at | timestamptz | ❌ | now() | 创建时间 |
   | updated_at | timestamptz | ❌ | now() | 更新时间 |

4. **设置主键**
   - 将 `id` 字段设置为 **Primary Key**
   - 启用 **"Is Identity"** 和 **"Is Generated"**

5. **启用 RLS (Row Level Security)**
   - 在表设置中找到 **"Enable Row Level Security"**
   - 勾选启用

6. **创建策略（可选，如果使用 SQL 方法则已自动创建）**
   - 在 **"Authentication" → "Policies"** 中为 `purchase_intents` 表创建策略：
     - **Insert Policy**: 允许 `anon` 角色插入
     - **Select Policy**: 允许 `anon` 角色读取

## ✅ 验证步骤

### 1. 测试插入数据
在 SQL Editor 中执行：
```sql
INSERT INTO public.purchase_intents (email, source)
VALUES ('test@example.com', 'Manual_Test');
```

### 2. 测试查询数据
```sql
SELECT COUNT(*) FROM public.purchase_intents;
SELECT * FROM public.purchase_intents ORDER BY created_at DESC LIMIT 10;
```

### 3. 测试前端功能
- 访问：https://propkitai.tech/index.html
- 点击 **"解锁完整报告"** 按钮
- 应该能成功插入数据（不再出现 404 错误）
- 访问：https://propkitai.tech/monitor.html
- 应该能看到计数增加

## 🔧 常见问题

### Q1: 执行 SQL 时提示权限错误
**解决方案：**
- 确保使用项目 Owner 账户登录
- 或者使用 service_role key 通过 API 执行

### Q2: 前端插入数据时返回 403 Forbidden
**解决方案：**
- 检查 RLS 策略是否正确创建
- 确保 `anon` 角色有 INSERT 权限
- 在 SQL Editor 中重新执行策略创建语句

### Q3: Monitor 页面显示 0，但数据已插入
**解决方案：**
- 检查 `monitor.html` 中的 Supabase URL 和 Key 是否正确
- 确认表的 schema 是 `public`
- 检查网络请求是否成功（浏览器开发者工具）

## 📝 表结构说明

```sql
purchase_intents
├── id (BIGSERIAL PRIMARY KEY)        # 自增主键
├── email (TEXT)                       # 用户邮箱，可为空
├── source (TEXT NOT NULL)             # 来源标识，如 "Dashboard_Purchase_Button"
├── created_at (TIMESTAMPTZ)           # 创建时间，默认 NOW()
└── updated_at (TIMESTAMPTZ)           # 更新时间，默认 NOW()
```

## 🎯 完成后的下一步

1. **测试插入功能**
   - 在 index.html 页面点击购买按钮
   - 检查是否成功插入数据

2. **测试监控功能**
   - 访问 monitor.html
   - 验证计数是否正确显示
   - 插入 20 条数据后，验证是否触发绿色显示和成功消息

3. **反馈结果**
   - 如果遇到问题，请提供错误信息
   - 如果成功，告诉我，我会再次运行自动化测试验证阈值功能
