from flask import Flask, render_template, request
import cv2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_image():
    image_file = request.files['image']
    size = int(request.form['size'])
    color = [int(request.form['colorB']), int(request.form['colorG']), int(request.form['colorR'])]
    position = request.form['position']

    # Simpan file gambar yang diunggah
    image_path = 'static/uploads/image.jpg'
    image_file.save(image_path)

    # Baca gambar menggunakan OpenCV
    img = cv2.imread(image_path)

    # Fungsi untuk memotong gambar berdasarkan posisi
    def crop_by_position(img, position, size):
        if position == 'top_left':
            cropped_image = img[0:size, 0:size]
        elif position == 'top_center':
            cropped_image = img[0:size, img.shape[1] // 2 - size // 2:img.shape[1] // 2 + size // 2]
        elif position == 'top_right':
            cropped_image = img[0:size, img.shape[1] - size:img.shape[1]]
        elif position == 'center_left':
            cropped_image = img[img.shape[0] // 2 - size // 2:img.shape[0] // 2 + size // 2, 0:size]
        elif position == 'center':
            cropped_image = img[img.shape[0] // 2 - size // 2:img.shape[0] // 2 + size // 2, img.shape[1] // 2 - size // 2:img.shape[1] // 2 + size // 2]
        elif position == 'center_right':
            cropped_image = img[img.shape[0] // 2 - size // 2:img.shape[0] // 2 + size // 2, img.shape[1] - size:img.shape[1]]
        elif position == 'bottom_left':
            cropped_image = img[img.shape[0] - size:img.shape[0], 0:size]
        elif position == 'bottom_center':
            cropped_image = img[img.shape[0] - size:img.shape[0], img.shape[1] // 2 - size // 2:img.shape[1] // 2 + size // 2]
        elif position == 'bottom_right':
            cropped_image = img[img.shape[0] - size:img.shape[0], img.shape[1] - size:img.shape[1]]
        else:
            # Posisi tidak valid, kembalikan None
            return None
        
        return cropped_image

    # Panggil fungsi crop_by_position
    cropped_image = crop_by_position(img, position, size)
    cropped_image_path = 'static/uploads/cropped_image.jpg'
    cv2.imwrite(cropped_image_path, cropped_image)

    return render_template('index.html',
                           image_path=image_path,
                           cropped_image_path=cropped_image_path)

if __name__ == '__main__':
    app.run(debug=True)
