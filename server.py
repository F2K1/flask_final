from flask import Flask, render_template, redirect, url_for, request
import repository
from datetime import datetime


#session setup
app = Flask(__name__)
app.secret_key = 'jiejfirjeijrrcm4334qjdwx293r82ud2few2ed' #bad practice
app.config['SESSION_TYPE'] = 'filesystem'

#redirect to home page
@app.route("/")
def routeToHome(latest_blogs_list=None):
    latest_blogs_list = repository.getLatestBlogs(latest_blogs_list)
    isSession = repository.checkUser()
    return render_template("index.html", isSession=isSession, len=len(latest_blogs_list), latest_blogs_list=latest_blogs_list)

#redirect to user profile page
@app.route("/profile")
def routeToProfile(blogs_list=None):
    blogs_list = repository.getUsersBlogs(blogs_list)
    isSession = repository.checkUser()

    if blogs_list == None:
        return redirect(url_for("routeToLogin"))
    else:
        return render_template("profile.html", isSession=isSession, username=blogs_list[1], role=blogs_list[2], len=len(blogs_list[0]), blogs_list=blogs_list[0])

#redirect to individual blog page
@app.route("/view-blog/<blog_id>")
def routeToViewBlog(blog_id):
    blog_id = repository.getBlogDetails(blog_id)
    isSession = repository.checkUser()
    return render_template("view_blog.html", isSession=isSession, blog=blog_id[0], length=len(blog_id[1]), comments_list=blog_id[1])


#redirect to admin dashboard
@app.route("/dashboard")
def routeToDashboard():
    data = repository.getUsers()
    return render_template("dashboard.html", len=len(data[0]), users_list=data[0], user=data[1])

#admin dashboard
@app.route("/manageUsers", methods=["POST"])
def manageUsers():
    repository.checkUser()
    if request.form["actionbutton"] == "blockUser":
        userid = request.form["userid"]
        data = repository.blockUser(userid)
        return redirect(url_for("routeToDashboard", user=data))
    
    elif request.form["actionbutton"] == "unblockUser":
        userid = request.form["userid"]
        data = repository.unblockUser(userid)
        return redirect(url_for("routeToDashboard", user=data))

    elif request.form["actionbutton"] == "setasAuthor":
        userid = request.form["userid"]
        data = repository.setasAuthor(userid)
        return redirect(url_for("routeToDashboard", user=data))

    elif request.form["actionbutton"] == "unsetasAuthor":
        userid = request.form["userid"]
        data = repository.unsetasAuthor(userid)
        return redirect(url_for("routeToDashboard", user=data))


#user comment dashboard
@app.route("/manageComments/<blog_id>", methods=["POST"])
def manageComments(blog_id):
    repository.checkUser()
    if request.form["actionbutton"] == "addCommentID":        
        comment = request.form["comment"]
        date = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
        blog_id = repository.addComment(blog_id, comment, date)
        return redirect(url_for("routeToViewBlog", blog_id=blog_id))


#manage user blogs
@app.route("/manageBlogs", methods=["POST"])
def manageBlogs():
    repository.checkUser()
    if request.form["actionbutton"] == "addFormID":
        title = request.form["title"]
        content = request.form["content"]
        date = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
        data = repository.addBlog(title, content, date)
        return redirect(url_for("routeToProfile", user=data))

    elif request.form["actionbutton"] == "updateFormID":
        blogid = request.form["blogid"]
        title = request.form["title"]
        content = request.form["content"]
        date = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
        data = repository.updateBlog(blogid, title, content, date)
        return redirect(url_for("routeToProfile", user=data))

    elif request.form["actionbutton"] == "deleteFormID":
        blogid = request.form["blogid"]
        data = repository.deleteBlog(blogid)
        return redirect(url_for("routeToProfile", user=data))


#redirect to login page
@app.route("/login", methods=["POST", "GET"])
def routeToLogin():
    isSession = repository.checkUser()
    if request.method == "POST":
        error = None

        username = request.form["username"]
        password = request.form["password"]

        data = repository.login(error, username, password)

        if data[0] != None:
            return render_template("user_auth/login.html", isSession=isSession, error=data[0])
        elif data[1] == "admin":
            return redirect(url_for("routeToDashboard"))
        elif data[1] == "notadmin":
            return redirect(url_for("routeToProfile"))

    return render_template("user_auth/login.html", isSession=isSession)

#logout user
@app.route("/logout")
def routeToLogout():
    repository.logout()
    return redirect(url_for("routeToHome"))

#redirect to signin page 
@app.route("/signin", methods=["POST", "GET"])
def routeToSignin():
    isSession = repository.checkUser()
    if request.method == "POST":
        error = None

        username = request.form["username"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]

        data = repository.signin(error, username, firstname, lastname, email, password)
        if data[0] != None:
            render_template("user_auth/signin.html", isSession=isSession, error=data)
        else:
            redirect(url_for("routeToLogin"))
        
    return render_template("user_auth/signin.html", isSession=isSession)


if __name__ == "__main__":
    app.run(debug=True)