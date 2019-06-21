from ticket_system.tests.base import BaseTest


class EventTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        super(EventTest, cls).setUpClass()
        cls.EVENT_URL = '/event/'

    def test_get_events(self):
        response = self.client.get(self.EVENT_URL)
        self.assertContains(response, '\"id\":{}'.format(self.event.id))
