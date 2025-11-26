## 项目概述

### 项目背景

随着高校教学活动与校园生活的持续进行，教材、辅导资料与课外读物在学期末与专业调整时常被闲置。传统的线下交换信息零散、效率低且缺乏信任保障；而通用二手平台缺乏面向校园的实名认证与配送闭环，无法很好满足校园场景的特殊需求。

为缓解教材浪费、降低学术资源获取成本并构建校园内部循环生态，本项目拟设计并实现一套**面向高校的二手书交易平台——“书屋（Campus Book Trade）”**，为师生提供便捷、安全、高效的书籍流通渠道。

### 项目名称

**项目名称：书屋（Campus Book Trade）**

### 项目定位

“书屋”定位为校园内**C2C 为主、辅以 B2C 的混合型电子商务平台**，以学生二手书交易为核心，集成学生实名认证、校园社交、校内配送与智能推荐等功能，目标成为校园内可信赖的书籍流通与知识共享平台。

### **运行步骤**

安装依赖包：

```bash
pip install -r requirements.txt
```

配置数据库：

创建 MySQL 数据库 python_mask
在 mask/settings.py 中配置数据库连接信息
恢复数据库结构：python manage.py migrate
创建管理员账户（可选）：

```bash
python manage.py createsuperuser
```

运行项目：

```bash
python manage.py runserver
```

访问应用：

前台页面：http://127.0.0.1:8000/
管理后台：http://127.0.0.1:8000/admin/

### **项目结构说明**

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

### **主要功能模块**

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

### **数据模型**

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

### **自定义模板标签**

项目包含自定义模板标签 app_tag：

time_since: 显示相对发布时间
check_expire: 检查信息是否过期

### **部署注意事项**

修改 mask/settings.py 中的 SECRET_KEY
设置 DEBUG = False 用于生产环境
配置合适的数据库连接
配置静态文件收集和部署

### 启动项目 

```
django-admin startproject mask
```

### 创建应用

```
python3 manage.py startapp app
```

### model设计

主要是对需求表Product进行设计，在此项目中，我们需要标题、联系人、电话等字段。可参考models.py文件。

设计字段如下：

```python
class Product(models.Model):
    list_display = ("title", "type", "location")
    title = models.CharField(max_length=100,blank=True, null=True)
    type = models.IntegerField(default=0)
    pv = models.IntegerField(default=0)
    contact = models.CharField(max_length=10,blank=True, null=True)
    location = models.CharField(max_length=20,blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    weixin = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    expire = models.IntegerField(default=1)
```

### 业务编写

本项目一共分为3个页面，分别是列表页、详情页、提交页。

我们一一讲解

#### 首页

首先是首页，它的模版位于templates/app/index.html  它主要是用来展示首页内容， 并提交搜索词，到搜索接口，所有的接口都位于app/urls.py里面，如下

```python
app_name = 'app'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('commit', views.CommitView.as_view(), name='commit')
]
```

我们设置首页的路由为IndexView， 开始编写IndexView的代码。它的代码非常简单：

```python
class IndexView(generic.ListView):
    model = Product
    template_name = 'app/index.html'
    context_object_name = 'product_list'
    paginate_by = 15
    c = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['c'] = self.c
        context['page_list'] = page_list
        return context

    def get_queryset(self):
        self.c = self.request.GET.get("c", None)
        if self.c:
            return Product.objects.filter(type=self.c).order_by('-timestamp')
        else:
            return Product.objects.filter(status=0).order_by('-timestamp')

```


#### 详情页

我们再来开发详情页，从urls.py中看到，详情页是由DetailView来实现的，我们来窥探它的全貌：

```python
class DetailView(generic.DetailView):
    model = Product
    template_name = 'app/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context
```

它很简单，继承了DetailView通用模板类来显示详情。

#### 提交页

最后再来看一下提交页，它是由CommitView来实现的。同样是观看代码：

```python
class CommitView(generic.CreateView):

    model = Product
    form_class = CommitForm
    template_name = 'app/commit.html'

    @ratelimit(key='ip', rate='2/m')
    def post(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.warning(self.request, "操作太频繁了，请1分钟后再试")
            return render(request, 'app/commit.html', {'form': CommitForm()})
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "发布成功! ")
        return reverse('app:commit')
```

它是继承自CreateView，因为是创建操作嘛，在post中，我们通过ratelimit来限制提交次数，防止恶意提交。

### 运行项目

```
python3 manage.py runserver
```

