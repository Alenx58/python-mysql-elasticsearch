## 简介

一个 全量同步 MySQL 数据到 Elasticsearch的工具，大数据量情况下非读写内存。

纯 Python 编写，运行 python-mysql-elasticsearch 的唯三要求:

* python3.7
* redis
* elasticsearch

## 快速开始

从一个全量同步开始。

### 安装

```shell
python3 -m pip install requirements.txt
```

创建全量同步配置文件

```shell
python3 main.py
```

等待同步完成即可。

### 注意

全量同步完成后不会自动增量同步新修改的数据，需要增量同步请查看全部文档中的增量同步部分。
