class ProfileSelectCourseHandler(BaseUserHandler):
    def get(self, user_id):
        try:
            if self.is_administrator():
                courses = content.get_courses()
            elif self.is_instructor():
                courses = content.get_courses_connected_to_user(user_id)

            if len(courses) > 1:
                self.render("profile_select_course.html", courses=courses, page="instructor", user_info=self.get_user_info(), is_administrator=self.is_administrator(), is_instructor=self.is_instructor(), is_assistant=self.is_assistant())
            else:
                self.render("profile_instructor.html", page="instructor", tab=None, course=courses[0][1], assignments=content.get_assignments(courses[0][0]), instructors=content.get_users_from_role(courses[0][0], "instructor"), assistants=content.get_users_from_role(courses[0][0], "assistant"), registered_students=content.get_registered_students(courses[0][0]), result=None, user_info=self.get_user_info(), is_administrator=self.is_administrator(), is_instructor=self.is_instructor_for_course(courses[0][0]), is_assistant=self.is_assistant_for_course(courses[0][0]))
        except Exception as inst:
            render_error(self, traceback.format_exc())
