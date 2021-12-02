#create helper in log in
class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
