# 公主连结Re:Dive群机器人
配合酷Q食用  
使用了CQHTTP插件  
垃圾实现,能用就行  
每一个版本中都含有大量的bug,慎用  

# 支持的命令
## /测试 [参数列表]
返回解析后的参数  
## /挂树 [参数列表]
将消息发送者挂树,如果提供了参数,则改为将参数依次挂树,普通用户不可提供参数  
## /下树 [参数列表]
将消息发送者下树,如果提供了参数,则改为将参数依次下树,普通用户不可提供参数  
## /查树
查看树上都有那些小可爱  
## /砍树
Boss终于被打完了,全员下树,普通用户不可调用该命令  
## /模拟出刀 <第一刀伤害> <第二刀伤害> <第三刀伤害>
添加模拟刀  
## /查看模拟刀
查看当前的模拟刀列表,以刀为单位降序  
## /清空模拟刀
Boss被打完了,清空模拟刀数据

# 更新日志
## 2020/05/05 v1.1
各处优化  
## 2020/05/05 v1.0
开了个后门直接执行python代码,假装有个控制台  
添加模拟刀  
## 2020/05/05 v0.7
修改异常处理逻辑  
人名中可能有空格,但是命令参数以空格分隔,故以下划线替代空格  
## 2020/05/05 v0.6
由于可选参数加入,群机器人可能试图发送很长的信息,比如全员挂树的指令就会发送大约2500字节的消息,这超过了http请求的限制  
现在会分割成120字符(最大占1080字节)的小段分批次发送  
增强了安全性检查  
## 2020/05/05 v0.5
挂树功能基本定型  
添加命令说明  
## 2020/05/05 v0.4
更改代码结构  
优化显示  
## 2020/05/05 v0.3
增加命令后参数  
添加一些安全检查  
增加权限检查  