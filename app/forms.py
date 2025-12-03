from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Product  # 关联Product模型


class CommitForm(forms.ModelForm):
    class Meta:
        model = Product
        # 只包含Product模型中实际存在的字段（移除不存在的description）
        fields = ['title', 'type', 'contact', 'location', 'phone', 'weixin']  # 新增location（模型中有该字段）
        widgets = {
            # 可根据需要为字段添加样式，不涉及不存在的字段
            'title': forms.TextInput(attrs={'placeholder': '请输入商品标题'}),
            'location': forms.TextInput(attrs={'placeholder': '请输入地点'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'placeholder': '可选邮箱'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '请输入用户名'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("用户名长度不能少于3个字符")
        return username