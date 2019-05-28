import uuid, subprocess, os
from flask import Flask, jsonify, request, send_file, after_this_request

app = Flask(__name__)

@app.route('/api/stl/thumb', methods=['GET', 'POST'])
def get_stl_thumbnail():
    # Create SCAD file.
    session_id = uuid.uuid1()
    stl_file = 'test.stl'
    scad_file = '{}.scad'.format(session_id)
    png_file = '{}.png'.format(session_id)

    with open(scad_file, 'w+') as file:
        file.write('import("{}");'.format(stl_file))

    # Render image.
    res = subprocess.check_output(['openscad', '-o', png_file, scad_file, '--colorscheme=Tomorrow', '--viewall', '--autocenter', '--render'])
    print(res)

    # Clean up.
    @after_this_request
    def remove_files(response):
        try:
            os.remove(scad_file)
        except Exception as error:
            print('An error ocurred when removing: {}.'.format(scad_file))
        try:
            os.remove(png_file)
        except Exception as error:
            print('An error ocurred when removing: {}.'.format(png_file))
        return response
    return send_file(png_file, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
