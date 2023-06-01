import uuid
from flask import Flask, render_template, request, send_file
from io import BytesIO
from os.path import splitext
from PIL import Image
from reportlab.pdfgen import canvas

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/converter', methods=['POST'])
def converter():
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)
    unique_filename = str(uuid.uuid4())

    for img_file in request.files.getlist('imagens'):
        img = Image.open(img_file)
        img_ext = splitext(img_file.filename)[1].lower()
        if img_ext not in ('.jpg', '.jpeg', '.png'):
            return 'Extensão de arquivo inválida. Use apenas .jpg, .jpeg ou .png.'

        width, height = img.size
        pdf.setPageSize((width, height))
        img.save(f'/tmp/{unique_filename}.png')
        pdf.drawImage(f'/tmp/{unique_filename}.png',
                      0, 0, width=width, height=height)
        pdf.showPage()

    pdf.save()

    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name='converted.pdf')


app.register_blueprint(multiple_routes)

if __name__ == '__main__':
    app.run()
