class MockResponse():
    def __init__(self, status='ok', articles=[], total_results=0):
        self.data = {
            'status': status,
            'articles': articles,
            'totalResults': total_results,
        }

    def json(self):
        return self.data
