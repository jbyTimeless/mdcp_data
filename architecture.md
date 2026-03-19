mdcp_data/                    # 【父项目】根目录
├── common/                            # 【共享模块】全局共享（彻底扁平化）
│   ├── exceptions/                    # 直接放代码，无内层嵌套
│   ├── dependencies/
│   ├── utils/
│   ├── schemas/
│   ├── tests/
│   ├── __init__.py                    # 标记为 Python 包
│   └── pyproject.toml                 # 配置包含当前目录
│
├── config/                            # 【配置中心】全局配置（彻底扁平化）
│   ├── settings.py                    # 直接放代码
│   ├── env_loader.py
│   ├── tests/
│   ├── __init__.py                    # 标记为 Python 包
│   └── pyproject.toml                 # 配置包含当前目录
│
├── services/                          # 【业务服务集群】
│   └── dataset/               # 数据集服务（已扁平化）
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       ├── interfaces/
│       ├── alembic/
│       ├── tests/
│       ├── __init__.py
│       ├── main.py
│       ├── Dockerfile
│       └── pyproject.toml
│
├── docker/
├── scripts/
├── .env.example
├── .gitignore
└── README.md