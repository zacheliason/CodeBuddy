from content import *
import contextvars
from datetime import datetime
import glob
from helper import *
import html
import io
import json
import logging
import os
import re
import sys
from tornado.auth import GoogleOAuth2Mixin
import tornado.ioloop
from tornado.log import enable_pretty_logging
from tornado.log import LogFormatter
from tornado.options import options
from tornado.options import parse_command_line
from tornado.web import *
import traceback
from urllib.parse import urlencode
import urllib.request
import uuid
import sqlite3
from sqlite3 import Error
import zipfile
from Handlers import *
# from Handlers import AddInstructorHandler
# from Handlers.AssignmentHandler import *
# from Handlers.BackEndHandler import *
# from Handlers.BaseUserHandler import *
# from Handlers.CheckPartnersHandler import *
# from Handlers.CopyAssignmentHandler import *
# from Handlers.CourseHandler import *
# from Handlers.CreateVideoExerciseHandler import *
# from Handlers.DeleteAssignmentHandler import *
# from Handlers.DeleteAssignmentSubmissionsHandler import *
# from Handlers.DeleteCourseHandler import *
# from Handlers.DeleteCourseSubmissionsHandler import *
# from Handlers.DeleteExerciseHandler import *
# from Handlers.DeleteExerciseSubmissionsHandler import *
# from Handlers.DeleteHelpRequestHandler import *
# from Handlers.DevelopmentLoginHandler import *
# from Handlers.DownloadAllScoresHandler import *
# from Handlers.DownloadFileHandler import *
# from Handlers.DownloadScoresHandler import *
# from Handlers.EditAssignmentHandler import *
# from Handlers.EditCourseHandler import *
# from Handlers.EditScoresHandler import *
# from Handlers.EditExerciseHandler import *
# from Handlers.ExerciseHandler import *
# from Handlers.ExerciseScoresHandler import *
# from Handlers.ExerciseSubmissionsHandler import *
# from Handlers.ExportCourseHandler import *
# from Handlers.ExportSubmissionsHandler import *
# from Handlers.GetPresubmissionHandler import *
# from Handlers.GetSubmissionHandler import *
# from Handlers.GetSubmissionsHandler import *
# from Handlers.GoogleLoginHandler import *
# from Handlers.HelpRequestsHandler import *
# from Handlers.HomeHandler import *
# from Handlers.ImportCourseHandler import *
# from Handlers.LoggingFilter import *
# from Handlers.LogoutHandler import *
# from Handlers.MoveExerciseHandler import *
# from Handlers.ProfileAdminHandler import *
# from Handlers.ProfileCoursesHandler import *
# from Handlers.ProfileHelpRequestsHandler import *
# from Handlers.ProfileInstructorHandler import *
# from Handlers.ProfileManageUsersHandler import *
# from Handlers.ProfilePersonalInfoHandler import *
# from Handlers.ProfilePreferencesHandler import *
# from Handlers.ProfileSelectCourseHandler import *
# from Handlers.ProfileStudentHelpRequestsHandler import *
# from Handlers.RemoveAdminHandler import *
# from Handlers.RemoveAssistantHandler import *
# from Handlers.RemoveInstructorHandler import *
# from Handlers.ResetTimerHandler import *
# from Handlers.RunCodeHandler import *
# from Handlers.SavePresubmissionHandler import *
# from Handlers.StaticFileHandler import *
# from Handlers.StudentExerciseHandler import *
# from Handlers.StudentScoresHandler import *
# from Handlers.SubmitHandler import *
# from Handlers.SubmitHelpRequestHandler import *
# from Handlers.SummarizeLogsHandler import *
# from Handlers.TestHandler import *
# from Handlers.UnregisterHandler import *
# from Handlers.ViewAnswerHandler import *
# from Handlers.ViewHelpRequestsHandler import *
# from Handlers.ViewScoresHandler import *
# sys.path.append()

def make_app():
    app = Application([
        url(r"/", HomeHandler),
        url(r"\/profile\/courses\/([^\/]+)", ProfileCoursesHandler, name="profile_courses"),
        url(r"\/profile\/personal_info\/([^\/]+)", ProfilePersonalInfoHandler, name="profile_personal_info"),
        url(r"\/profile\/admin\/([^\/]+)", ProfileAdminHandler, name="profile_admin"),
        url(r"\/profile\/instructor\/course\/([^\/]+)", ProfileSelectCourseHandler, name="profile_select_course"),
        url(r"\/profile\/instructor\/([^\/]+)\/([^\/]+)", ProfileInstructorHandler, name="profile_instructor"),
        url(r"\/profile\/manage_users", ProfileManageUsersHandler, name="profile_manage_users"),
        url(r"\/profile\/help_requests", ProfileHelpRequestsHandler, name="profile_help_requests"),
        url(r"\/profile\/student_help_requests", ProfileStudentHelpRequestsHandler, name="profile_student_help_requests"),
        url(r"\/profile\/preferences\/([^\/]+)", ProfilePreferencesHandler, name="profile_preferences"),
        url(r"\/unregister\/([^\/]+)\/([^\/]+)", UnregisterHandler, name="unregister"),
        url(r"\/course\/([^\/]+)", CourseHandler, name="course"),
        url(r"\/edit_course\/([^\/]+)?", EditCourseHandler, name="edit_course"),
        url(r"\/delete_course\/([^\/]+)?", DeleteCourseHandler, name="delete_course"),
        url(r"\/delete_course_submissions\/([^\/]+)?", DeleteCourseSubmissionsHandler, name="delete_course_submissions"),
        url(r"\/import_course", ImportCourseHandler, name="import_course"),
        url(r"\/export_course\/([^\/]+)?", ExportCourseHandler, name="export_course"),
        url(r"\/export_submissions\/([^\/]+)?", ExportSubmissionsHandler, name="export_submissions"),
        url(r"\/assignment\/([^\/]+)\/([^\/]+)", AssignmentHandler, name="assignment"),
        url(r"\/edit_assignment\/([^\/]+)\/([^\/]+)?", EditAssignmentHandler, name="edit_assignment"),
        url(r"\/copy_assignment\/([^\/]+)\/([^\/]+)?", CopyAssignmentHandler, name="copy_assignment"),
        url(r"\/delete_assignment\/([^\/]+)\/([^\/]+)?", DeleteAssignmentHandler, name="delete_assignment"),
        url(r"\/delete_assignment_submissions\/([^\/]+)\/([^\/]+)?", DeleteAssignmentSubmissionsHandler, name="delete_assignment_submissions"),
        url(r"\/exercise\/([^\/]+)\/([^\/]+)/([^\/]+)", ExerciseHandler, name="exercise"),
        url(r"\/edit_exercise\/([^\/]+)\/([^\/]+)/([^\/]+)?", EditExerciseHandler, name="edit_exercise"),
        url(r"\/create_video_exercise\/([^\/]+)\/([^\/]+)", CreateVideoExerciseHandler, name="create_video_exercise"),
        url(r"\/move_exercise\/([^\/]+)\/([^\/]+)/([^\/]+)?", MoveExerciseHandler, name="move_exercise"),
        url(r"\/delete_exercise\/([^\/]+)\/([^\/]+)/([^\/]+)?", DeleteExerciseHandler, name="delete_exercise"),
        url(r"\/delete_exercise_submissions\/([^\/]+)\/([^\/]+)/([^\/]+)?", DeleteExerciseSubmissionsHandler, name="delete_exercise_submissions"),
        url(r"\/run_code\/([^\/]+)\/([^\/]+)/([^\/]+)", RunCodeHandler, name="run_code"),
        url(r"\/submit\/([^\/]+)\/([^\/]+)/([^\/]+)", SubmitHandler, name="submit"),
        url(r"\/get_submission\/([^\/]+)\/([^\/]+)/([^\/]+)/([^\/]+)/(\d+)", GetSubmissionHandler, name="get_submission"),
        url(r"\/get_submissions\/([^\/]+)\/([^\/]+)/([^\/]+)/([^\/]+)", GetSubmissionsHandler, name="get_submissions"),
        url(r"\/save_presubmission\/([^\/]+)\/([^\/]+)/([^\/]+)", SavePresubmissionHandler, name="save_presubmission"),
        url(r"\/get_presubmission\/([^\/]+)\/([^\/]+)/([^\/]+)/([^\/]+)", GetPresubmissionHandler, name="get_presubmission"),
        url(r"\/check_partners\/([^\/]+)", CheckPartnersHandler, name="check_partners"),
        url(r"\/view_answer\/([^\/]+)\/([^\/]+)/([^\/]+)", ViewAnswerHandler, name="view_answer"),
        url(r"\/add_instructor\/([^\/]+)", AddInstructorHandler, name="add_instructor"),
        url(r"\/remove_admin\/([^\/]+)", RemoveAdminHandler, name="remove_admin"),
        url(r"\/remove_instructor\/([^\/]+)\/([^\/]+)", RemoveInstructorHandler, name="remove_instructor"),
        url(r"\/remove_assistant\/([^\/]+)\/([^\/]+)", RemoveAssistantHandler, name="remove_assistant"),
        url(r"\/reset_timer\/([^\/]+)\/([^\/]+)\/([^\/]+)", ResetTimerHandler, name="reset_timer"),
        url(r"\/view_scores\/([^\/]+)\/([^\/]+)", ViewScoresHandler, name="view_scores"),
        url(r"\/download_file\/([^\/]+)\/([^\/]+)/([^\/]+)/([^\/]+)", DownloadFileHandler, name="download_file"),
        url(r"\/download_scores\/([^\/]+)\/([^\/]+)", DownloadScoresHandler, name="download_scores"),
        url(r"\/download_all_scores\/([^\/]+)", DownloadAllScoresHandler, name="download_all_scores"),
        url(r"\/edit_scores\/([^\/]+)\/([^\/]+)\/([^\/]+)", EditScoresHandler, name="edit_scores"),
        url(r"\/student_scores\/([^\/]+)\/([^\/]+)\/([^\/]+)", StudentScoresHandler, name="student_scores"),
        url(r"\/student_exercise\/([^\/]+)\/([^\/]+)/([^\/]+)/([^\/]+)", StudentExerciseHandler, name="student_exercise"),
        url(r"\/exercise_scores\/([^\/]+)\/([^\/]+)\/([^\/]+)", ExerciseScoresHandler, name="exercise_scores"),
        url(r"\/exercise_submissions\/([^\/]+)\/([^\/]+)\/([^\/]+)", ExerciseSubmissionsHandler, name="exercise_submissions"),
        url(r"\/help_requests\/([^\/]+)", HelpRequestsHandler, name="help_requests"),
        url(r"\/submit_request\/([^\/]+)\/([^\/]+)\/([^\/]+)", SubmitHelpRequestHandler, name="submit_request"),
        url(r"\/view_request\/([^\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)", ViewHelpRequestsHandler, name="view_request"),
        url(r"\/delete_request\/([^\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)", DeleteHelpRequestHandler, name="delete_request"),
        url(r"\/back_end\/([^\/]+)", BackEndHandler, name="back_end"),
        url(r"/static/(.+)", StaticFileHandler, name="static_file"),
        url(r"\/summarize_logs", SummarizeLogsHandler, name="summarize_logs"),
        url(r"/login", GoogleLoginHandler, name="login"),
        url(r"/devlogin(/.+)?", DevelopmentLoginHandler, name="devlogin"),
        url(r"/logout", LogoutHandler, name="logout"),
        url(r"/test", TestHandler, name="test"),
    ], autoescape=None)

    return app

if __name__ == "__main__":
    if "PORT" in os.environ and "MPORT" in os.environ:
        application = make_app()

        secrets_dict = load_yaml_dict(read_file("/app/secrets.yaml"))
        application.settings["cookie_secret"] = secrets_dict["cookie"]
        application.settings["google_oauth"] = {
            "key": secrets_dict["google_oauth_key"],
            "secret": secrets_dict["google_oauth_secret"]}
        settings_dict = load_yaml_dict(read_file("/Settings.yaml"))

        content = Content(settings_dict)
        content.create_database_tables()

        database_version = content.get_database_version()
        code_version = int(read_file("VERSION").rstrip())

        # Check to see whether there is a database migration script (should only be one per version).
        # If so, make a backup copy of the database and then do the migration.
        for v in range(database_version, code_version):
            run_command("bash /etc/cron.hourly/back_up_database.sh")

            migration = f"{v}_to_{v + 1}"
            print(f"Checking database status for version {v+1}...")

            if v <= 6:
                command = f"python /migration_scripts/{migration}.py"
            else:
                command = f"python /migration_scripts/migrate.py {migration}"

            result = run_command(command)

            if "***NotNeeded***" in result:
                print("Database migration not needed.")
            elif "***Success***" in result:
                print(f"Database successfully migrated to version {v+1}.")
                content.update_database_version(code_version)
            else:
                print(f"Database migration failed for verson {v+1}, so rolling back...")
                print(result)
                run_command("bash /etc/cron.hourly/restore_database.sh")
                break

        ##for assignment_title in ["18 - Biostatistics - Analyzing proportions"]:
        ##    content.rebuild_exercises(assignment_title)
        ##    content.rerun_submissions(assignment_title)

        server = tornado.httpserver.HTTPServer(application)
        server.bind(int(os.environ['PORT']))
        server.start(int(os.environ['NUM_PROCESSES']))

        user_info_var = contextvars.ContextVar("user_info")
        user_is_administrator_var = contextvars.ContextVar("user_is_administrator")
        user_instructor_courses_var = contextvars.ContextVar("user_instructor_courses")
        user_assistant_courses_var = contextvars.ContextVar("user_assistant_courses")

        # Set up logging
        options.log_file_prefix = "/logs/codebuddy.log"
        options.log_file_max_size = 1024**2 * 1000 # 1 gigabyte per file
        options.log_file_num_backups = 10
        parse_command_line()
        my_log_formatter = LogFormatter(fmt='%(levelname)s %(asctime)s %(module)s %(message)s %(user_id)s')
        logging_filter = LoggingFilter()
        for handler in logging.getLogger().handlers:
            handler.addFilter(logging_filter)
        root_logger = logging.getLogger()
        root_streamhandler = root_logger.handlers[0]
        root_streamhandler.setFormatter(my_log_formatter)

        logging.info("Starting on port {}...".format(os.environ['PORT']))
        tornado.ioloop.IOLoop.instance().start()
    else:
        logging.error("Values must be specified for the PORT and MPORT environment variables.")
        sys.exit(1)
