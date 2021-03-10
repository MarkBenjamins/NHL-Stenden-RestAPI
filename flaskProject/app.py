from flask import Flask

app = Flask(__name__)


@app.route('/Mark/<mark>')
def abc(mark):
    return (mark + " ") * 2


if __name__ == '__main__':
    app.run()

