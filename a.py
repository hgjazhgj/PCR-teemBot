from flask import Flask,request,jsonify
from requests import post
from traceback import print_exc

class A:
    def __init__(self):
        self.tree=set()
        self.call={'测试':self.test,'挂树':self.add,'查树':self.get,'砍树':self.clear,'下树':self.erase}
    def test(self):
        return '测试返回'
    def add(self):
        if len(self.cmd)==1:
            if self.sender in self.tree:
                return '你已经在树上了'
            self.tree.add(self.sender)
            return '已挂树,当前树上%d人'%len(self.tree)
        if self.param['sender']['role']=='member'and self.sender!='hgjazhgj':
            return '没有权限'
        ans=''
        for i in self.cmd[1:]:
            if i in self.tree:
                ans+=i+' 添加失败\n'
                continue
            self.tree.add(i)
            ans+=i+' 添加成功\n'
        return ans+'当前树上%d人'%len(self.tree)
    def get(self):
        return '树上共%d人\n'%len(self.tree)+'\n'.join(('%2d. %s'%(i,j)for i,j in enumerate(self.tree)))
    def clear(self):
        if self.param['sender']['role']=='member'and self.sender!='hgjazhgj':
            return '没有权限'
        self.tree.clear()
        return '砍树成功'
    def erase(self):
        if len(self.cmd)==1:
            if self.sender in self.tree:
                self.tree.remove(self.sender)
                return '下树成功'
            return '你不在树上'
        if self.param['sender']['role']=='member'and self.sender!='hgjazhgj':
            return '没有权限'
        ans=''
        for i in self.cmd[1:]:
            if i in self.tree:
                self.tree.remove(i)
                ans+=i+' 移除成功\n'
                continue
            ans+=i+' 移除失败\n'
        return ans+'当前树上%d人'%len(self.tree)
    def __call__(self,param):
        try:
            if not param['message'].startswith('/'):
                return '__'
            self.param=param
            try:
                seld.cmd=[i for i in param['message'].split(' ') if i]
                self.sender=param['sender']['card']if param['sender']['card']else param['sender']['nickname']
                return self.call[self.cmd[0][1:]]()
            except KeyError:
                return '错误'
        except:
            print_exc()
            return '__'
a=A()

app=Flask(__name__)
@app.route("/api",methods=['post','OPTIONS'])
def api():
    try:
        js=request.get_json()
        print(js)
        t=a(js)
        if t!='__':
            post('http://localhost:5700/send_group_msg',data={'group_id':js['group_id'],'message':t})
        return b'Done'
    except KeyError:
        return b'KeyError'
    except:
        print_exc()
        return b'Fuck'

app.run(host='localhost',port=8000,debug=False)