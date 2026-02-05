-- ============================================
-- 刷新 Supabase Schema Cache
-- ============================================
-- 执行此 SQL 可以强制刷新 schema cache，让新创建的表立即可用

-- 方法 1: 通知 PostgREST 重新加载 schema
NOTIFY pgrst, 'reload schema';

-- 方法 2: 如果方法1不行，执行以下命令刷新
-- SELECT pg_notify('pgrst', 'reload schema');

-- 执行后等待 10-30 秒，然后重试 API 调用
