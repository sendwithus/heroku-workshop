import os

import bottle

from db import get_latest_messages, insert_message


MESSAGE_FORM = """
    <br><br>
    <h3>Post New Message</h3>
    <form action="/messages" method="post">
        Username:<br>
        <input name="username"><br>
        Message:<br>
        <textarea name="message"></textarea><br>
        <button type="submit">Submit</button>
    </form>
"""


@bottle.get('/')
def index():

    messages = get_latest_messages()

    html = '<h1>Heroku Workshop!</h1>'

    # List messages
    html += '<br><br>'
    html += '<h3>Latest Messages:</h3>'
    html += '<ul>'
    for message in messages:
        html += '<li>@%s: %s</li>' % (message['username'], message['text'])
    html += '</ul>'

    html += MESSAGE_FORM

    return html


@bottle.post('/messages')
def messages():
    username = bottle.request.forms.get('username')
    message = bottle.request.forms.get('message')

    print 'New Message: %s - %s' % (username, message)
    insert_message(username, message)

    bottle.redirect('/')


# Run server
if __name__ == '__main__':
    if 'PORT' in os.environ:
        bottle.run(host='0.0.0.0', port=os.environ['PORT'])
    else:
        bottle.run(host='localhost', port=8080)
