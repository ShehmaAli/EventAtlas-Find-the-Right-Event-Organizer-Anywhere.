# Flask: This is a web framework for Python that allows you to build web applications easily.
# render_template: This function is used to render HTML templates.
# request: This object is used to handle incoming requests to the Flask application.
# jsonify: This function converts Python dictionaries into JSON format, which is useful for API responses.
from flask import Flask, render_template, request, jsonify
import csv

# This line creates an instance of the Flask class.
# The __name__ variable is passed to the Flask constructor to help it determine the root path of the application.
app = Flask(__name__)


# Backend function to get event organizers

# get_event_organizers: This function takes two parameters: country and event.
# It initializes an empty list called organizers to store the results.
def get_event_organizers(country, event):
    organizers = []
    file_name = "pakistan.csv" if country == "pakistan" else "America.csv"
    try:
        with open(file_name, "r") as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            for row in reader:
                if row.get(event) == "Yes":
                    organizers.append({
                        "name": row["Company Name"],
                        "location": row["Location"],
                        "email": row["Email"]
                    })
    except FileNotFoundError:
        return []
    return organizers


# Route for the homepage
@app.route("/")
def home():
    return render_template("home.html")


# Route for the event form
@app.route("/event-form")
def event_form():
    return render_template("index.html")


# Route for the about page
@app.route("/about")
def about():
    return render_template("about.html")


# Route for the contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Route to handle form submission
@app.route("/get-organizers", methods=["POST"])
def get_organizers():
    data = request.json
    country = data.get("country")
    event = data.get("event")

    if not country or not event:
        return jsonify({"error": "Please select both country and event type."}), 400

    organizers = get_event_organizers(country, event)
    return jsonify(organizers)


if __name__ == "__main__":
    app.run(debug=True)