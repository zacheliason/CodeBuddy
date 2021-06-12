import BaseUserHandler

class RunCodeHandler(BaseUserHandler):
    async def post(self, course, assignment, exercise):
        out_dict = {"text_output": "", "image_output": ""}

        try:
            code = self.get_body_argument("user_code").replace("\r", "")
            exercise_basics = content.get_exercise_basics(course, assignment, exercise)
            exercise_details = content.get_exercise_details(course, assignment, exercise)

            text_output, image_output = exec_code(settings_dict, code, exercise_basics, exercise_details, request=None)

            out_dict["text_output"] = format_output_as_html(text_output)
            out_dict["image_output"] = image_output
        except ConnectionError as inst:
            out_dict["text_output"] = "The front-end server was unable to contact the back-end server."
        except ReadTimeout as inst:
            out_dict["text_output"] = f"Your solution timed out after {settings_dict['back_ends'][exercise_details['back_end']]['timeout_seconds']} seconds."
        except Exception as inst:
            out_dict["text_output"] = format_output_as_html(traceback.format_exc())

        self.write(json.dumps(out_dict))
