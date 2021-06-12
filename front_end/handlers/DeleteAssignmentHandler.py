import BaseUserHandler

class DeleteAssignmentHandler(BaseUserHandler):
    def post(self, course, assignment):
        try:
            if not self.is_administrator() and not self.is_instructor_for_course(course):
                self.render("permissions.html")
                return

            content.delete_assignment(content.get_assignment_basics(course, assignment))
        except Exception as inst:
            render_error(self, traceback.format_exc())
