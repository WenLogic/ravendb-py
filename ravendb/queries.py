import time
from .documents import loader as l
from .indexes import querier as q


class queries(object):

    def __init__(self, client):
        self._client = client

    def load(self, documentIds):
        return l.loader(self._client).load(documentIds)

    def query(self, indexId, query, fetch={}, pageoffset=0, pagelimit=256):
        querier = q.querier(self._client, indexId)
        response = querier.query(query, fetch, pageoffset, pagelimit)

        attempt = 0
        maxAttempts = self._client.config.maxAttemptsToWaitForNonStaleResults

        if self._client.config.waitForNonStaleResults:
            while response["IsStale"] is True:
                time.sleep(self._client.config.secondsToWaitForNonStaleResults)
                if attempt <= maxAttempts:
                    attempt = attempt + 1
                    response = querier.query(query, fetch, pageoffset, pagelimit)
                else:
                    return response

        return response
