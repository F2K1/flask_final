class User:
    def __init__(self, username, firstname, lastname, email, password, role, blocked):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role = role
        self.blocked = blocked

    # def __str__(self) -> str:
    #     return "<{} {}>".format(self.id, self.name)
    
    def serialize(self):
        return {
            'userid': self.userID, 
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'role': self.role,
            'blocked': self.blocked
        }


class Blog:
    def __init__(self, userID, title, content, date):
        self.userID = userID
        self.title = title
        self.content = content
        self.date = date

    def serialize(self):
        return {
            'blogid': self.blogID, 
            'userid': self.userID,
            'title': self.title,
            'content': self.content,
            'date': self.date
        }


class Comment:
    def __init__(self, userID, blogID, text, date):
        self.userID = userID
        self.blogID = blogID
        self.text = text
        self.date = date

    def serialize(self):
        return {
            'commentid': self.commentID,
            'userid': self.userID,
            'blogid': self.blogID,
            'text': self.text,
            'date': self.date
        }