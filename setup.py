from setuptools import setup

setup(
    name='Pdf_highlight',
    version='1.0.0',
    packages=['edge_pdf'],
    url='',
    license='BSD (3-clause)',
    author='wangwl',
    author_email='643176574@qq.com',
    description='pdf工具库',
    python_requires='>=3.6, <=3.12',
    install_requires=["PyMuPDF==1.22.5", "pandas==2.0.3", "openpyxl==3.1.2"],
    # extras_require={"annot_read": ["PyMuPDF==1.22.5"], },
    entry_points={
        'console_scripts': [
            'readpdf = edge_pdf.annot_read:read_annot'
        ]
    },
)
