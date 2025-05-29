from flask import Flask, request, jsonify, send_file, abort
import requests
import os
import random

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'ekranlar')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/<int:random_id>', methods=['GET'])
def download_image(random_id):
    file_path = os.path.join(UPLOAD_FOLDER, f'{random_id}.jpg')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'batu': 'Dosya bulunamadı'}), 404

@app.route('/', methods=['GET'])
def capture_screenshot():
    url = request.args.get('url')
    if not url or not url.startswith('http'):
        return jsonify({'batu': 'LINK NERDE YARRAM'}), 400

    params = {
        'tkn': '125',        # Pikwy'den aldığın token'i buraya koy.
        'd': '3000',
        'u': url,
        'fs': '0',
        'w': '1280',
        'h': '1200',
        's': '100',
        'z': '100',
        'f': 'jpg',
        'rt': 'jweb'
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get("https://api.pikwy.com/", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        image_url = data.get("iurl")
        if not image_url:
            return jsonify({'batu': 'Ekran görüntüsü URL\'si alınamadı!'}), 500

        img_resp = requests.get(image_url)
        img_resp.raise_for_status()

        random_id = random.randint(100000, 999999)
        file_path = os.path.join(UPLOAD_FOLDER, f'{random_id}.jpg')
        with open(file_path, 'wb') as f:
            f.write(img_resp.content)

        return jsonify({
            'batu': '✅ Ekran görüntüsü başarıyla alındı.',
            'indirme_linki': f'{request.host_url}{random_id}'
        })

    except Exception as e:
        return jsonify({'hata': f'Bir hata oluştu: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
