from setuptools import setup

setup(
    name='python-fcm',
    version='1.0.0',
    description='Send push notification through Firebase Cloud Messaging API',
    long_description='Check it out on GitHub...',
    keywords='firebase cloud messaging google fcm',
    url='https://github.com/asistia/python-fcm',
    download_url = 'https://github.com/asistia/python-fcm/tarball/1.0.0',
    author='henocdz',
    author_email='self@henocdz.com',
    license='MIT',
    packages=['python-fcm'],
    install_requires=['requests>=2.8.1'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
)