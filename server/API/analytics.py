from sample import *
import operator,json
@app.route('/analytics/user',methods=['GET'])
# @auth.login_required
def time_spent():
	user = g.user.username
	sites = Visited_logs.query.all()
	frequency = {}
	timetot = {}
	for i in sites:
		if i.userid == user
			if i.host in frequency:
				frequency[i.host]+=1
			else:
				frequency[i.host]=1
			if i.host in timetot:
				timetot[i.host]+ = i.time_spent
			else:
				timetot[i.host] = i.time_spent 
	frequency = sorted(frequency.items(), key=operator.itemgetter(1))[::-1]
	frequency = dict(frequency)
	timetot = sorted(timetot.items(), key=operator.itemgetter(1))[::-1]
	timetot = dict(timetot)
	return jsonify({'frequency':frequency,'time_dist':timetot}),201


