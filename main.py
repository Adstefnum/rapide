from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    # Render a simple HTML page with a "Connect with LinkedIn" button that redirects to the authorization URL
    return '''
        <html>
            <body>
                <h1>Connect with LinkedIn</h1>
                <a href="https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={your_client_id}&redirect_uri=http://localhost:5000/callback&state=foobar&scope=r_liteprofile%20r_emailaddress%20w_member_social">Connect with LinkedIn</a>
            </body>
        </html>
    '''

@app.route("/callback")
def callback():
    # Retrieve the authorization code from the query parameters
    code = request.args.get("code")
    # Do something with the authorization code (e.g. exchange it for an access token)
    return f"Authorization code: {code}"

if __name__ == "__main__":
    app.run(debug=True)
