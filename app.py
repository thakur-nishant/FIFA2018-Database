from flask import Flask, render_template, request, jsonify
import MySQLdb

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="root", db="fifa")

if conn:
    print("DB connection successful!")
else:
    print("Failed to connect MySQL Server!")

cursor = conn.cursor()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/getPlayers', methods=['POST'])
def getPlayers():
    if request.method == "POST":
        CName = request.form['CName']
        sql = "SELECT PName, PNo, Position FROM PLAYER WHERE LOWER(Team) = '{}';".format(CName.lower())
        print(sql, CName)
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        ret = []
        for row in results:
            ret.append(row)

        return jsonify({"result": ret})


@app.route('/getResults', methods=['POST'])
def getResults():
    if request.method == "POST":
        GType = request.form['GType']
        sql = "SELECT T1.Team, G.Team1_Score, T2.Team, G.Team2_Score FROM GAME as G, Team as T1, Team as T2 WHERE T1.TeamID = G.TeamID1 and T2.TeamID = G.TeamID2 and LOWER(G.MatchType) = '{}';".format(
            GType.lower())
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        ret = []
        for row in results:
            ret.append(row)

        return jsonify({"result": ret})


if __name__ == "__main__":
    app.run()
