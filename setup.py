import re
from setuptools import setup, find_packages

# 'Borrowed' from fastai setup.py
long_description = open('README.md').read()
for ext in ['png', 'svg']:
    long_description = re.sub(r'!\['+ext+'\]\((.*)\)', '!['+ext+']('+'https://raw.githubusercontent.com/corey-cole/sam_iam/master'+'/\\1)', long_description)
    long_description = re.sub(r'src=\"(.*)\.'+ext+'\"', 'src=\"https://raw.githubusercontent.com/corey-cole/sam_iam/master'+'/\\1.'+ext+'\"', long_description)

setup(
    name='sam_iam',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='SAM Policy Template Expansion',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/corey-cole/sam_iam',
    author='Corey Cole',
    author_email='corey.cole@nxdomain.com',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.6, <4',
    include_package_data=True,
    license='AGPLv3+',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
    ],
    platforms='any',
    zip_safe=True,
    entry_points={  # Optional
        'console_scripts': [
            'expand-sam-policy=sam_iam.policy:main',
        ],
    },
)