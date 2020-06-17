# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='scrapyredis',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy':['settings=scrapyredis.settings']},
)