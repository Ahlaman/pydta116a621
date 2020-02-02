import setuptools
from distutils.core import setup
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session="hack")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(name='pydta116a621',
      install_requires=reqs,
      version='0.3.0',
      description='Daikin DTA116A621 SDK',
      author='Jason Gao',
      author_email='github@jasongao.com',
      url='https://github.com/JasonGao180/pydta116a621',
      packages=['pydta116a621'],
     )
