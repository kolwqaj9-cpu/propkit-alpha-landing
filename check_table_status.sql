-- ============================================
-- 检查 purchase_intents 表状态
-- ============================================

-- 1. 确认表是否存在
SELECT 
    table_schema,
    table_name,
    table_type
FROM information_schema.tables
WHERE table_name = 'purchase_intents'
AND table_schema = 'public';

-- 2. 检查 RLS 是否启用
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables
WHERE tablename = 'purchase_intents'
AND schemaname = 'public';

-- 3. 检查 RLS 策略
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename = 'purchase_intents'
AND schemaname = 'public';

-- 4. 检查表权限
SELECT 
    grantee,
    privilege_type
FROM information_schema.role_table_grants
WHERE table_name = 'purchase_intents'
AND table_schema = 'public';

-- 5. 强制刷新 schema（如果上面的检查都正常）
NOTIFY pgrst, 'reload schema';

-- 6. 测试插入（可选，用于验证）
-- INSERT INTO public.purchase_intents (email, source)
-- VALUES ('test@example.com', 'Manual_Test')
-- RETURNING *;
