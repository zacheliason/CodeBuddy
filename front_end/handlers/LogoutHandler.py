from tornado.web import *

class LogoutHandler(RequestHandler):
    def get(self):
        try:
            self.clear_all_cookies()

            if settings_dict["mode"] == "production":
                self.redirect("https://accounts.google.com/Logout")
            else:
                self.redirect("/")
        except Exception as inst:
            render_error(self, traceback.format_exc())
