﻿from flask import Flask,request
from requests import post
from traceback import print_exc
import html
import re
import time

def check(x=0):#白名单1检查锁2群主管理员可用4成员可用
    def wrapper(func):
        def inner(self,*args,**kwargs):
            if self.param['sender']['user_id']==979449732:#是我就直接放行,不管锁没锁
                return func(self,*args,**kwargs)
            if x&1 and self.locked:
                return'禁止访问'
            return func(self,*args,**kwargs)if x&2and self.param['sender']['role']!='member'or x&4and self.param['sender']['role']=='member'else'没有权限'
        return inner
    return wrapper

class A:
    def __init__(self):
        self.treeData=set()
        self.simulData={}
        self.debug=None
        self.locked=False
        self.call={'在?':self.test,'exec':self.exec,'eval':self.eval,'lock':self.lock,'unlock':self.unlock,
                   '挂树':self.addTree,'下树':self.eraseTree,'查树':self.getTree,'砍树':self.clearTree,
                   '模拟出刀':self.addSimul,'查看模拟刀':self.getSimul,'清空模拟刀':self.clearSimul}
    @check()
    def lock(self):
        self.locked=True
        return'完成'
    @check()
    def unlock(self):
        self.locked=False
        return'完成'
    @check()
    def exec(self):
        try:
            exec(self.param['message'][6:])
            return'完成'
        except BaseException as e:
            return'错误:'+str(e)
    @check()
    def eval(self):
        try:
            return str(eval(self.param['message'][6:]))
        except BaseException as e:
            return'错误:'+str(e)
    def countTree(self):
        return'树上共%d人'%len(self.treeData)
    def test(self):
        return'在 '+str(self.cmd)
    @check(7)
    def addTree(self):
        if len(self.cmd)==1:
            if self.sender in self.treeData:
                return'你已经在树上了'
            self.treeData.add(self.sender)
            return'已挂树,'+self.countTree()
        if self.param['sender']['role']=='member':
            return'没有权限'
        ans=''
        for i in self.cmd[1:]:
            if i in self.treeData:
                ans+=i+' 添加失败\n'
                continue
            self.treeData.add(i)
            ans+=i+' 添加成功\n'
        return ans+self.countTree()
    def getTree(self):
        return self.countTree()+'\n'+'\n'.join((str(i+1)+'.'+('  'if i<9else'')+j for i,j in enumerate(self.treeData)))
    @check(3)
    def clearTree(self):
        self.treeData.clear()
        return'砍树成功'
    @check(7)
    def eraseTree(self):
        if len(self.cmd)==1:
            if self.sender in self.treeData:
                self.treeData.remove(self.sender)
                return'下树成功'
            return'你不在树上'
        if self.param['sender']['role']=='member':
            return'没有权限'
        ans=''
        for i in self.cmd[1:]:
            if i in self.treeData:
                self.treeData.remove(i)
                ans+=i+' 移除成功\n'
                continue
            ans+=i+' 移除失败\n'
        return ans+self.countTree()
    def countSimul(self):
        return'已有%d模拟刀'%len(self.simulData)
    @check(7)
    def addSimul(self):
        if len(self.cmd)!=4:
            return'错误:需要正好3个参数'
        try:
            self.simulData[self.sender]=(lambda cmd:[sum(cmd)]+cmd)([int(i)for i in self.cmd[1:]])
            return'数据添加成功,'+self.countSimul()
        except BaseException as e:
            return str(e)
    def getSimul(self):
        return self.countSimul()+'\n排名_用户_刀序_伤害\n'+'\n'.join(('%d_%s_%d_%d'%(i,*j)for i,j in enumerate(sorted(((i,j,self.simulData[i][j])for i in self.simulData for j in range(1,4)),key=lambda x:-x[2]))))
    @check(3)
    def clearSimul(self):
        self.simulData.clear()
        return'清除成功'
    def __call__(self,param):
        try:
            param['message']=html.unescape(param['message'])
            self.param=param
            if param['message'].startswith('`'):
                return param['message']
            if param['message'].startswith('!'):
                ans=[]
                for s in re.findall(r'[0-9+\-*/().%<>|&^]+',param['message']):
                    try:
                        t=str(eval(ans))
                    except:
                        continue
                    if s!=t:
                        ans.append(s+'='+t)
                if ans:
                    return'\n'.join(ans)
                else:
                    return'错误:未找到表达式'
            if not param['message'].startswith(':'):
                return'__'
            try:
                self.cmd=[i for i in param['message'].split(' ') if i]
                self.sender=(param['sender']['card']if param['sender']['card']else param['sender']['nickname']).replace(' ','_')
                return self.call[self.cmd[0][1:]]()
            except KeyError:
                return'错误:找不到指令'
        except KeyError:
            return'__'
        except:
            print_exc()
            return'__'
a=A()

app=Flask(__name__)
@app.route("/api",methods=['post'])
def api():
    try:
        js=request.get_json()
        t=a(js)
        if t!='__':
            print(time.strftime('%Y-%m-%d_%H.%M.%S',time.localtime(js['time'])),js['sender'])
            print(js['message'])
            print(t)
            while t:
                post('http://localhost:5700/send_group_msg',data={'group_id':js['group_id'],'message':t[:120]})
                t=t[120:]
        return b'Done'
    except KeyError:
        return b'KeyError'
    except:
        print_exc()
        return b'Fuck'
app.run(host='localhost',port=8000,debug=False)