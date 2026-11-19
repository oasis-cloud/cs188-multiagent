# 极大极小搜索的测试题

1.

```
                 MAX
               /     \
             A         B
            MIN       MIN
           /  \      /  \
          3    5    2    9
```

- 进入 A 时的 Alpha、Beta。
  Alpha = -inf，Beta = +️inf
- A 看完 3 时的 Alpha、Beta。
  beta = min(+inf，3)
  alpha = -inf
- A 看完 5 时，A 返回什么？
  beta = min(3, 5)
  alpha = -inf
  return 3
- 根节点 Alpha 更新为多少？
  根节点 max, alpha = max(-inf, 3)
  beta = +inf
- 进入 B 时，Alpha、Beta 是多少？
  Alpha = 3, beta = +inf
- B 返回什么？
  看 2 的时候，beta = min(+inf, 2)
  这时 alpha > beta, 剪枝 9
- 最终 MAX 选择哪个？
  选择 A

2.

```
                 MAX
               /     \
             A         B
            MIN       MIN
           /  \      /  \
          3    5    2    9
```

- A 搜索完以后，根节点的 Alpha 是多少？
  根节点 max, alpha = max(-inf, 3)
  beta = +inf
- 进入 B 后，MIN 先看到 2，Beta 变成多少？
  beta = min(+inf, 2)
- 此时是否满足剪枝条件？满足
- 9 是否需要搜索？否
