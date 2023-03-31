from flask import Flask, render_template, request, session, redirect, url_for, g
import sqlite3
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'jiejfirjeijrrcm4334qjdwx293r82ud2few2ed' #bad practice
app.config['SESSION_TYPE'] = 'filesystem'


# Database Setup (here bad practice)
def connectDb():
    conn = sqlite3.connect("blog.db")
    return conn

def createTables():
    db = connectDb()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users
        (userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        blocked INTEGER NOT NULL)
    """)
    db.commit

    db.execute("""
        CREATE TABLE IF NOT EXISTS blogs
        (blogID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(userID) REFERENCES users(userID))
    """)
    db.commit

    db.execute("""
        CREATE TABLE IF NOT EXISTS comments
        (commentID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        blogID INTEGER,
        text TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(userID) REFERENCES users(userID),
        FOREIGN KEY(blogID) REFERENCES blogs(blogID))
    """)
    db.commit

createTables() #creates the database

def checkUser():
    user_id = session.get("user_id")
    if user_id == None:
        g.user = None
    else:
        db = connectDb()
        g.user = db.execute("SELECT * FROM users WHERE userID=?", (user_id,)).fetchone()


@app.route("/")
def routeToHome(latest_blogs_list=None):
    db = connectDb()
    latest_blogs_list = db.execute("SELECT * FROM blogs ORDER BY date ASC")
    latest_blogs_list = db.execute("SELECT * FROM blogs").fetchall()
    return render_template("index.html", len=len(latest_blogs_list), latest_blogs_list=latest_blogs_list)

@app.route("/profile")
def routeToProfile(blogs_list=None):
    checkUser()
    if g.user == None:
        return redirect(url_for("routeToLogin"))
    else:
        db = connectDb()
        blogs_list = db.execute("SELECT * FROM blogs WHERE userID=?", (g.user[0],)).fetchall()
        return render_template("profile.html", username=g.user[1], role=g.user[6], len=len(blogs_list), blogs_list=blogs_list)

@app.route("/view-blog/<blog_id>")
def routeToViewBlog(blog_id):
    db = connectDb()
    blog = db.execute("SELECT * FROM blogs WHERE blogID=?", (blog_id,)).fetchone()
    comments_list = db.execute("SELECT text FROM comments WHERE blogID=?", (blog_id,)).fetchall()
    return render_template("view_blog.html", blog=blog, length=len(comments_list), comments_list=comments_list)

@app.route("/dashboard")
def routeToDashboard():
    db = connectDb()
    checkUser()
    users_list = db.execute("SELECT userID, username FROM users WHERE userID!=1").fetchall()
    return render_template("dashboard.html", len=len(users_list), users_list=users_list, user=g.user)


# Admin Dashboard
@app.route("/manageUsers", methods=["POST"])
def manageUsers():
    checkUser()
    if request.form["actionbutton"] == "blockUser":
        error = None

        userid = request.form["userid"]

        db = connectDb()
        db.execute("UPDATE users SET blocked=1 WHERE userID=?", (userid,))
        db.commit()
        return redirect(url_for("routeToDashboard", user=g.user))
    
    elif request.form["actionbutton"] == "unblockUser":
        userid = request.form["userid"]

        db = connectDb()
        db.execute("UPDATE users SET blocked=0 WHERE userID=?", (userid,))
        db.commit()
        return redirect(url_for("routeToDashboard", user=g.user))

    elif request.form["actionbutton"] == "setasAuthor":
        userid = request.form["userid"]

        db = connectDb()
        db.execute("UPDATE users SET role='author' WHERE userID=?", (userid,))
        db.commit()
        return redirect(url_for("routeToDashboard", user=g.user))

    elif request.form["actionbutton"] == "unsetasAuthor":
        userid = request.form["userid"]

        db = connectDb()
        db.execute("UPDATE users SET role='user' WHERE userID=?", (userid,))
        db.commit()
        return redirect(url_for("routeToDashboard", user=g.user))


# Comments CRUD
@app.route("/manageComments/<blog_id>", methods=["POST"])
def manageComments(blog_id):
    if request.form["actionbutton"] == "addCommentID":
        error = None
        
        comment = request.form["comment"]
        date = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")

        checkUser()

        db = connectDb()
        db.execute("INSERT INTO comments(userID, blogID, text, date) VALUES(?, ?, ?, ?)", (g.user[0], blog_id, comment, date))
        db.commit()

        return redirect(url_for("routeToViewBlog", blog_id=blog_id))


# Blog CRUD
@app.route("/manageBlogs", methods=["POST"])
def manageBlogs():
    if request.form["actionbutton"] == "addFormID":
        error = None

        title = request.form["title"]
        content = request.form["content"]
        date = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")

        checkUser()

        db = connectDb()
        db.execute("INSERT INTO blogs(userID, title, content, date) VALUES(?, ?, ?, ?)", (g.user[0], title, content, date))
        db.commit()

        return redirect(url_for("routeToProfile", user=g.user))

    elif request.form["actionbutton"] == "updateFormID":
        error = None

        blogid = request.form["blogid"]
        title = request.form["title"]
        content = request.form["content"]
        date = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")

        checkUser()

        db = connectDb()
        db.execute("UPDATE blogs SET userID=?, title=?, content=?, date=? WHERE blogID=?", (g.user[0], title, content, date, blogid))
        db.commit()

        return redirect(url_for("routeToProfile", user=g.user))

    elif request.form["actionbutton"] == "deleteFormID":
        error = None
        blogid = request.form["blogid"]

        db = connectDb()
        db.execute("DELETE FROM blogs WHERE blogID=?", (blogid))
        db.commit()

        return redirect(url_for("routeToProfile", user=g.user))
    

# User Authentication & Registration
#login
@app.route("/login", methods=["POST", "GET"])
def routeToLogin():
    if request.method == "POST":
        error = None

        username = request.form["username"]
        password = request.form["password"]

        db = connectDb()
        user = db.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()

        if user == None:
            error = "User doesn't exist! Please create an account to continue!"
            return redirect(url_for("routeToSignin")), render_template("user_auth/signin.html", error=error)
 
        elif password != user[5]:
            error = "Invalid Credentials!"
            return render_template("user_auth/login.html", error=error)
        
        elif user[7] == 1:
            error = "This account has been blocked!"
            return render_template("user_auth/login.html", error=error)

        else:
            session.clear()
            session["user_id"] = user[0]
            if user[6] == "admin":
                return redirect(url_for("routeToDashboard"))
            
            else:
                return redirect(url_for("routeToProfile"))
                    
    return render_template("user_auth/login.html")

#logout
@app.route("/logout")
def routeToLogout():
    session.clear()
    return redirect(url_for("routeToHome"))

#signin
@app.route("/signin", methods=["POST", "GET"])
def routeToSignin():
    if request.method == "POST":
        error = None

        username = request.form["username"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]

        db = connectDb()
        usernames_list = db.execute("SELECT username FROM users").fetchall()

        if username in usernames_list:
            error = "Username Taken! Please select another username."
            return render_template("user_auth/signin.html", error=error)
        
        else:
            db.execute("INSERT INTO users(username, firstname, lastname, email, password, role, blocked) VALUES(?, ?, ?, ?, ?, 'user', 0)", (username, firstname, lastname, email, password))
            db.commit()
            return redirect(url_for("routeToLogin"))
        
    return render_template("user_auth/signin.html")


if __name__ == "__main__":
    app.run(debug=True)