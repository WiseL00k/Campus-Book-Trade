from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from ratelimit.decorators import ratelimit

from app.forms import CommitForm, RegisterForm
from app.models import Product
from helpers import get_page_list


class IndexView(generic.ListView):
    """商品列表页：支持分类筛选、搜索和分页"""
    model = Product
    template_name = 'app/index.html'
    context_object_name = 'product_list'
    paginate_by = 15
    c = None  # 分类参数（0:供应，1:求购）
    q = None  # 搜索关键词

    def get_context_data(self, object_list=None, **kwargs):
        """补充上下文：分页数据、分类参数、搜索关键词"""
        context = super().get_context_data(object_list=object_list,** kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        context['page_list'] = get_page_list(paginator, page)  # 分页控件
        context['c'] = self.c  # 传递分类参数到模板
        context['q'] = self.q  # 传递搜索关键词到模板（用于回显）
        return context

    def get_queryset(self):
        """获取商品列表：支持分类筛选和搜索"""
        # 1. 获取分类参数（c）和搜索关键词（q）
        self.c = self.request.GET.get("c", None)
        self.q = self.request.GET.get("q", "").strip()  # 去除首尾空格

        # 基础查询：只显示已审核商品（status=1），按发布时间倒序
        queryset = Product.objects.filter(status=1).order_by('-timestamp')

        # 2. 应用分类筛选（如果有c参数）
        if self.c:
            queryset = queryset.filter(type=self.c)

        # 3. 应用搜索筛选（如果有关键词q）：模糊匹配标题
        if self.q:
            queryset = queryset.filter(title__icontains=self.q)

        return queryset


class DetailView(generic.DetailView):
    """商品详情页：展示单个商品的详细信息"""
    model = Product
    template_name = 'app/detail.html'
    context_object_name = 'product'  # 模板中使用的变量名

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class CommitView(generic.CreateView):
    """商品发布页：仅登录用户可访问，含频率限制"""
    model = Product
    form_class = CommitForm
    template_name = 'app/commit.html'

    @ratelimit(key='ip', rate='100/h')  # 限制每IP每小时最多100次提交
    def post(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.warning(request, "操作太频繁了，请1分钟后再试")
            return render(request, self.template_name, {'form': CommitForm()})
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "发布成功！您的商品已提交审核")
        return reverse('app:commit')


class CustomLoginView(LoginView):
    """自定义登录页：指定模板，已登录用户自动跳转"""
    template_name = 'app/login.html'
    redirect_authenticated_user = True  # 已登录用户访问登录页时自动跳转

    def get_success_url(self):
        return reverse('home')  # 登录成功返回首页


class CustomLogoutView(LogoutView):
    """自定义登出：登出后返回首页"""
    next_page = 'home'


class RegisterView(generic.FormView):
    """用户注册页：处理注册逻辑"""
    template_name = 'app/register.html'
    form_class = RegisterForm
    success_url = '/app/login/'  # 注册成功跳转登录页

    def form_valid(self, form):
        form.save()  # 保存新用户
        messages.success(self.request, "注册成功，请使用新账号登录")
        return super().form_valid(form)