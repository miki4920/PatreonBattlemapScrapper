class Submission(object):
    def __init__(self, links, tags):
        self.links = links
        self.tags = tags
        self.compressed_photos = []
        self.photos = []