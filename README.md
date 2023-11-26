# llm4reversi_dev

## 输入规则

黑棋先走，黑子在棋盘上表示为1(X)。白棋在棋盘上表示为-1(O)。空位表示为0。输入为一个64维的数组。

## 动作输出

返回一个0到63的整数，表示下棋的位置。下棋位置顺序为从左到右，从上到下。左上角为0，右上角为7，左下角为56，右下角为63：

```text
0  1  2  3  4  5  6  7
8  9  10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63

```

## Install

```commandline
pip install -e .
```

## Play with LLM locally

```commandline
# on Linux/Mac
bash run_web.sh

# on Windows
cd web && python run.py
```

Then visit: http://localhost:10086/

## Play on QQ Game

```commandline
cd qq_game && python run.py
```

