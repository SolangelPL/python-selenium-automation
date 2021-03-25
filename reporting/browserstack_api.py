import requests

from support.logger import logger


class BSSession:
    session = 'https://{}:{}@api-cloud.browserstack.com/automate/sessions/{}.json'

    def __init__(self, bs_user, bs_key, session_id):
        """
        :param bs_user: BrowserStack username
        :param bs_key: BrowserStack account key
        :param session_id: Driver session, established upon Remote Driver connection to BrowserStack
        """
        self.bs_user = bs_user
        self.bs_key = bs_key
        self.session_id = session_id
        self.automation_session = {}

    def _get_session_info(self):
        session_url = self.session.format(self.bs_user, self.bs_key, self.session_id)
        response = requests.get(session_url)
        logger.info('GET {}\nResponse {}:\n{}'.format(session_url, response.status_code, response.content))
        self.automation_session = response.json()['automation_session']

    def get_browser_url(self) -> str:
        """
        :return: automation_session -> browser_url, generated by BS
        """
        if not self.automation_session:
            self._get_session_info()
        return self.automation_session['browser_url']

    def put_fail_status(self, step_name):
        """
        Display step as failed on BrowserStack (controls the red dot)
        :param step_name: step.name from behave, displayed af a reason for failure
        """
        session_url = self.session.format(self.bs_user, self.bs_key, self.session_id)
        response = requests.put(session_url, data={'status': 'error', 'reason': 'Step failed: {}'.format(step_name)})
        logger.info('PUT {}\nResponse {}:\n{}'.format(session_url, response.status_code, response.content))