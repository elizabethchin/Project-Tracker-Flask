"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get("github")

    first, last, github = hackbright.get_student_by_github(github)

    title = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            title=title)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/add_student")
def add_student():
    """Displays a form to add student."""
    #this allows you to add student in the html file
    #which links you to "/student-add"
    #this info is inserted to "/student-add" function

    return render_template("student_add.html")

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first = request.form.get("first_name")#must match html form
    last = request.form.get("last_name")
    github = request.form.get("github")
    #uses function that adds student to DB
    hackbright.make_new_student(first, last, github)

    #shows page of student info, can really return to any page you want
    return redirect("/student?github=" + github)

@app.route("/project")
def projet_info():
    """Show information about a project."""

    title = request.args.get("title")

    project_info = hackbright.get_project_by_title(title)

    print(project_info)
    html = render_template("project_info.html",
                            title = title,
                            description=project_info[1],
                            max_grade=project_info[2])

    return html


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
