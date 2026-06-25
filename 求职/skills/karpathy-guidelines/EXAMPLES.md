# Karpathy Guidelines — Examples

> 来源：github.com/multica-ai/andrej-karpathy-skills
> 用途：每个原则的正例/反例，帮助判断何时该做、何时不该做

---

## 原则 1：先思考再编码 Think Before Coding

### ✅ 正例：提出多种解读

用户说："The button should save the form."

AI 响应：
"Two interpretations:
1. Save to localStorage (draft persistence)
2. Save to backend via API (submits the form)

Which do you want? I'd suggest (1) for drafts and (2) if this is a submit button."

### ❌ 反例：悄悄选了一个

用户说："The button should save the form."

AI 响应：[直接实现 localStorage 版本，没问用户意图]

---

## 原则 2：简洁优先 Simplicity First

### ❌ 反例：过度设计（8 行 → 80 行）

```typescript
// ❌ 用户只要一个 10 分钟缓存
const CACHE_TTL = 10 * 60 * 1000;
let cached: { data: T; ts: number } | null = null;

async function getOrgs() {
  if (cached && Date.now() - cached.ts < CACHE_TTL) return cached.data;
  const data = await fetchOrgs();
  cached = { data, ts: Date.now() };
  return data;
}
```

AI 重写为：
```typescript
// ❌ 加了一堆没要求的东西
type CacheEntry<T> = { value: T; expiry: number };
type CacheOptions = { ttlMs?: number; maxSize?: number; evictionPolicy?: 'lru' | 'fifo' };
const DEFAULTS = { ttlMs: 600_000, maxSize: 100, evictionPolicy: 'lru' } as const;

class Cache<T> {
  private store = new Map<string, CacheEntry<T>>();
  private opts: Required<CacheOptions>;
  constructor(opts: CacheOptions = {}) { this.opts = { ...DEFAULTS, ...opts }; }
  // ... 70 more lines
}
```

### ✅ 正例：保持简单

```typescript
// ✅ 就是 10 分钟缓存，就这样
const CACHE_TTL = 10 * 60 * 1000;
let cached: { data: T; ts: number } | null = null;

async function getOrgs() {
  if (cached && Date.now() - cached.ts < CACHE_TTL) return cached.data;
  const data = await fetchOrgs();
  cached = { data, ts: Date.now() };
  return data;
}
```

> **判断标准**：如果一个资深工程师看了你的代码会说"这也太复杂了吧"——那就是过度设计了。

---

## 原则 3：外科手术式改动 Surgical Changes

### ❌ 反例：被要求改一个函数，顺手重构了三个

用户说："Fix the error handling in processOrder()."

AI 响应的 diff：
```
 // processOrder 的错误处理修复 ✅ 该改
+ try { ... } catch (e) { ... }

 // 但 AI 还顺手改了这些 ❌ 没人要求
- function validate(item) { return item != null; }
+ function validate(item: Item | null | undefined): item is Item {
+   return item !== null && item !== undefined;
+ }
- // Old logging approach
- console.log('user', user)
+ logger.info('user authenticated', { userId: user.id })
```

### ✅ 正例：只改被要求的部分

用户说："Fix the error handling in processOrder()."

AI 响应：
```
 // 只改了 processOrder 的错误处理
+ try {
+   validateOrder(order);
+ } catch (e) {
+   return { error: 'Invalid order', details: e.message };
+ }

 // 注意到但没改的问题（提了一嘴）
 AI: "I noticed validateUser() has an off-by-one error on line 45.
      Want me to fix that separately?"
```

---

## 原则 4：目标驱动执行 Goal-Driven Execution

### ❌ 反例：弱成功标准

用户说："Make the dashboard load faster."

AI 响应：
```
Plan:
1. Add caching
2. Optimize queries
3. Add loading spinner
```

### ✅ 正例：强成功标准

用户说："Make the dashboard load faster."

AI 响应：
```
Plan:
1. Profile current load time → verify: document baseline (e.g., 4.2s LCP)
2. Add query caching for top 3 slow queries → verify: same queries < 100ms
3. Lazy-load chart components → verify: LCP < 2s on slow 3G

Success: LCP under 2 seconds, measured with Chrome DevTools throttling.
```

> **判断标准**：如果成功标准是"让它跑起来"——这不是标准，这是愿望。真正的标准是你能独立验证"做完了没有"。

---

## 牛马生态使用提示

1. **原则 1+2 在写新代码时强制执行**——先对齐认知，再写最少代码
2. **原则 3 在改已有代码时强制执行**——只碰必须碰的
3. **原则 4 在 debug/多步任务时强制执行**——定义可验证的成功标准
4. **简单任务可跳过**——配置修改、明确指令、一行 fix 不需要全套流程
