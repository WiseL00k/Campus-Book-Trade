**二手商品交易平台**
这是一个基于 Python Django 框架开发的二手商品交易信息发布平台。

**项目简介**
该项目是一个简单的供需信息发布网站，允许用户发布供应和需求信息。主要功能包括：

浏览供应和需求信息
发布新的供需信息
查看详细信息
信息分类浏览
基于有效期的信息管理
开发环境和技术栈：

**依赖说明**
本项目使用的第三方库及主要组件版本：

- Django 3.2.11: Web框架
- PyMySQL 1.0.2: MySQL数据库驱动
- matplotlib 3.7.5: 图表绘制库(如用于数据可视化)
- numpy 1.24.4: 数值计算基础库
- pillow 10.4.0: 图像处理库
- 其他辅助库详见 requirements.txt
**演示地址**
http://mask.gitapp.cn


**首页展示**

![](https://github.com/geeeeeeeek/mask/blob/master/static/img/demo01.png)


**发布页**

![](https://github.com/geeeeeeeek/mask/blob/master/static/img/demo02.png)


**详情页**

![](https://github.com/geeeeeeeek/mask/blob/master/static/img/demo03.png)


**运行步骤**
安装依赖包：

pip install -r requirements.txt
配置数据库：

创建 MySQL 数据库 python_mask
在 mask/settings.py 中配置数据库连接信息
恢复数据库结构：python manage.py migrate

为了能够访问后台管理系统，需要创建一个超级用户账户：
python manage.py createsuperuser


启动开发服务器：
python manage.py runserver
访问应用：

前台页面：在浏览器中访问 http://127.0.0.1:8000/ 查看网站首页
管理后台：在浏览器中访问 http://127.0.0.1:8000/admin/ 进入后台管理系统（使用上面创建的超级用户账户）

**项目结构说明**
mask/                 # Django项目配置文件夹
├── settings.py       # 项目配置文件
├── urls.py           # 主URL配置
└── wsgi.py           # WSGI部署配置

app/                  # 主应用文件夹
├── models.py         # 数据模型定义
├── views.py          # 视图处理逻辑
├── forms.py          # 表单处理
├── urls.py           # 应用URL配置
├── admin.py          # 后台管理配置
└── migrations/       # 数据库迁移文件

templates/            # 模板文件夹
├── app/              # 应用模板
└── base/             # 基础模板

static/               # 静态文件夹
├── css/              # 样式文件
└── js/               # JavaScript文件

**主要功能模块**
1. 首页 (Index)
展示所有已审核通过的供需信息
支持按照供应/需求类型筛选
分页显示信息列表
2. 信息发布 (Commit)
提供表单供用户发布供需信息
包含标题、类型、有效期、联系方式等字段
支持防重复提交机制
3. 详情页 (Detail)
显示特定供需信息的详细内容
4. 后台管理
通过Django Admin管理供需信息
可以审核、编辑、删除信息

**数据模型**

主要数据模型为 Product，包含以下字段：

title: 标题
type: 类型（供应/需求）
contact: 联系人
phone: 手机号
weixin: 微信号
location: 所在地
expire: 有效期（天）
status: 状态（是否审核通过）
timestamp: 发布时间

**自定义模板标签**
项目包含自定义模板标签 app_tag：

time_since: 显示相对发布时间
check_expire: 检查信息是否过期

**部署注意事项**
修改 mask/settings.py 中的 SECRET_KEY
设置 DEBUG = False 用于生产环境
配置合适的数据库连接
配置静态文件收集和部署