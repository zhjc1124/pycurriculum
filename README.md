# pycurriculum

# 功能
自动登陆UIMS获取课程表
然后生成ics文件导入日历

# 如何使用
自行配置好selenium环境
```
pip install selenium, requests
python analyze.py
username,password
```
在目录下生成的ics文件既可导入到outlook中或者手机日历中

# 如何自行添加课程
```
from pycurriculum import Course, Curriculum
# 用课程名 教师 计划表来初始化课程
#            课程    教师        地点    周二1-4节 1-20的单周(单周为1，双周为2)
t1 = Course('课程二', '刘老师', [['三教', '2-1-4', '1-20-1'], ['三阶', '1-3-4', '4-10']])
t2 = Course(name='英语', teacher='何老师', schedule=['一阶', '3-1-2', '2-6-2'])
```
schedule包括地点，上课日与节数，周数

```
#用教学日历第一周的日期来初始化Curriculum
tc = Curriculum('2018-01-30')

# 添加课程
tc.add(t1)
tc.add(t2)

# 保存为test.ics文件
tc.to_ics('test')
```

# 相关
JLU_UIMS: https://github.com/zhjc1124/JLU_UIMS
