# **[TryWordle](https://github.com/HeQianye/TryWodle)** #

## 项目意义

本项目借助Vue3框架以及ant-design组件库，精心打造了一款简易的[wordle](https://www.nytimes.com/games/wordle/index.html)猜词小游戏。其设计初衷是为了助力大家更好地复习英语单词，为此特别将词库限定在四级英语范围内，并且排除了词形变化的情况。当下，项目选用Sqlite作为数据库，要是有更新词汇单的需求，可考虑对wordle-back中的数据库内容进行相应修改。其表结构具体如下：

```sql
CREATE TABLE IF NOT EXISTS cet4_word (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cet4_word TEXT,
  cet4_phonetic TEXT,
  cet4_translate TEXT,
  cet4_distortion TEXT,
  cet4_phrase TEXT,
  cet4_samples TEXT
);
```

不过，该项目目前还存在一些有待改进之处：

其一，答案的验证逻辑放置在后端会更为合适；

其二，词汇库相对比较匮乏，暂时还没办法支持词形变化；

其三，项目的整体结构还不够规范。

## 项目启动方式

本项目的启动方式与一般的Vue3项目并无二致，具体步骤如下：

首先，需要安装node.js。

接着，在cmd或者powershell中执行以下指令来安装依赖：

```bash
npm install --legacy-peer-deps
```

然后，同样在cmd或者powershell中执行以下指令，以便进入调试模式：

```bash
npm run dev
```

此外，还需要运行wordle-back/main.py这个文件。
