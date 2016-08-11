from string import Template

BASE_URL = "http://nrc.nl"

class ArticleHtml:

    def __init__(self):
        self.template = Template("""
            <h2><a href='%s$url'>[$tag] $headline</a></h2>
            <p>$teaser</p>
            <hr><br>
        """ % BASE_URL)

    def create_article_html(self, rec):
        return self.template.substitute(
            url=rec.url, tag=rec.tag, 
            headline=rec.headline, teaser=rec.teaser
        )
