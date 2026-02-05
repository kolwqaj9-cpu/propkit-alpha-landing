-- ============================================
-- Supabase purchase_intents 表创建脚本
-- ============================================

-- 步骤 1: 创建 purchase_intents 表
CREATE TABLE IF NOT EXISTS public.purchase_intents (
    id BIGSERIAL PRIMARY KEY,
    email TEXT,
    source TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 步骤 2: 添加索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_purchase_intents_created_at ON public.purchase_intents(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_purchase_intents_email ON public.purchase_intents(email) WHERE email IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_purchase_intents_source ON public.purchase_intents(source);

-- 步骤 3: 启用 Row Level Security (RLS)
ALTER TABLE public.purchase_intents ENABLE ROW LEVEL SECURITY;

-- 步骤 4: 创建策略 - 允许 service_role 完全访问（用于 API 调用）
CREATE POLICY "Allow service_role full access" ON public.purchase_intents
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- 步骤 5: 创建策略 - 允许匿名用户插入（用于前端插入数据）
CREATE POLICY "Allow anonymous insert" ON public.purchase_intents
    FOR INSERT
    TO anon
    WITH CHECK (true);

-- 步骤 6: 创建策略 - 允许匿名用户读取（用于 monitor 页面显示计数）
CREATE POLICY "Allow anonymous read" ON public.purchase_intents
    FOR SELECT
    TO anon
    USING (true);

-- 步骤 7: 添加注释说明
COMMENT ON TABLE public.purchase_intents IS '用户购买意向追踪表';
COMMENT ON COLUMN public.purchase_intents.id IS '主键，自增ID';
COMMENT ON COLUMN public.purchase_intents.email IS '用户邮箱（可选）';
COMMENT ON COLUMN public.purchase_intents.source IS '来源标识（如 Dashboard_Purchase_Button）';
COMMENT ON COLUMN public.purchase_intents.created_at IS '创建时间戳';

-- ============================================
-- 验证查询（可选，用于测试）
-- ============================================
-- SELECT COUNT(*) FROM public.purchase_intents;
-- SELECT * FROM public.purchase_intents ORDER BY created_at DESC LIMIT 10;
