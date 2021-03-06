from flask import Flask, request, render_template, redirect
from tellonym import Tellonym as tellonymClient

WrongCredentialsError = Exception(
    'you have provided a wrong username password combination')
UnauthorizedError = Exception(
    'we failed to provide a correct auth_token. are you logged in?')
UserNotFoundError = Exception(
    'the user_id you have entered does not belong to any user.')
InvalidParameterError = Exception(
    'an invalid parameter was send to the api endpoint. please contact the author of this module')
UnknownError = Exception(
    'an unknown error has occured, please inform the author of this module')

app = Flask(__name__)

client = False


@app.route("/")
def home():
    global client
    hideOnLogin = "d-none"
    displayOnLogin = ""
    if(not client):
        hideOnLogin = ""
        displayOnLogin = "d-none"
    return render_template('home.html', home_active="active", display_on_login=displayOnLogin, hide_on_login=hideOnLogin)


@app.route("/tells", methods=['POST'])
def tells():
    username = request.form['username']
    password = request.form['password']
    global client
    if(not client):
        client = tellonymClient.Tellonym(username, password)

    allTells = client.get_tells()
    nonspam = []
    spam = []

    for tell in allTells:
        tellContent = tell.tell
        if ("Tell" in tellContent or "tell" in tellContent):
            nonspam.append(tellContent)
        else:
            spam.append(tellContent)

    spamReturn = ""
    nonspamReturn = ""

    for non_tell in nonspam:
        nonspamReturn += non_tell
        nonspamReturn += "\n"
    for spam_tell in spam:
        spamReturn += spam_tell
        spamReturn += "\n"
    return render_template('tells.html', tells=True, nonspam_tells=nonspamReturn, spam_tells=spamReturn)


@app.route("/tells")
def tellsSignedIn():
    global client
    if(not client):
        return redirect('/')
    allTells = client.get_tells()
    nonspam = []
    spam = []

    for tell in allTells:
        tellContent = tell.tell
        if ("Tell" in tellContent or "tell" in tellContent):
            nonspam.append(tellContent)
        else:
            spam.append(tellContent)

    spamReturn = ""
    nonspamReturn = ""

    for non_tell in nonspam:
        nonspamReturn += non_tell
        nonspamReturn += "\n"
    for spam_tell in spam:
        spamReturn += spam_tell
        spamReturn += "\n"
    return render_template('tells.html', tells=True, nonspam_tells=nonspamReturn, spam_tells=spamReturn)


@app.errorhandler(404)
def page_not_found(e):
    print(client)
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


"""
class ManyWrongCredentials(Exception):
    pass

@app.errorhandler(ManyWrongCredentials)
def wrong_credentials(e):
    # note that we set the 404 status explicitly
    return render_template('wrong-credentials.html'), 404

@app.route('/test_exception')
def test_exception():
    raise ManyWrongCredentials('just testing :)')
"""

heroku = Heroku(app)

if __name__ == "__main__":
    app.run(debug=True)
