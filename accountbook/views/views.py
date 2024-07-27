from django.views import generic
from django.shortcuts import render, redirect
from django.db.models import Sum
from ..models import Account, Category
from ..forms.accountbook.forms import RegisterForm, CategoryRegisterer


# htmlファイルを表示させる関数
class Home(generic.TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = super(Home, self).get_context_data()
        return render(request, 'home.html', context)


class Register(generic.TemplateView):
    template_name = 'register.html'
    form_class = RegisterForm
    object = None

    def create(request):
        if request.method == 'GET':
            inputdata = RegisterForm()
            data = {'data': inputdata}
            return render(request, 'accountbook/register.html', data)

        if request.method == 'POST':
            category = Category.objects.get(id=request.POST['category'])
            contents = request.POST['contents']
            date = request.POST['date']
            amount = request.POST['amount']
            account = Account(category=category, contents=contents, date=date, amount=amount)
            account.save()
            return redirect(to='/accountbook/inquiry')


# カテゴリーの登録
class CategoryRegister(generic.TemplateView):
    template_name = 'category.html'
    form_class = CategoryRegisterer
    object = None

    def create(request):
        if request.method == 'GET':
            inputdata = CategoryRegisterer()
            data = {'data': inputdata}
            return render(request, 'accountbook/category.html', data)

        if request.method == 'POST':
            latest = Category.objects.order_by('category_id').last().category_id + 1
            category_id = latest
            category = request.POST['category']
            flag = request.POST['flag']
            newcategory = Category(category_id=category_id, category=category, flag=flag)
            newcategory.save()
            return redirect(to='/accountbook/inquiry')


class Change(generic.TemplateView):
    model = Account
    template_name = 'change.html'

    def get(self, request, *args, **kwargs):
        data = Account.objects.all()
        params = {'data': data}
        return render(request, 'accountbook/change.html', params)


class DataChange(generic.TemplateView):
    model = Account
    template_name = 'datachange.html'

    def change(request, pk):
        if request.method == 'GET':
            inputdata = RegisterForm()
            beforedata = Account.objects.get(pk=pk)
            params = {'data': inputdata,
                      'before': beforedata,
                      }
            return render(request, 'accountbook/datachange.html', params)

        if request.method == 'POST':
            data = Account.objects.get(pk=pk)
            data.category = Category.objects.get(id=request.POST['category'])
            data.contents = request.POST['contents']
            data.date = request.POST['date']
            data.amount = request.POST['amount']
            data.save()
            return redirect(to='/accountbook/inquiry')


class Inquiry(generic.TemplateView):
    template_name = 'account.html'
    model = Account, Category

    def get(self, request, *args, **kwargs):
        data = Account.objects.all()
        incomelist = Category.objects.filter(flag='in')
        expenselist = Category.objects.filter(flag='out')
        incomedata = Account.objects.filter(category__in=incomelist).aggregate(result=Sum('amount'))
        expensedata = Account.objects.filter(category__in=expenselist).aggregate(result=Sum('amount'))
        income = incomedata['result']
        if incomedata['result'] is None: income = 0
        expense = expensedata['result']
        if expensedata['result'] is None: expense = 0
        params = {'data': data,
                  'income': income,
                  'expense': expense,
                  }
        return render(request, 'accountbook/account.html', params)


class Delete(generic.TemplateView):
    model = Account
    template_name = 'change.html'

    def get(self, request, *args, **kwargs):
        self.object = Account.objects.get(pk=kwargs['pk'])
        self.object.delete()
        return redirect(to='/accountbook/change')
