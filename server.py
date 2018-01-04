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
