import plotly.graph_objs as go
import plotly
import json, props
from collections import OrderedDict
from flaskapp import recommender
import csv

def return_plot(data, title):
    labels = list(data.keys())
    values = list(data.values())
    trace = go.Pie(labels=labels, values=values, hoverinfo='label+percent', textinfo='value', textfont=dict(size=12))
    data = [trace]
    layout = go.Layout(title=title, autosize=False,
    width=500,
    height=500,)
    fig = go.Figure(data=data, layout=layout)
    # Convert the figures to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    '''graphJSON = plotly.offline.plot(fig,
                                     config={"displayModeBar": False},
                                     show_link=False, include_plotlyjs=False,
                                     output_type='div')'''

    return graphJSON

def return_ordered_pie(data, title):
    data = OrderedDict(sorted(data.items(), key = lambda x : x[1], reverse=True))
    cats = 15
    labels = []
    values = []
    for key, val in data.items():
        if cats > 0:
            labels.append(key)
            values.append(val)
        cats -= 1
    trace = go.Pie(labels=labels, values=values, hoverinfo='label+percent', textinfo='value', textfont=dict(size=12))
    data = [trace]
    layout = go.Layout(title=title, autosize=False,
                       width=500,
                       height=500, )
    fig = go.Figure(data=data, layout=layout)
    # Convert the figures to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def get_dict(label, results):
    dt = dict()

    for user in results:
        for row in user:
            if row[label] not in dt:
                dt[row[label]] = 0
            dt[row[label]] += 1

    return dt

def get_course_tags():

    course_tags = recommender.get_tables(props.COURSE_TAGS_URI)
    course_tags.rename(index=str, columns={'0': 'course_id', '1': 'course_tags'}, inplace=True)
    c_dt = course_tags.set_index('course_id').to_dict()
    return c_dt

def get_view_dict(label, results, c_tags):

    dt = dict()

    for user in results:
        for row in user:
            if c_tags.get(row[label]) is not None:
                if c_tags.get(row[label]) not in dt:
                    dt[c_tags.get(row[label])] = 0
                dt[c_tags.get(row[label])] += 1
    return dt