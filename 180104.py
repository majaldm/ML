
# coding: utf-8

# In[14]:


get_ipython().system(' pip install --user flask')


# In[31]:


from flask import Flask, request, make_response, jsonify

app = Flask('flask-api')

@app.route('/')
def hello_world():
    message = {'message': 'hello world'}
    return jsonify(message)


from ptt_crawler import PttCrawler

@app.route('/ptt_crawler', methods=['GET','POST'])
def run_crawler():
    if request.method == 'GET':
        crawler = PttCrawler('Gossiping', page=1)
    elif request.method == 'POST':
        board = request.get_json().get('board','Gossiping')
        page = request.get_json().get('page','1')
        crawler = PttCrawler(board, page=page)
    result = crawler.run()
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8000)


# In[37]:


print(app)
print('-------------------')
print(vars(app))
print('-------------------')
print(', '.join("%s: %s" % item for item in vars(app).items()))
print('-------------------')
print(app.__dict__)
print('-------------------')
print(dir(app))


# In[43]:


print(app.test_client())
print('-------------------')
print(vars(app.test_client()))
print('-------------------')
print(', '.join("%s: %s" % item for item in vars(app.test_client()).items()))
print('-------------------')
print(app.test_client().__dict__)
print('-------------------')
print(dir(app))


# In[45]:


print(app.test_client().get('/'))
print('-------------------')
print(vars(app.test_client().get('/')))
print('-------------------')
print(', '.join("%s: %s" % item for item in vars(app.test_client().get('/')).items()))
print('-------------------')
print(app.test_client().get('/').__dict__)
print('-------------------')
print(dir(app))


# In[13]:


import json

resp = app.test_client().get('/')
print(resp.data)
print(resp.data.decode())
print(json.loads(resp.data.decode()))


# In[10]:


from ptt_crawler import PttCrawler

crawler = PttCrawler('Gossiping', page=1)
result = crawler.run()
print(result)


# In[11]:


resp = app.test_client().get('/ptt_crawler')
print(resp.data)
print(json.loads(resp.data.decode()))


# In[32]:


resp = app.test_client().post(
    '/ptt_crawler',
    data=json.dumps({'board':'Baseball','page':3}),
    content_type='application/json'
)

print(json.loads(resp.data.decode()))

