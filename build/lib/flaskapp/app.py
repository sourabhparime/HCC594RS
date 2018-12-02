from flaskapp import db
from flask import Flask, g, render_template, request, session, redirect, url_for
from flask import Flask, render_template, url_for
from flaskapp import graph_helper
import json, sys
from werkzeug.routing import Rule
from flaskapp import create_app
from flask import Markup

app = create_app()
# url-maps
app.url_map.add(Rule('/', endpoint='hello', methods=['POST', 'GET']))
#app.url_map.add(Rule('/reco', endpoint='reco', methods=['POST', 'GET']))


@app.endpoint('hello')
def hello():
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        user_id = form_dict['user_handle']
        user_id = int(user_id)

        if user_id < 1 or user_id > 8760:  # hard coded for now can be set from g later
            print("Enter a valid number between 1 and 8760", file=sys.stdout)
            render_template('hello.html')
        result = db.get_similar(user_id)
        user_interests = []
        user_views = []
        user_levels = []
        for row in result:
            for user in row:
                user = int(user)
                print(user)
                user_interests.append(db.get_int(user))
                user_levels.append(db.get_levels(user))
                user_views.append(db.get_views(user))

        c_tags = graph_helper.get_course_tags()
        c_tags = c_tags['course_tags']


        dt_lvl = graph_helper.get_dict('level', user_levels)
        dt_int = graph_helper.get_dict('interest_tag', user_interests)
        dt_view = graph_helper.get_view_dict('course_id', user_views, c_tags)

        level = graph_helper.return_plot(dt_lvl, "Similar users by Level")
        inte = graph_helper.return_ordered_pie(dt_int, "Similar users by Interests")
        views = graph_helper.return_ordered_pie(dt_view, "Users similar to you viewed courses from the categories")

        return render_template("dashboard.html", lgraph=level, igraph=inte, vgraph = views)

    return render_template('hello.html')

if __name__ == "__main__":
    app.run()