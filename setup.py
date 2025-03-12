from setuptools import setup, find_packages

setup(
    name="cyber_witness",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'scapy>=2.4.5',
        'numpy>=1.21.0',
        'scikit-learn>=1.0.0',
        'elasticsearch>=7.0.0',
        'aiohttp>=3.8.0',
        'joblib>=1.0.0',
        'cryptography>=38.0.0',
        'pyopenssl>=23.2.0'
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'cyber-witness=network.threat_detector:main',
        ],
    },
)