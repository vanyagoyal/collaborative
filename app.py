#import libraries
from flask import Flask , request , render_template , jsonify , redirect , url_for , send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant

app = Flask(__name__)
fake = Faker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/token')
def generate_token() :
    TWILIO_ACCOUNT_SID = 'ACa66762e15908a9c10a5c3f132306ff53'
    TWILIO_SYNC_SERVICE_SID = 'IS3fac1b70bac51b15008f7aad8d0c386a'
    TWILIO_API_KEY = 'SKa19a1443defb64de631ee6546705b733'
    TWILIO_API_SECRET = '3PFPx2AcJuJoeGHnOYAuep0NE5VpBDqi'

    username = request.args.get('username' , fake.user_name())
    token = AccessToken(TWILIO_ACCOUNT_SID , TWILIO_API_KEY , TWILIO_API_SECRET , identity = username)
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity = username , token = token.to_jwt().decode())

@app.route('/' , methods = ['POST'])
def download_text() :
    text_from_notepad = request.form['text']

    with open('workfile.txt','w') as f :
        f.write(text_from_notepad)

    path_to_store_txt = 'workfile.txt'

    return send_file(path_to_store_txt , as_attachment = True)

if __name__ == "__main__":
    app.run()

