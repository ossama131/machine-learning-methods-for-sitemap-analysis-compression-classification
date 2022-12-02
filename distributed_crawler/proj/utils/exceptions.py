class SitemapRequestError(Exception):
    pass

class SitemapGunzipError(Exception):
    pass

class SitemapUnicodeError(Exception):
    pass

class SitemapParsingError(Exception):
    pass

class SitemapTypeNotHandledError(Exception):
    pass

class SitemapEmptyError(Exception):
    pass

class SitemapMaximumRecursionLevelReached(Exception):
    pass

class MinioS3Error(Exception):
    pass

class MinioS3UnicodeError(Exception):
    pass