import numpy as np
import pandas as pd
import props
from odo import odo
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.exc import DatabaseError
from collections import OrderedDict

user_views = None
course_tags = None


def dump_tables(uri, filename):
    try:
        odo(filename, uri)
        return True
    except IOError:
        raise Exception("File specified not found")


def get_tables(uri):
    try:
        data = odo(uri, pd.DataFrame)
        return data

    except DatabaseError:
        raise Exception("Table not retrieved or connection issues")


def create_table():
    global user_views
    global course_tags
    user_views = get_tables(props.USER_VIEWS_URI)
    course_tags = get_tables(props.COURSE_TAGS_URI)


def min_max_scale(df, index_col):
    copy = df.copy()
    users = copy.pop(index_col)
    copy.index = users
    scaled = (copy - copy.min()) / (copy.max() - copy.min())
    scaled.reset_index(inplace=True)
    return scaled


def check_and_fill_zero(df):
    if df.isnull().values.any():
        df.fillna(0, inplace=True)
    return df


def get_similarity_matrix(df, index_col):
    copy = df.copy()
    users = copy.pop(index_col)
    copy.index = users
    arr = copy.values

    if arr.shape[0] == df.shape[0]:  # sanity check
        arr_sparse = sparse.csr_matrix(arr)
        similarities = cosine_similarity(arr_sparse)
        sim_df = pd.DataFrame(similarities, columns=[i for i in range(1, arr.shape[0] + 1)])
        sim_df.reset_index(inplace=True)
        sim_df['index'] = sim_df['index'] + 1
        sim_df.rename(index=str, columns={'index': 'user_handle'}, inplace=True)
        return sim_df
    return False


def save_10_most_similar_users(df, count=10, user_count=8760):
    similar_users = pd.DataFrame(columns=['user_handle'] + ["similar_" + str(i) for i in range(1, count + 1)])
    row_list = []
    users = list(df.user_handle)
    for user in users:
        dt = df[df['user_handle'] == user].to_dict(orient='records')
        dt = dt[0]
        dt = OrderedDict(sorted(dt.items(), key=lambda x: x[1], reverse=True))
        # print(dt)
        row = dict()
        row['user_handle'] = int(dt['user_handle'])
        del dt['user_handle']
        i = 0
        for key, val in dt.items():
            if i >= 11: break
            row["similar_" + str(i)] = int(key)
            i += 1
        # print(row)
        row_list.append(row)
    app = pd.DataFrame(row_list)
    similar_users = pd.concat([similar_users, app])
    similar_users.to_csv("data/similar_users.csv",index=False)

    return True


def create_recommender_matrix():
    file_path = ''

    create_table()
    check_and_fill_zero(user_views)
    check_and_fill_zero(course_tags)
    course_tags.rename(index=str, columns={'0': 'course_id', '1': 'course_tags'}, inplace=True)

    unique_users = sorted(user_views.user_handle.unique())
    unique_tags = course_tags.course_tags.unique()
    unique_levels = user_views.level.unique()

    acc_df = pd.DataFrame(columns=["user_handle"] + list(unique_tags) + list(unique_levels))
    keys_list = acc_df.columns

    user_course = pd.merge(user_views, course_tags, how='left', on='course_id')

    rows_list = []
    for user in unique_users:
        user_df = user_course[user_course['user_handle'] == user]
        by_tags = user_df['course_tags'].value_counts().to_dict()
        by_view_time = user_df['view_time_seconds'].mean() / 60
        by_level = user_df['level'].value_counts().to_dict()
        row = OrderedDict.fromkeys(keys_list)
        row['user_handle'] = user
        row['view_time_seconds'] = by_view_time
        # loop and add vals

        for key, val in by_tags.items():
            row[key] = val

        for key, val in by_level.items():
            row[key] = val

        rows_list.append(row)

    app = pd.DataFrame(rows_list)
    acc_df = pd.concat([acc_df, app], sort=True)
    check_and_fill_zero(acc_df)
    scaled = min_max_scale(acc_df, 'user_handle')
    check_and_fill_zero(scaled)
    sim_df = get_similarity_matrix(scaled, 'user_handle')

    save_10_most_similar_users(sim_df)

    return True
