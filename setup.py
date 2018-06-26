from setuptools import setup


requires = [
    'requests',
    'feedparser',
    'lxml',
    'cssselect',
    'sqlalchemy',
]


setup(name="bookmatch.crawler",
      install_requires=requires,
      packages=['bookmatch.crawler'],
      include_package_data=True,
)
