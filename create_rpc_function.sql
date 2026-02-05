-- ============================================
-- 创建 RPC 函数用于获取 purchase_intents 计数
-- 这个函数可以绕过 schema cache 问题
-- ============================================

-- 创建函数
CREATE OR REPLACE FUNCTION get_purchase_intents_count()
RETURNS bigint
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
    SELECT COUNT(*) FROM public.purchase_intents;
$$;

-- 授予执行权限给 anon 角色（用于前端调用）
GRANT EXECUTE ON FUNCTION get_purchase_intents_count() TO anon;
GRANT EXECUTE ON FUNCTION get_purchase_intents_count() TO authenticated;

-- 测试函数（可选）
-- SELECT get_purchase_intents_count();
