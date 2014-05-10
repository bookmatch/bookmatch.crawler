from setuptools import setup


requires = [
    'requests',
    'feedparser',
    'lxml',
    'cssselect',
]


setup(name="bookmatch",
      install_requires=requires,
      packages=['bookmatch.crawler'],
      include_package_data=True,
)
