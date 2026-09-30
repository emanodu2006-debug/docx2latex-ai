from setuptools import setup, find_packages

setup(
    name='docx2latex',
    version='0.1.0',
    description='Convert Word documents to Overleaf-ready LaTeX with local AI models.',
    author='docx2latex contributors',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['python-docx>=1.0.0', 'requests>=2.31.0'],
    entry_points={'console_scripts': ['docx2latex=docx2latex.cli:main']},
    package_data={'docx2latex': ['templates/*.tex']},
)
