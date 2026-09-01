from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # Dynamically build file path matching the weather station code format
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"

    # Read the text file, ignoring metadata comments (first 20 rows)
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    # Extract the exact temperature matching the string date and convert to a native type
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10

    return {
        "station": station,
        "date": date,
        "temperature": int(temperature) / 10,
    }


if __name__ == "__main__":
    app.run(debug=True, port=5001)