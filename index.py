from server_app import app

f = open("file.txt", "a")
f.write('EVALUATE FILE')
f.close()

app.run(debug=False)