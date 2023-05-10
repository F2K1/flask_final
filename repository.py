from flask import request, session, g
from db import *
from models import *


#check if the user session is still valid
def checkUser():
    user_id = session.get("user_id")
    if user_id == None:
        g.user = None
        return "no"
    else:
        db = getConnection()
        g.user = db.execute("SELECT * FROM users WHERE userID=?", (user_id,)).fetchone()
        return "yes"

#get latest blogs
def getLatestBlogs(latest_blogs_list):
    db = getConnection()
    latest_blogs_list = db.execute("SELECT * FROM blogs ORDER BY date ASC")
    latest_blogs_list = db.execute("SELECT * FROM blogs").fetchall()
    return latest_blogs_list

#get user's blogs
def getUsersBlogs(blogs_list):
    checkUser()
    if g.user == None:
        return None
    else:
        db = getConnection()
        blogs_list = db.execute("SELECT * FROM blogs WHERE userID=?", (g.user[0],)).fetchall()
        return [blogs_list, g.user[1], g.user[6]]
    
#get individual blog's details
def getBlogDetails(blog_id):
    db = getConnection()
    blog = db.execute("SELECT * FROM blogs WHERE blogID=?", (blog_id,)).fetchone()
    comments_list = db.execute("SELECT text FROM comments WHERE blogID=?", (blog_id,)).fetchall()
    return [blog, comments_list]


#get users
def getUsers():
    db = getConnection()
    checkUser()
    users_list = db.execute("SELECT userID, username FROM users WHERE userID!=1").fetchall()
    return [users_list, g.user]

#admin block user
def blockUser(userid):
    db = getConnection()
    db.execute("UPDATE users SET blocked=1 WHERE userID=?", (userid,))
    db.commit()

    return g.user

#admin unblock user
def unblockUser(userid):
    db = getConnection()
    db.execute("UPDATE users SET blocked=0 WHERE userID=?", (userid,))
    db.commit()

    return g.user

#admin set user as author
def setasAuthor(userid):
    db = getConnection()
    db.execute("UPDATE users SET role='author' WHERE userID=?", (userid,))
    db.commit()

    return g.user

#admin unset user as author
def unsetasAuthor(userid):
    db = getConnection()
    db.execute("UPDATE users SET role='user' WHERE userID=?", (userid,))
    db.commit()

    return g.user


#add user comment
def addComment(blog_id, comment, date):
    db = getConnection()
    model = Comment(g.user[0], blog_id, comment, date)
    db.execute("INSERT INTO comments(userID, blogID, text, date) VALUES(?, ?, ?, ?)", (model.userID, model.blogID, model.text, model.date))
    db.commit()

    return blog_id


#add author blog
def addBlog(title, content, date):
    db = getConnection()
    model = Blog(g.user[0], title, content, date)
    db.execute("INSERT INTO blogs(userID, title, content, date) VALUES(?, ?, ?, ?)", (model.userID, model.title, model.content, model.date))
    db.commit()

    return g.user

#update author blog
def updateBlog(blogid, title, content, date):
    db = getConnection()
    db.execute("UPDATE blogs SET userID=?, title=?, content=?, date=? WHERE blogID=?", (g.user[0], title, content, date, blogid))
    db.commit()

    return g.user

#delete author blog
def deleteBlog(blogid):
    db = getConnection()
    db.execute("DELETE FROM blogs WHERE blogID=?", (blogid))
    db.commit()

    return g.user

    
#login user
def login(error, username, password):
    db = getConnection()
    user = db.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()

    if user == None:
        error = "User doesn't exist! Please create an account to continue!"
        return [error, ""]

    elif password != user[5]:
        error = "Invalid Credentials!"
        return [error, ""]
    
    elif user[7] == 1:
        error = "This account has been blocked!"
        return [error, ""]

    else:
        session.clear()
        session["user_id"] = user[0]
        if user[6] == "admin":
            return [error, "admin"]
        else:
            return [error, "notadmin"]
                    
#logout user
def logout():
    print(session) #test
    session.clear()

#signin user
def signin(error, username, firstname, lastname, email, password):
    if request.method == "POST":
        db = getConnection()
        usernames_list = db.execute("SELECT username FROM users").fetchall()

        if username in usernames_list:
            error = "Username Taken! Please select another username."
            return [error, ""]
        
        else:
            model = User(username, firstname, lastname, email, password, "user", 0)
            db.execute("INSERT INTO users(username, firstname, lastname, email, password, role, blocked) VALUES(?, ?, ?, ?, ?, ?, ?)", (model.username, model.firstname, model.lastname, model.email, model.password, model.role, model.blocked))
            db.commit()
