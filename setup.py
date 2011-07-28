from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='katran',
      version=version,
      description="The website of The Offices of the Kat Ran Press",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Sam Jacoby',
      author_email='sam@shackmanpress.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
        'Django==1.3',
        'PIL==1.1.7',
        'South==0.7.3',
        'distribute==0.6.14',
        'django-appmedia==1.0.1',
        'django-classy-tags==0.3.0',
        'django-cms==2.1.1',
        'sorl-thumbnail==11.01',
        'wsgiref==0.1.2',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

