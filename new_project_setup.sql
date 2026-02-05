-- ============================================
-- 新项目 Supabase 设置脚本
-- Project: kolwqaj9-cpu's Project
-- Project ID: ndwfvkclnrfetyvwkess
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

-- 步骤 7: 创建 RPC 函数用于获取计数（绕过 schema cache）
CREATE OR REPLACE FUNCTION get_purchase_intents_count()
RETURNS bigint
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
    SELECT COUNT(*) FROM public.purchase_intents;
$$;

-- 步骤 8: 授予 RPC 函数执行权限
GRANT EXECUTE ON FUNCTION get_purchase_intents_count() TO anon;
GRANT EXECUTE ON FUNCTION get_purchase_intents_count() TO authenticated;
GRANT EXECUTE ON FUNCTION get_purchase_intents_count() TO service_role;

-- 步骤 9: 强制刷新 schema cache
NOTIFY pgrst, 'reload schema';

-- ============================================
-- 验证查询（可选，用于测试）
-- ============================================
-- 测试插入
-- INSERT INTO public.purchase_intents (email, source)
-- VALUES ('test@example.com', 'Manual_Test')
-- RETURNING *;

-- 测试 RPC 函数
-- SELECT get_purchase_intents_count();

-- 查看所有记录
-- SELECT * FROM public.purchase_intents ORDER BY created_at DESC LIMIT 10;
