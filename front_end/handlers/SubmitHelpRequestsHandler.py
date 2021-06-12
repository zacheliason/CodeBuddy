import BaseUserHandler

class SubmitHelpRequestHandler(BaseUserHandler):
    def post(self, course, assignment, exercise):
        try:
            user_id = self.get_user_id()
            student_comment = self.get_body_argument("student_comment")
            help_request = content.get_help_request(course, assignment, exercise, user_id)
            if help_request:
                content.update_help_request(course, assignment, exercise, user_id, student_comment)

            else:
                code = self.get_body_argument("user_code").replace("\r", "")

                exercise_basics = content.get_exercise_basics(course, assignment, exercise)
                exercise_details = content.get_exercise_details(course, assignment, exercise)

                text_output, image_output = exec_code(settings_dict, code, exercise_basics, exercise_details, request=None)
                #text_output = format_output_as_html(text_output)

                content.save_help_request(course, assignment, exercise, user_id, code, text_output, image_output, student_comment, datetime.datetime.now())

        except Exception as inst:
            render_error(self, traceback.format_exc())
