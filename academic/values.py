import os
import platform
import yaml

ERROR = 0
ACCEPT = 1

INTO_TEMPLATE_MD = "# 个人简介 \n 无"
INTO_TEMPLATE_HTML = '<h1><a id="_0"></ a>个人简介</h1> <p>无</p > '

MAGIC = "s~8>1)"

SALT1 = 'a'
SALT2 = 'w'
SALT3 = '1'
SALT4 = '7'

# with open(BASE_DIR / 'secrets.yaml', 'r') as f:
#     secrets = yaml.load(f, Loader=yaml.FullLoader)

# ES_IP = secrets['ES']['IP']
# ES = Elasticsearch(
# 	hosts = ES_IP
# )

# ES_INDEX = secrets['ES']['INDEX']

APPEAL_PAPER = 1
APPEAL_IDENTITY = 2
CLAIM_PAPER = 3
FEEDBACK = 4
RERLY = 5

PAGE = 20

STORAGE_PATH = ''

NOT = 2
AND = 1
OR = 0

ALPHA = 0.01
BETA = 3.14159265358979 * 2.71828 * 100
