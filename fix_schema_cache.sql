-- ============================================
-- 强制刷新 Supabase Schema Cache
-- ============================================

-- 方法 1: 通知 PostgREST 重新加载（已执行过，可能需要多次）
NOTIFY pgrst, 'reload schema';

-- 方法 2: 如果方法1不行，尝试重启 PostgREST
-- 在 Supabase Dashboard: Settings → API → Restart Project

-- 方法 3: 检查表是否在正确的 schema 中
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE tablename = 'purchase_intents';

-- 方法 4: 验证表权限
SELECT 
    grantee,
    privilege_type
FROM information_schema.role_table_grants
WHERE table_name = 'purchase_intents'
AND table_schema = 'public';

-- 方法 5: 创建一个 RPC 函数作为备用方案（如果 API 还是不行）
CREATE OR REPLACE FUNCTION get_purchase_intents_count()
RETURNS bigint
LANGUAGE sql
SECURITY DEFINER
AS $$
    SELECT COUNT(*) FROM public.purchase_intents;
$$;

-- 测试 RPC 函数
-- SELECT get_purchase_intents_count();
