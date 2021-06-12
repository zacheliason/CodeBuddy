import BaseUserHandler

class DevelopmentLoginHandler(RequestHandler):
    def get(self, target_path):
        if not target_path:
            target_path = ""

        self.render("devlogin.html", courses=content.get_courses(False), target_path=target_path)

    def post(self, target_path):
        try:
            user_id = self.get_body_argument("user_id")

            if user_id == "":
                self.write("Invalid user ID.")
            else:
                if not content.user_exists(user_id):
                    # Add static information for test user.
                    user_dict = {'id': user_id, 'email': 'test_user@gmail.com', 'verified_email': True, 'name': 'Test User', 'given_name': 'Test', 'family_name': 'User', 'picture': 'https://vignette.wikia.nocookie.net/simpsons/images/1/15/Capital_City_Goofball.png/revision/latest?cb=20170903212224', 'locale': 'en'}
                    content.add_user(user_id, user_dict)

                self.set_secure_cookie("user_id", user_id, expires_days=30)

                if not target_path:
                    target_path = "/"
                self.redirect(target_path)

        except Exception as inst:
            render_error(self, traceback.format_exc())
