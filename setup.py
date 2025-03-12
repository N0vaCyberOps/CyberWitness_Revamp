from setuptools import setup, find_packages

setup(
    name="cyber_witness",
    version="0.1",
    packages=find_packages(include=['network*', 'integrations*', 'ml*']),
    install_requires=[
        'scapy>=2.5.0',
        'scikit-learn>=1.0.0',
        'elasticsearch>=7.0.0',
        'aiohttp>=3.8.0',
        'joblib>=1.0.0'
    ],
)