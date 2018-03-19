from flask import Flask, render_template, request, send_file
import pandas
from geopy.geocoders import Nominatim

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=["POST"])
def success():
    global file
    if request.method == 'POST':
        file = request.files['file']
        file.filename = "Uploaded" + file.filename
        df = pandas.read_csv(file)

        row_name = ''
        if "Address" in df.columns:
            row_name = 'Address'
        elif "address" in df.columns:
            row_name = "address"

        if row_name != '':
            nom = Nominatim(scheme='http')
            df["Latitude"] = df[row_name].apply(nom.geocode).apply(lambda x: x.latitude if x != None else None)
            df["Longitude"] = df[row_name].apply(nom.geocode).apply(lambda x: x.longitude if x != None else None)
            df.to_csv(file.filename)
            return render_template("index.html",
                                   tables=["view.html", df.to_html(escape=False)],
                                   btn="download.html")
        else:
            return render_template("index.html", text="Please make sure you have an address column in your csv file!")


@app.route("/download")
def download():
    return send_file(file.filename, attachment_filename="yourfile.csv", as_attachment=True)


if __name__ == "__main__":
    app.debug = True
    app.run()
