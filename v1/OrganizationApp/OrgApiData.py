import pymongo
from pprint import pprint
from django.http import HttpResponse
from datetime import datetime
import MySQLdb
from organization_dashboard_api.v1.dbv import *
sql_user = MYSQL_USER
sql_pswd = MYSQL_PSWD
sql_db = MYSQL_DB
mongodb = MONGO_DB
mysqlFlag = False
mongoFlag = False
db_mysql = None
mongo_client = None
def connect():
    try:
        global db_mysql
        db_mysql = MySQLdb.connect(user=sql_user, passwd=sql_pswd, db=sql_db)  # Establishing MySQL connection
        global mysqlFlag
        mysqlFlag = True
    except:
        print "MySQL connection not established"
        return HttpResponse("Mysql connection not established")

    try:
        global mongo_client
        mongo_client = pymongo.MongoClient()  # Establishing MongoDB connection
        global mongoFlag
        mongoFlag = True
    except:
        print "MongoDB connection not established"
        return HttpResponse("MongoDB connection not established")  # MongoDB could not be connected
def disconnect():

    try:
        db_mysql.close()
        mongo_client.close()
    except:
        None

""" Description: Function to Get grading policy of a Course
    Input Parameters:
            CourseDefinition  
    Output Type: JSON of Course Grading Policy
    Author: Dhruv Thakker
    Date of Creation: 21 June 2017
"""
def get_grading_policy(course_defination_id):


    connect()

    db_mongo = mongo_client[mongodb]
    mongo_cursor = db_mongo.modulestore.definitions.find({'_id': course_defination_id})
    course_definition = mongo_cursor[0]
    grading_policy = {}
    try:
        grade_list = course_definition['fields']['grading_policy']['GRADER']
        grader_result_list = []

        for j in range(len(grade_list)):
            grader_result_dict = {}
            min_count = grade_list[j]['min_count']
            drop_count = grade_list[j]['drop_count']
            short_label = grade_list[j]['short_label']
            display_name = grade_list[j]['type']
            weight = grade_list[j]['weight']
            grader_result_dict["min_count"] = min_count
            grader_result_dict["drop_count"] = drop_count
            grader_result_dict["short_label"] = str(short_label)
            grader_result_dict["type"] = str(display_name)
            grader_result_dict["weight"] = weight
            grader_result_list.append(grader_result_dict)
        grading_policy["grader"] = grader_result_list
        try:
            grade_cutoffs = course_definition['fields']['grading_policy']['GRADE_CUTOFFS']
            grading_policy["grade_cutoffs"] = grade_cutoffs
        except:
            grading_policy["grade_cutoffs"] = {}
            # print "No grade cutoffs mentioned"
    except:
        grading_policy["grade_cutoffs"] = {}
        grading_policy["grader"] = []

    disconnect()

    return grading_policy
        # print "No grading policy found"


def get_course_summary(course_name,course_run,course_org,details = False):

    connect()

    db_mongo = mongo_client[mongodb]
    mongo_cursor = db_mongo.modulestore.active_versions.find({"course": course_name, "run": course_run,
                                                              "org": course_org})
    mysql_cursor = db_mysql.cursor()
    course_team_query = "SELECT user_id,role FROM student_courseaccessrole where course_id = %s"
    course_staff_detail_query = "SELECT username,email FROM auth_user where id = %s"

    course_student_count_query = "select COUNT(user_id) from student_courseenrollment where binary course_id = %s"

    course_course = mongo_cursor[0]
    try:
        published_version = course_course['versions']['published-branch']
    except:
        return None

    mongo_cursor = db_mongo.modulestore.structures.find({'_id': published_version})

    course_structures = mongo_cursor[0]['blocks']

    for block in course_structures:
        if block['block_type'] == 'course':
            course_block = block
    try:
        course_start = course_block['fields']['start']
    except:
        course_start = None
    try:
        course_end = course_block['fields']['end']
    except:
        course_end = None

    try:
        course_registration_start = course_block['fields']['enrollment_start']
    except:
        course_registration_start = None

    try:
        course_registration_end = course_block['fields']['enrollment_end']
    except:
        course_registration_end = None

    try:
        course_organization = course_course['org']
    except:
        course_organization = None

    try:
        course_id = course_course['course']
    except:
        course_id = None

    try:
        course_run = course_course['run']
    except:
        course_run = None

    try:
        course_display_name = course_block['fields']['display_name']
    except:
        course_display_name = None
    course_id = "course-v1:" + course_organization + "+" + course_id + "+" + course_run

    try :  #<-Last Edit
        mysql_cursor.execute(course_student_count_query, (str(course_id),))
        course_student_count = mysql_cursor.fetchall()[0][0]
    except:
        course_student_count = None


    if course_start != None and course_end != None:
        if course_start > datetime.now():
            course_status = "upcoming"
        else:
            if course_end < datetime.now():
                course_status = "archived"
            else:
                course_status = "ongoing"
    else:
        course_status = "undefined"

    mysql_cursor.execute(course_team_query, (str(course_id),))
    course_team_list = mysql_cursor.fetchall()
    course_team = {}
    course_team['course_instructors'] = []
    course_staffs = []
    for item in course_team_list:
        mysql_cursor.execute(course_staff_detail_query, (item[0],))
        course_staff_detail = mysql_cursor.fetchall()[0]
        mcourse_staff_detail = {}
        mcourse_staff_detail['username'] = course_staff_detail[0]
        mcourse_staff_detail['email'] = course_staff_detail[1]
        if item[1] == 'instructor':
            course_team["course_instructors"].append(mcourse_staff_detail)
        else:
            course_staffs.append(mcourse_staff_detail)
    course_team["course_members"] = course_staffs


    course_details = {}
    course_details["course_start"] = course_start;
    course_details["course_end"] = course_end;
    course_details["course_registration_start"] = course_registration_start;
    course_details["course_registration_end"] = course_registration_end;
    course_details["course_id"] = course_id;
    course_details["course_display_name"] = course_display_name;
    course_details["course_status"] = course_status;
    course_details["course_team"] = course_team
    course_details["course_student_count"] = course_student_count #<- Last Edit

    if details :
        ## Getting Grading Policy
        definition_id = course_block['definition']
        grading_policy = get_grading_policy(definition_id)
        course_details["course_grading_policy"] = grading_policy

    disconnect()

    return course_details


def get_courses_with_organization(org,details=False):

    connect()

    course_list = []
    courses_with_org = {}
    courses_with_org['organization_name'] = org
    courses_with_org['organization_course_list'] =[]
    db_mongo = mongo_client[mongodb]
    mongo_cursor = db_mongo.modulestore.active_versions.find({'org':org})
    for course_course in mongo_cursor:

        try:
            course_org = course_course['org']
        except:
            course_org = None

        try:
            course_name = course_course['course']
        except:
            course_name = None

        try:
            course_run = course_course['run']
        except:
            course_run = None

        course_summary = get_course_summary(course_name,course_run,course_org,details)
        if course_summary == None:
            continue
        courses_with_org['organization_course_list'].append(course_summary)
    course_list.append(courses_with_org)

    disconnect()

    return course_list


def get_all_courses_with_org(details = False):

    connect()

    query = "select distinct(display_org_with_default) from course_overviews_courseoverview"

    mysql_cursor = db_mysql.cursor()
    mysql_cursor.execute(query)
    organizations = mysql_cursor.fetchall()

    list = []

    for organization in organizations:
        list.append(get_courses_with_organization(organization[0],details)[0])

    disconnect()

    return list
