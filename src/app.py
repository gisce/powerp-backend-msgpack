from flask import Flask, request, abort
import msgpack
from ooservice import OpenERPService, PoolWrapper
import bjoern

import os
import sys


os.environ.update({
    'OPENERP_ROOT_PATH': "/home/ecarreras/Projectes/erp/server/bin",
    'OPENERP_ADDONS_PATH': "/home/ecarreras/Projectes/erp/server/bin/addons",
    'OPENERP_DB_HOST': "localhost",
    'OPENERP_DB_PORT': "5432",
    'OPENERP_DB_USER': "erp",
    'OPENERP_DB_PASSWORD': "erp",
    'OPENERP_DB_NAME': "test_ov",
})

sys.path.extend([
    os.environ['OPENERP_ROOT_PATH'],
    os.environ['OPENERP_ADDONS_PATH']
])


app = Flask(__name__)
service = OpenERPService()


@app.route('/', methods=['POST'])
def execute():
    data = request.get_data()
    args = msgpack.unpackb(data, raw=False)
    #db, uid, passwd, object, method, *args)
    print(args)
    if args[0] != service.db_name:
        raise abort(403)
    uid = service.login(args[1], args[2])
    if not uid:
        raise abort(403)
    c = PoolWrapper(service.pool, service.db_name, uid)
    obj = c.model(args[3])
    method = args[4]
    method_args = args[5:]
    res = getattr(obj, method)(*method_args)
    return msgpack.packb(res, use_bin_type=False)


if __name__ == '__main__':
    bjoern.run(app, 'localhost', 8000, reuse_port=True)
