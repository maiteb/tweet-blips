# encoding: utf-8
import re

QUADRANT_DICT = {
    "tecnicas":"techniques",
    "técnicas":"techniques",
    "techniques":"techniques",
    "plataformas":"platforms",
    "plataforms":"platforms",
    "ferramentas":"tools",
    "tools":"tools",
    "linguagens e frameworks":"languages & frameworks",
    "linguagens & frameworks":"languages & frameworks",
    "languages and frameworks":"languages & frameworks",
    "languages & frameworks":"languages & frameworks"
}

CYCLE_DICT = {
    "adote":"adopt",
    "adopt":"adopt",
    "experimente":"trial",
    "trial":"trial",
    "avalie":"assess",
    "assess":"assess",
    "evite":"hold",
    "hold":"hold"
}

REGEX_quadrant="(T[é|e]cnicas|Plataformas|Ferramentas|Linguagens\s?[&|e|&amp;]\s?Frameworks|Techniques|Platforms|Tools|Languages\s?[&|and|&amp;]\s?Frameworks)"
REGEX_CYCLE="(Adote|Experimente|Avalie|Evite|Adopt|Trial|Assess|Hold)"
REGEX_BLIP="(.*)$"

FULL_REGEX="^[.*]?" + REGEX_quadrant + "[\s*]?-[\s*]?" + REGEX_CYCLE + "[\s*]?-[\s*]?" + REGEX_BLIP
print FULL_REGEX
class Tweet:

    def __init__(self, date, username, name, content):
        self.date = date
        self.username = username.encode('ascii', 'ignore')
        self.name = name.encode('ascii', 'ignore')
        self.split_content(content.encode('ascii', 'ignore'))

    def split_content(self, content):
        print content
        results = re.search(FULL_REGEX, content)
        self.quadrant = QUADRANT_DICT[results.group(1).lower()]
        self.cycle = CYCLE_DICT[results.group(2).lower()]
        dirty_blip = results.group(3).lower()
        self.blip = dirty_blip[:dirty_blip.index('#')].strip()

    def __str__(self):
        return "[%s] %s (@%s): [%s %s %s]" % (self.date, self.name, self.username, self.quadrant, self.cycle, self.blip)
