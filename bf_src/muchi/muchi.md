## muchi.bf

### 概要
以下の文字列を出力します:
> "ﾑﾁｯ♡「ﾑﾁｯ♡ﾑﾁｯ♡」ﾑﾁｯ♡ﾑﾁｯ♡
>
>「ﾑﾁｯ♡ﾑﾁｯ♡…」
>
>
>ﾑﾁｯ♡「ﾑﾁｯ♡ﾑﾁｯ♡」ﾑｯﾁｨｲｲｲｲｲｲｲｲｲｲｲｲｯ♡♡♡♡ﾑｯﾁｨｲｲｲｲｲｲｲｲｲｲｲｲｯ♡♡♡♡
>
>ﾑﾁｯ♡ﾑﾁｯ♡!(ﾑﾁｯ♡ﾑﾁｯ♡)
>「ﾑﾁｯ♡ﾑﾁｯ♡!」
>
>ﾑﾁｯ♡「ﾑﾁｯ♡」ﾑﾁｯ♡

### 拡張
メモリ領域にコマンドとなる値を書き込むことで、以下の文字列からなる任意の文字列を構成できます:

| 値 | 文字列 |
| --: | :-- |
| 1 | ﾑﾁｯ♡ |
| 2 | \n |
| 3 | 「 |
| 4 | 」 |
| 5 | ! |
| 6 | ﾑｯﾁｨｲｲｲｲｲｲｲｲｲｲｲｲｯ♡♡♡♡ |
| 7 | ( |
| 8 | ) |
| >9 | ... |

したがってデフォルトのコマンド列は以下の通りです:
```
1, 4, 1, 3, 1, 2, 2, 4, 5, 1, 1, 3, 2, 8, 1, 1, 7, 5, 1, 1, 2, 2, 6, 6, 4, 1, 1, 3, 1, 2, 2, 4, 9, 1, 1, 3, 2, 2, 1, 1, 4, 1, 1, 3, 1
```
コマンドは終端側から処理されるため目的の文字列と逆順になることに留意してください。