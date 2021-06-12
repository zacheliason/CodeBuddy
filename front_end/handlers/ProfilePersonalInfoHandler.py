import BaseUserHandler

class ProfilePersonalInfoHandler(BaseUserHandler):
    def get(self, user_id):
        try:
            self.render("profile_personal_info.html", page="personal_info", user_info=self.get_user_info(), is_administrator=self.is_administrator(), is_instructor=self.is_instructor(), is_assistant=self.is_assistant())
        except Exception as inst:
            render_error(self, traceback.format_exc())