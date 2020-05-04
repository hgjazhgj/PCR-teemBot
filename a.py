from flask import Flask,request,jsonify
from requests import post
import traceback
app=Flask(__name__)
class A:
    def __init__(self):
        self.tree=set()
        self.call={
            '测试':self.test,
            '挂树':self.hang,
            '查树':self.get,
            '砍树':self.clear
            }
    def test(self):
        return '测试返回'
    def hang(self):
        try:
            self.tree.add(self.pram['sender']['card'])
        except:
            self.tree.add(self.pram['sender']['nickname'])
        return '已挂树,当前树上%d人'%len(self.tree)
    def get(self):
        return '树上没人'if len(self.tree)==0else'\n'.join(self.tree)
    def clear(self):
        self.tree.clear()
        return '砍树成功'
    def __call__(self,pram):
        try:
            if pram['message'].startswith('/'):
                self.pram=pram
                try:
                    return self.call[pram['message'][1:]]()
                except:
                    traceback.print_exc()
                    return '错误'
        except:
            traceback.print_exc()
            return '__'
a=A()
@app.route("/api",methods=['post','OPTIONS'])
def api():
    try:
        js=request.get_json()
        print(js)
        t=a(js)
        if t!='__':post('http://localhost:5700/send_group_msg',data={'group_id':1036066961,'message':t})
        return b'done'
    except:
        traceback.print_exc()
        return b'fuck'

app.run(host='localhost',port=8000,debug=False)