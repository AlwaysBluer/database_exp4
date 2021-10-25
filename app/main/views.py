from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app import utils
from app.models import CfgNotify, store, canteen, dish, user_info, deal, store_manager_info
from app.main.forms import CfgNotifyForm, StoreForm, DishForm, UserForm, DealForm
from . import main
import datetime

logger = get_logger(__name__)
cfg = get_config()


def store_query_filter(DynamicModel, id):
    #店铺要筛选掉不属于它的菜品，（dynamicmodel : dish, filter:store_id）
    # 不属于它的deal(dynamicmodel:deal, filter:store_id)
    #id是用户id
    model = current_user
    store_id = model.store_id #所属商铺编号
    query = DynamicModel.select().where(DynamicModel.store_id == store_id)
    return query

def user_query_filter(DynamicModel, id):
# 顾客要筛选掉不属于它的deal(dynamicmodel:deal, filter:user_id)
    query = DynamicModel.select().where(DynamicModel.user_id == id)
    return query



# 通用列表查询
def common_list(DynamicModel,view, ReliantModel=None):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            model = DynamicModel.get(DynamicModel.id == id)
            model.delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    # query = DynamicModel.select()
    print('current_user:', current_user.user_type)
    print('current_user id:', current_user)
    if current_user.user_type ==  'user' and DynamicModel == deal:
        query = user_query_filter(DynamicModel=DynamicModel, id=current_user.id)
    elif current_user.user_type == 'store_manager':
        query = store_query_filter(DynamicModel=DynamicModel, id=current_user.id)
    # 获得所有数据
    else:
        query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)
    content = utils.query_to_list(query)
    total_page = math.ceil(total_count / length)
    diction = {'content': content, 'total_count': total_count,
            'total_page': total_page, 'page': page, 'length': length}
    return render_template(view, form=diction, reliant=ReliantModel, current_user=current_user)

# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            # store_num = model.save()
            # print(store_num)
            dict_ = utils.obj_to_dict(model) #model转字典
            try:
                DynamicModel.create(**dict_)
                flash('保存成功')
            except:
                utils.flash_errors(form)
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    # # return redirect(url_for('main.index'))
     return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required#直接就是食堂管理员
def index():
    if session['login_type'] == 'user':
        return render_template('user_index.html', current_user=current_user)
    elif session['login_type'] == 'canteen_manager':
        return render_template('index.html', current_user=current_user)
    elif session['login_type'] == 'store_manager':
        return render_template('store_manager_index.html', current_user=current_user)
    else:
        return render_template('errors/404.html')



# 通知方式查询
@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    # return common_list(DynamicModel=CfgNotify, view='notifylist.html')
    return common_list(DynamicModel=store,ReliantModel=canteen, view='storelist.html')


# 通知方式配置
@main.route('/notifyedit', methods=['GET', 'POST'])
@login_required
def notifyedit():
    # return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit.html')
    return common_edit(DynamicModel=store, form=StoreForm(), view='storeedit.html')

#查询菜品信息
@main.route('/dishlist', methods=['GET', 'POST'])
@login_required
def dishlist():
    # if current_user.user_type == 'user':
    #     return common_list(DynamicModel=dish, ReliantModel=store, view='dishlist.html')
    # elif current_user.user_type == 'store_manager':
    #     return common_list(DynamicModel=dish, ReliantModel=store, view='')
    return common_list(DynamicModel=dish, ReliantModel=store, view='dishlist.html')

#编辑菜品信息
@main.route('/dishedit', methods=['GET', 'POST'])
@login_required
def dishedit():
    return common_edit(DynamicModel=dish, form=DishForm(), view='dishedit.html')

#查询用户信息
@main.route('/userlist', methods=['GET', 'POST'])
@login_required
def userlist():
    return common_list(DynamicModel=user_info, ReliantModel=None, view='userlist.html')

#编辑用户信息
@main.route('/useredit', methods=['GET', 'POST'])
@login_required
def useredit():
    return common_edit(DynamicModel=user_info, form=UserForm(), view='useredit.html')

#查询订单信息
@main.route('/deallist', methods=['GET', 'POST'])
@login_required
def deallist():
    return common_list(DynamicModel=deal, ReliantModel=user_info, view='deallist.html')

#编辑订单信息
@main.route('/dealedit', methods=['GET', 'POST'])
@login_required
def dealedit():
    return common_edit(DynamicModel=deal, form=DealForm(), view='dealedit.html')

@main.route('/oderdish/<dish_id>', methods=['GET', 'POST'])
@login_required
def orderdish(dish_id):

    model = dish.get(dish.id == dish_id)
    store_id = model.store_id
    create_deal(store_id)
    return common_list(DynamicModel=deal, ReliantModel=user_info, view='deallist.html')



def create_deal(store_id):
    query = deal.select()
    num = query.count()
    deal_dict = {}
    deal_dict['id'] = utils.strID_increase(num)
    deal_dict['is_finish'] = False
    deal_dict['deal_begin_time'] = datetime.datetime.now()
    deal_dict['deal_finish_time'] = datetime.datetime.now()
    deal_dict['user_id'] = current_user.id
    deal_dict['store_id'] = store_id
    deal.create(**deal_dict)
    flash('创建成功')
