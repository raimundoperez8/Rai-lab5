from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdfs.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Pdf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    psw = db.Column(db.String(50))
    ip = db.Column(db.String(50))
    so = db.Column(db.String(50))
    ver = db.Column(db.String(50))

    def __init__(self, psw, ip, so, ver):
        self.psw = psw
        self.ip = ip
        self.so = so
        self.ver = ver


db.create_all()


class PdfSchema(ma.Schema):
    class Meta:
        fields = ('id', 'psw', 'ip', 'so', 'ver')


pdf_schema = PdfSchema()
pdfs_schema = PdfSchema(many=True)


@app.route('/')
def table():
    all_pdfs = Pdf.query.all()
    result = pdfs_schema.dump(all_pdfs)
    aux = []
    for i in range(len(result)):
        aux.append((result[i]["psw"], result[i]["ip"], result[i]["so"], result[i]["ver"]))
        print(aux)
    return render_template("table.html", data=aux)


@app.route('/pdfs', methods=['Post'])
def add_pdf():
    psw = request.json['psw']
    ip = request.json['ip']
    so = request.json['so']
    ver = request.json['ver']

    new_pdf = Pdf(psw, ip, so, ver)

    db.session.add(new_pdf)
    db.session.commit()
    return pdf_schema.jsonify(new_pdf)


@app.route('/pdfs', methods=['GET'])
def get_pdfs():
    all_pdfs = Pdf.query.all()
    result = pdfs_schema.dump(all_pdfs)
    print(result[0]["id"])
    return jsonify(result)


@app.route('/pdfs/<id>', methods=['DELETE'])
def delete_pdf(id):
    pdf = Pdf.query.get(id)
    db.session.delete(pdf)
    db.session.commit()
    return pdf_schema.jsonify(pdf)


if __name__ == "__main__":
    app.run(debug=True)
