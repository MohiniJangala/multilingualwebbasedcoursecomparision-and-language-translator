from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import webbrowser
app = Flask(__name__)
#  LOAD DATA 
df = pd.read_csv("dataset.csv")
#  ANALYSIS 
def analyze_course(df, course):
    filtered = df[df["course_name"].str.lower() == course.lower()].copy()
    if filtered.empty:
        return None, None, None
    # Depth %
    filtered["depth_percentage"] = (
        filtered["content_depth_score"] /
        filtered["content_depth_score"].max()
    ) * 100
    # Popularity
    filtered["popularity"] = filtered["enrolled"] + filtered["num_reviews"]
    # Overall Score
    filtered["overall_score"] = (
        filtered["rating"] * 0.4 +
        filtered["content_depth_score"] * 0.4 +
        filtered["explanation_quality_score"] * 0.2
    )
    # Best Platforms
    best_student = filtered.sort_values(by="rating", ascending=False).iloc[0]["platform"]
    best_professor = filtered.sort_values(by="content_depth_score", ascending=False).iloc[0]["platform"]
    return filtered, best_student, best_professor
#  CHARTS 
def generate_charts(filtered, course):
    plt.figure()
    filtered.plot(x="platform", y="rating", kind="bar")
    plt.title(f"{course} - Rating")
    plt.savefig("static/rating.png")
    plt.close()
    plt.figure()
    filtered.set_index("platform")["popularity"].plot(kind="pie", autopct="%1.1f%%")
    plt.title(f"{course} - Popularity")
    plt.savefig("static/popularity.png")
    plt.close()
    plt.figure()
    filtered.plot(x="platform", y="depth_percentage", kind="bar")
    plt.title(f"{course} - Depth %")
    plt.savefig("static/depth.png")
    plt.close()
    plt.figure()
    filtered.plot(x="platform", y="overall_score", kind="bar")
    plt.title(f"{course} - Score")
    plt.savefig("static/score.png")
    plt.close()
#  COURSE LINKS
def get_course_link(platform, course):
    course = course.lower()
    links = {
        "python": {
            "Udemy": "https://www.udemy.com/topic/python/",
            "Coursera": "https://www.coursera.org/courses?query=python",
            "NPTEL": "https://onlinecourses.nptel.ac.in/",
            "GeeksforGeeks": "https://www.geeksforgeeks.org/python-programming-language/",
            "W3Schools": "https://www.w3schools.com/python/",
            "Class Central": "https://www.classcentral.com/subject/python"
        },

        "c": {
            "Udemy": "https://www.udemy.com/topic/c-programming/",
            "NPTEL": "https://onlinecourses.nptel.ac.in/",
            "GeeksforGeeks": "https://www.geeksforgeeks.org/c-programming-language/",
            "W3Schools": "https://www.w3schools.com/c/"
        },

        "c++": {
            "Udemy": "https://www.udemy.com/topic/c-plus-plus/",
            "Coursera": "https://www.coursera.org/search?query=c%2B%2B",
            "GeeksforGeeks": "https://www.geeksforgeeks.org/c-plus-plus/",
            "W3Schools": "https://www.w3schools.com/cpp/"
        },

        "java": {
            "Udemy": "https://www.udemy.com/topic/java/",
            "Coursera": "https://www.coursera.org/search?query=java",
            "GeeksforGeeks": "https://www.geeksforgeeks.org/java/",
            "NPTEL": "https://onlinecourses.nptel.ac.in/"
        },

        "html": {
            "W3Schools": "https://www.w3schools.com/html/",
            "GeeksforGeeks": "https://www.geeksforgeeks.org/html/",
            "Udemy": "https://www.udemy.com/topic/html/"
        },

        "css": {
            "W3Schools": "https://www.w3schools.com/css/",
            "Udemy": "https://www.udemy.com/topic/css/"
        },

        "javascript": {
            "W3Schools": "https://www.w3schools.com/js/",
            "GeeksforGeeks": "https://www.geeksforgeeks.org/javascript/",
            "Udemy": "https://www.udemy.com/topic/javascript/",
            "Coursera": "https://www.coursera.org/search?query=javascript"
        },

        "dsa": {
            "GeeksforGeeks": "https://www.geeksforgeeks.org/data-structures/",
            "Udemy": "https://www.udemy.com/topic/data-structures/",
            "Coursera": "https://www.coursera.org/search?query=data%20structures"
        },

        "data science": {
            "Coursera": "https://www.coursera.org/browse/data-science",
            "Udemy": "https://www.udemy.com/topic/data-science/",
            "NPTEL": "https://onlinecourses.nptel.ac.in/"
        },

        "data analytics": {
            "Coursera": "https://www.coursera.org/search?query=data%20analytics",
            "Udemy": "https://www.udemy.com/topic/data-analysis/"
        },

        "dbms": {
            "GeeksforGeeks": "https://www.geeksforgeeks.org/dbms/",
            "Udemy": "https://www.udemy.com/topic/database-management/",
            "NPTEL": "https://onlinecourses.nptel.ac.in/"
        }
    }

    return links.get(course, {}).get(platform, "#")
#  ROUTES 
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/dashboard")
def dashboard():
     return render_template("dashboard.html")
@app.route("/search", methods=["POST"])
def search():
    course = request.form["course"]
    filtered, best_student, best_professor = analyze_course(df, course)
    if filtered is None:
        return "No data found"
    generate_charts(filtered, course)
    # Get links
    student_link = get_course_link(best_student, course)
    professor_link = get_course_link(best_professor, course)
    return render_template(
        "result.html",
        tables=filtered.to_dict(orient="records"),
        best_student=best_student,
        best_professor=best_professor,
        course=course,
        student_link=student_link,
        professor_link=professor_link
    )
# RUN
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/dashboard")
    app.run(debug=True,port=5000)
    
    