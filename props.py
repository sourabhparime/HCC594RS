# properities file

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/recosys'
DB_TYPE = 'mysql'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
TEMP_UPLOAD = 'temp'
USER_VIEWS = 'data/user_course_views.csv'
USER_INTERESTS = 'data/user_interests.csv'
USER_ASSES = 'data/user_assessment_scores.csv'
COURSE_TAGS = 'data/course_tags.csv'
USER_VIEWS_URI = SQLALCHEMY_DATABASE_URI + '::' + USER_VIEWS.split('/')[-1][:-4]
USER_ASSES_URI = SQLALCHEMY_DATABASE_URI + '::' + USER_ASSES.split('/')[-1][:-4]
USER_INTERESTS_URI = SQLALCHEMY_DATABASE_URI + '::' + USER_INTERESTS.split('/')[-1][:-4]
COURSE_TAGS_URI = SQLALCHEMY_DATABASE_URI + '::' + COURSE_TAGS.split('/')[-1][:-4]
SIMILARITY = "data/similar_users.csv"
SIMILARITY_URI = SQLALCHEMY_DATABASE_URI + '::' + SIMILARITY.split('/')[-1][:-4]
