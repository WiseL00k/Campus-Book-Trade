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
    model = Product
    template_name = 'app/index.html'
    context_object_name = 'product_list'
    paginate_by = 15
    c = None

    # 修复第24行：参数定义去掉多余的逗号，使用标准语法
    def get_context_data(self, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(object_list=object_list,** kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['c'] = self.c
        context['page_list'] = page_list
        return context

    def get_queryset(self):
        self.c = self.request.GET.get("c", None)
        if self.c:
            return Product.objects.filter(type=self.c).filter(status=1).order_by('-timestamp')
        else:
            return Product.objects.filter(status=1).order_by('-timestamp')


class DetailView(generic.DetailView):
    model = Product
    template_name = 'app/detail.html'
    context_object_name = 'product'  # 补充：明确模板变量名

    def get_object(self, queryset=None):
        obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(** kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class CommitView(generic.CreateView):
    model = Product
    form_class = CommitForm
    template_name = 'app/commit.html'

    @ratelimit(key='ip', rate='100/h')
    def post(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.warning(self.request, "操作太频繁了，请1分钟后再试")
            return render(request, 'app/commit.html', {'form': CommitForm()})
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "发布成功! ")
        return reverse('app:commit')


class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('home')


class CustomLogoutView(LogoutView):
    next_page = 'home'


class RegisterView(generic.FormView):
    template_name = 'app/register.html'
    form_class = RegisterForm
    success_url = '/app/login/'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "注册成功，请登录！")
        return super().form_valid(form)