# 我在校园磨人精

这是一段很折磨人的代码：我在校园催打卡，即获取当天健康打卡未打卡的名单，发送到班级微信群里（当事人看到后应该很社s的吧），那么废话不多说，看看食用必读：



- 首先你需要是我在校园的班委，否则没有权限看到未打卡名单
- 这里用到了`wxpy`库，如果你的python环境没有这个库的话，在`cmd`执行`pip install wxpy`命令安装即可
- 运行代码是需要手机扫码登录的，登录原理是微信网页版，因此登录后pc端微信会下线~



大概就这些，作者现阶段因为太忙啦，发布这个也是应读者的要求；这个代码也是很久之前写的，代码很菜轻喷，目前也只有健康打卡的催打卡，后续内容有时间再玩玩吧~

哦对了，首次运行可能会有点慢需要耐心一点，因为会加载你的微信通讯录，来找到发送目标（班级群）