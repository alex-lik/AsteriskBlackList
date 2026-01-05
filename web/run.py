from flask import Flask, request, render_template, redirect
import db
app = Flask(__name__)



# @app.route("/")
# def modem_state():
# 	result = os.popen("asterisk -rx 'dongle show devices'").read()
# 	data = []
# 	for line in result.splitlines():
# 		line = line.split()
# 		trunk = line[0]
# 		group = line[1]
# 		if trunk == 'ID': continue
# 		state = line[2] if line[2] != 'Not' else 'Not connect'
# 		rssi = line[3] if re.search('\d+', line[3]) else line[4]
# 		operator = line[6] if not re.search('\d+', line[6]) else line[7]
# 		dongle_model = line[7] if line[7] != 'UA' else line[8]
# 		phone = line[-1]
# 		data.append((trunk, state, rssi, operator, dongle_model, phone))
# 	return render_template('index.html', data=data)



@app.route("/blacklist", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def black_list():
	message = None
	if request.method == 'POST':
		phone = request.form.get("phone")
		comment = request.form.get("comment")
		comment = comment.replace(' ', '_')
		success, message, normalized = db.add_phone(phone, comment)

	black_list = db.get_blacklist()

	return render_template('blacklist.html', black_list=black_list, message=message)


@app.route('/delete/<phone>')
def delete(phone):
	db.del_phone(phone)
	print(f"""Number {phone} removed from the black list""")        # Выводим сообщение на экран
	return redirect('/blacklist')

 
 
@app.route("/incoming_sms")
def incoming_sms():
	return render_template('incomingsms.html')
 

@app.route("/balance")
def sim_balance():
	return render_template('balance.html')
 

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True, port=81)
