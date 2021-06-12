import BaseUserHandler

class CheckPartnersHandler(BaseUserHandler):
    def post(self, course):
        partner_key = self.get_body_argument("partner_key")
        partner_dict = content.get_partner_info(course, self.get_user_info()["user_id"])

        # determine whether partner_key is a valid one while hiding student emails from the client side
        if partner_key in partner_dict.keys():
            self.write(json.dumps(True))
        else:
            self.write(json.dumps(False))
