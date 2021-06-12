import BaseUserHandler

class CourseHandler(BaseUserHandler):
    def get(self, course):
        if self.is_administrator() or self.is_instructor_for_course(course) or self.is_assistant_for_course(course):
            try:
                assignments = content.get_assignments(course, True)

                self.render("course_admin.html", courses=content.get_courses(True), assignments=assignments, course_basics=content.get_course_basics(course), course_details=content.get_course_details(course, True), course_scores=content.get_course_scores(course, assignments), user_info=self.get_user_info(), is_administrator=self.is_administrator(), is_instructor=self.is_instructor_for_course(course))
            except Exception as inst:
                render_error(self, traceback.format_exc())
        else:
            try:
                self.render("course.html", courses=content.get_courses(False), assignments=content.get_assignments(course, False), assignment_statuses=content.get_assignment_statuses(course, self.get_user_id()), course_basics=content.get_course_basics(course), course_details=content.get_course_details(course, True), curr_datetime=datetime.datetime.now(), user_info=self.get_user_info())
            except Exception as inst:
                render_error(self, traceback.format_exc())
