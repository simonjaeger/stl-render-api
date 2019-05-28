import uuid
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/stl/thumb', methods=['GET', 'POST'])
def get_stl_thumbnail():
    # Create SCAD file.
    session_id = uuid.uuid1()
    stl_file = 'test.stl'
    scad_file = '{}.scad'.format(session_id)
    png_file = '{}.png'.format(session_id)

    with open(scad_file, 'w+') as file:
        file.write('import({});'.format(stl_file))

    # Render image.
    res = subprocess.check_output(['openscad', '-o', png_file, scad_file])
    print(res)

    return jsonify({'task': res}), 201

if __name__ == '__main__':
    app.run(debug=True)
