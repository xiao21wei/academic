# academic
## 软件包说明
`pymysql` 用于连接数据库

`pyyaml` 用于读取配置文件

## 配置文件说明
`secrets.yaml` 

用于存放不易上传的账号密码等信息，如数据库账号密码，邮箱账号密码等不需要上传至仓库，但是需要在本地运行的信息, 请在本地创建该文件，参考格式如下：
```yaml
DATABASE:
  name : xxx
  host : xxx
  port : xxx
  user : xxx
  password : xxx
```
在`setting.py`文件中的调用方法：
```python
import yaml
with open(BASE_DIR / 'secrets.yaml', 'r') as f:
    secrets = yaml.load(f, Loader=yaml.FullLoader)
    databases_name = secrets['DATABASE']['name']
    databases_user = secrets['DATABASE']['user']
    databases_password = secrets['DATABASE']['password']
    databases_host = secrets['DATABASE']['host']
    databases_port = secrets['DATABASE']['port']
```
运行时，需要将该文件存放位置为项目文件夹下，与`manage.py`文件夹同级

**不要将该文件上传至Github仓库**

## 运行说明
运行指令：
```shell
python manage.py makemigrations # 生成迁移文件
python manage.py migrate # 迁移数据库
python manage.py createsuperuser # 创建超级用户(可选)
python manage.py runserver # 运行
```
## 项目说明
### 项目结构
```shell
├── academic
│   ├── __init__.py
│   ├── __pycache__
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── my_app
│   ├── migrations
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── templates
├── manage.py
├── README.md
├── secrets.yaml
```

### 项目功能（已完成）
- [x] publish_achievement 发布成果
- [x] get_achievement 获取成果
- [x] get_achievements 获取成果列表
- [x] update_achievement 更新成果
- [x] delete_achievement 删除成果
- [x] get_achievement_by_type 获取成果列表（按类型）
- [x] get_achievement_by_area 获取成果列表（按领域）
- [x] get_achievement_by_name 获取成果列表（按名称）
- [x] get_achievement_by_author 获取成果列表（按作者）
- [x] get_achievement_by_time 获取成果列表（按时间）
- [x] send_verification_code 发送验证码
- [x] report_achievement 举报学术成果
- [x] check_report 审核举报
- [x] get_report 获取举报信息
- [x] get_report_list 获取举报列表
- [x] get_unchecked_report_list 获取未审核举报列表
- [x] get_checked_report_list 获取已审核举报列表
- [x] get_report_list_by_achievement 获取举报列表（按成果）
- [x] get_report_list_by_user 获取举报列表（按用户）
- [x] get_report_list_by_admin 获取举报列表（按管理员）
- [x] like_achievement 点赞学术成果
- [x] cancel_like_achievement 取消点赞学术成果
- [x] get_like_list_by_achievement 获取点赞列表（按成果）
- [x] get_like_list_by_user 获取点赞列表（按用户）
- [x] get_like_count_by_achievement 获取点赞数（按成果）
- [x] comment_achievement 评论学术成果
- [x] delete_comment 删除评论
- [x] get_comment_list_by_achievement 获取评论列表（按成果）
- [x] get_comment_list_by_user 获取评论列表（按用户）
- [x] get_comment_count_by_achievement 获取评论数（按成果）
- [x] get_comment_count_by_user 获取评论数（按用户）
- [x] collect_achievement 收藏学术成果
- [x] cancel_collect_achievement 取消收藏学术成果
- [x] get_collect_list_by_achievement 获取收藏列表（按成果）
- [x] get_collect_list_by_user 获取收藏列表（按用户）
- [x] get_collect_count_by_achievement 获取收藏数（按成果）
- [x] get_collect_count_by_user 获取收藏数（按用户）

### 项目功能（待完成）



