from distutils.core import setup

setup(
    name='qilaihi.club',
    version='20160529',
    packages=['api', 'api.v1', 'api.v1.lbs', 'model', 'route', 'weixin', 'weixin.msghandler', 'weixin.eventparser'],
    package_dir={'': 'server'},
    url='http://qilaihi.me',
    license='N/A',
    author='zhangyan',
    author_email='john.zhangyan@gmail.com',
    description=''
)
