-- ============================================
-- 批量插入 20 条测试数据以触发阈值
-- ============================================

-- 方法 1: 使用 generate_series（推荐，快速）
INSERT INTO public.purchase_intents (email, source)
SELECT 
    'threshold_test_' || generate_series || '@example.com',
    'Threshold_Test_Batch'
FROM generate_series(1, 20)
RETURNING id, email, source, created_at;

-- 执行后应该看到 20 行返回，表示插入成功
-- 然后访问 https://propkitai.tech/monitor.html 查看是否触发阈值
