from flask import Flask, redirect, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from jisho_api.tokenize import Tokens
import json, csv, urllib.request, urllib.parse, ssl

ssl._create_default_https_context = ssl._create_unverified_context
MEANINGS_LIMIT = 3
DEF_AUDIO = ''
DEF_IMAGEURI = ''
DEF_IKNOWID = ''
DEF_IKNOWTYPE = ''
DEF_TAG = ''
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'
db = SQLAlchemy(app)


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(200))
    meaning = db.Column(db.String(200))
    reading = db.Column(db.String(200))
    audio = db.Column(db.String(200))
    image_URI = db.Column(db.String(200))
    iKnowID = db.Column(db.String(200))
    iKnowType = db.Column(db.String(200))
    tag = db.Column(db.String(200))


@app.route("/")
def index():
    db.session.commit()
    cards = Cards.query.order_by(Cards.id)
    return render_template("index.html", cards=cards)

@app.route("/generate", methods=["POST"])
def generate():
    if request.method == "POST":
        if not request.form.get("sentences"):
            return redirect("/")
        sentences = request.form.get("sentences")
        if "\n" in sentences:
            for sentence in sentences.split("\n"):
                cards = makeCards(sentence)
                for card in cards:
                    new_card = Cards(expression=card['expression'], meaning=card['meaning'], reading=card['reading'], audio=card['audio'], image_URI=card['image_URI'], iKnowID=card['iKnowID'], iKnowType=card['iKnowType'], tag=card['tag'])
                    try:
                        db.session.add(new_card)
                        db.session.commit()
                    except:
                        return "There was an error adding a card"
        else:
            cards = makeCards(sentences)
            for card in cards:
                    new_card = Cards(expression=card['expression'], meaning=card['meaning'], reading=card['reading'], audio=card['audio'], image_URI=card['image_URI'], iKnowID=card['iKnowID'], iKnowType=card['iKnowType'], tag=card['tag'])
                    try:
                        db.session.add(new_card)
                        db.session.commit()
                    except:
                        return "There was an error adding a card"
        return redirect("/")

@app.route("/clear", methods=["POST"])
def clear():
    if request.method == "POST":
        db.session.query(Cards).delete()
        db.session.commit()
        return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    card_to_delete = Cards.query.get_or_404(id)
    try:
        db.session.delete(card_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was an error deleting a card"

@app.route("/download", methods=["GET"])
def download():
    to_write = db.session.query(Cards).all()
    with open("test_file.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for i in to_write:
            writer.writerow([i.expression, i.meaning, i.reading, i.audio, i.image_URI, i.iKnowID, i.iKnowType, i.tag])
    return send_file('test_file.csv', mimetype='text/csv', attachment_filename='output.csv', as_attachment=True)

@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        id = request.form.get('row') or ''
        row = Cards.query.get(id)
        row.expression = request.form.get('expression') or ''
        row.meaning = request.form.get('meaning') or ''
        row.reading = request.form.get('reading') or ''
        row.audio = request.form.get('audio') or ''
        row.image_URI = request.form.get('image_URI') or ''
        row.iKnowID = request.form.get('iKnowID') or ''
        row.iKnowType = request.form.get('iKnowType') or ''
        row.tag = request.form.get('Tag') or ''
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating a card"

@app.route("/settings", methods=["POST", "GET"])
def settings():
    if request.method == "POST":
        global MEANINGS_LIMIT
        global DEF_AUDIO
        global DEF_IMAGEURI
        global DEF_IKNOWID
        global DEF_IKNOWTYPE
        global DEF_TAG
        MEANINGS_LIMIT = int(request.form.get('limit')) or 3
        DEF_AUDIO = request.form.get('audio') or ''
        DEF_IMAGEURI = request.form.get('image_URI') or ''
        DEF_IKNOWID = request.form.get('iKnowID') or ''
        DEF_IKNOWTYPE = request.form.get('iKnowType') or ''
        DEF_TAG = request.form.get("Tag") or ''
        return redirect("/settings")
    else:
        return render_template("settings.html", limit=MEANINGS_LIMIT, audio=DEF_AUDIO, image_URI=DEF_IMAGEURI, iKnowID=DEF_IKNOWID, iKnowType=DEF_IKNOWTYPE, Tag=DEF_TAG)

@app.route("/default")
def default():
    global MEANINGS_LIMIT
    global DEF_AUDIO
    global DEF_IMAGEURI
    global DEF_IKNOWID
    global DEF_IKNOWTYPE
    global DEF_TAG
    MEANINGS_LIMIT = 3
    DEF_AUDIO = ''
    DEF_IMAGEURI = ''
    DEF_IKNOWID = ''
    DEF_IKNOWTYPE = ''
    DEF_TAG = ''
    return redirect("/settings")
# Card maker code ------------------------

def makeCards(sentence):
    to_write = []
    if '\n' in sentence:
        sentence.split("\n")
    vocabs = getVocabs(sentence)
    
    if vocabs:
        for vocab in vocabs:
            with urllib.request.urlopen("https://jisho.org/api/v1/search/words?keyword=" + urllib.parse.quote(vocab, encoding='utf-8')) as url:
                data = json.loads("["+ url.read().decode() + "]")[0]

            if data["data"] != []:
                expression = getExpression(sentence, vocab)
                meaning = getMeaning(data, MEANINGS_LIMIT)
                reading = data["data"][0]["japanese"][0].get("reading")
                audio = DEF_AUDIO
                image_URI = DEF_IMAGEURI
                iKnowID = DEF_IKNOWID
                iKnowType = DEF_IKNOWTYPE
                tag = DEF_TAG
                to_write.append({'expression':expression, 'meaning':meaning, 'reading':reading, 'audio':audio, 'image_URI':image_URI, 'iKnowID':iKnowID, 'iKnowType':iKnowType, 'tag':tag})
    return to_write

def getMeaning(data_dict, limit=99):
    temp = ["; ".join(i["english_definitions"]) for i in data_dict["data"][0]["senses"]]
    ctr = 1
    meaning = ""
    for i in temp:
        if ctr == len(temp):
            meaning += str(ctr) + ". " + i
        else:
            meaning += str(ctr) + ". " + i + "\n"
        ctr += 1
        if ctr > limit:
            break
    return meaning

def getExpression(sentence, word):
    index = sentence.find(word)
    new_sentence = sentence[:index] + '「' + word + '」' + sentence[index + len(word):]
    return new_sentence

def getVocabs(sentence):
    if Tokens.request(sentence) == None:
        return None
    r = json.loads(Tokens.request(sentence).json())
    temp = []
    for i in r['data']:
        if i['pos_tag'] not in ['Particle', 'Determiner']:
            temp.append(i['token'])
    return temp

if __name__ == "__main__":
    app.run()