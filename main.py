from flask import Flask,request
from requests import post
from traceback import print_exc
import html
class A:
    def __init__(self):
        self.treeData=set()
        self.simulData={}
        self.debug=None
        self.call={'测试':self.test,'exec':self.exec,'get':self.get,
                   '挂树':self.addTree,'下树':self.eraseTree,'查树':self.getTree,'砍树':self.clearTree,
                   '模拟出刀':self.addSimul,'查看模拟刀':self.getSimul,'清空模拟刀':self.clearSimul}
    def exec(self):
        if self.param['sender']['user_id']!=979449732:
            return'__'
        try:
            exec(self.param['message'][6:])
            return'Done'
        except BaseException as e:
            return'错误:'+str(e)
    def get(slef):
        if self.param['sender']['user_id']!=979449732:
            return'__'
        try:
            return str(eval(self.param['message'][6:]))
        except BaseException as e:
            return'错误:'+str(e)
    def countTree(self):
        return'树上共%d人'%len(self.treeData)
    def check(self):
        return self.param['sender']['role']=='member'and self.param['sender']['user_id']!=979449732#权限狗的快乐
    def test(self):
        return'测试返回 '+str(self.cmd)
    def addTree(self):
        if len(self.cmd)==1:
            if self.sender in self.treeData:
                return'你已经在树上了'
            self.treeData.add(self.sender)
            return'已挂树,'+self.countTree()
        if self.check():
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
    def clearTree(self):
        if self.check():
            return'没有权限'
        self.treeData.clear()
        return'砍树成功'
    def eraseTree(self):
        if len(self.cmd)==1:
            if self.sender in self.treeData:
                self.treeData.remove(self.sender)
                return'下树成功'
            return'你不在树上'
        if self.check():
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
    def addSimul(self):
        if len(self.cmd)!=4:
            return'错误'
        try:
            self.simulData[self.sender]=(lambda cmd:[sum(cmd)]+cmd)([int(i)for i in self.cmd[1:]])
            return'数据添加成功,'+self.countSimul()
        except BaseException as e:
            return str(e)
    def getSimul(self):
        return self.countSimul()+'\n排名 用户 刀序 伤害\n'+'\n'.join(('%d  %s  %d  %d'%(i,*j)for i,j in enumerate(sorted(((i,j,self.simulData[i][j])for i in self.simulData for j in range(1,4)),key=lambda x:-x[2]))))
    def clearSimul(self):
        if self.check():
            return'没有权限'
        self.simulData.clear()
        return'清除成功'
    def __call__(self,param):
        try:
            if not param['message'].startswith('/'):
                return '__'
            print(param)
            self.param=param
            self.param['message']=html.unescape(self.param['message'])
            try:
                self.cmd=[i for i in self.param['message'].split(' ') if i]
                self.sender=(self.param['sender']['card']if self.param['sender']['card']else self.param['sender']['nickname']).replace(' ','_')
                return self.call[self.cmd[0][1:]]()
            except KeyError:
                return'错误'
        except KeyError:
            return'__'
        except:
            print_exc()
            return'__'
a=A()

app=Flask(__name__)
@app.route("/api",methods=['post','OPTIONS'])
def api():
    try:
        js=request.get_json()
        t=a(js)
        if t!='__':
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