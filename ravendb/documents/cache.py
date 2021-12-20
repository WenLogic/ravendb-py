class cache(object):

    def __init__(self, idgenerator):
        self._cache = []
        self._idgenerator = idgenerator

    def reset(self):
        self._cache = []

    def list(self):
        return self._cache

    def add(self, requests):
        ids = []
        
        for request in requests:
            document = request['document']
            if '@metadata' not in document and 'Raven-Entity-Name' not in document['@metadata']:
                raise Exception('documents must have entity name')
            id = request['id'] if 'id' in request else str(self._idgenerator.Create(document['@metadata']['Raven-Entity-Name']))
            ids.append(id)
            self._cache.append({
                "Method": "PUT",
                "Key": id,
                "Document": document,
                "Metadata": document['@metadata']
            })

        return ids

    def delete(self, documentIds):

        for docId in documentIds:
            for index, item in enumerate(self._cache):
                if docId in item:
                    self._cache.remove(index)
            self._cache.append({
                "Method": "DELETE",
                "Key": docId,
                "Document": {},
                "Metadata": {}
            })

    def update(self, updates):

        ids = []

        for update in updates:
            ids.append(update["id"])

            for index, item in enumerate(self._cache):
                if update["id"] in item:
                    self._cache[index]["document"] = update["document"]
            
            self._cache.append({
                "Method": "PATCH",
                "Key": update['id'],
                "Patches": list(map(
                    lambda item: {
                        "Name": item[0],
                        "Value": item[1],
                        "Type":"UnSet" if item[1] is None else "Set"
                    }
                    ,update["document"].items())),
                "Metadata": {}
            })

        return ids
