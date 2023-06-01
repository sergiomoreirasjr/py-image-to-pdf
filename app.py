from flask import Flask
from multipleRoutes import multiple_routes
from io import BytesIO
from os.path import splitext

from flask import Flask, render_template, request, send_file
from PIL import Image
from reportlab.pdfgen import canvas


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/converter', methods=['POST'])
def converter():
    img = Image.open(request.files['imagem'])
    img_ext = splitext(request.files['imagem'].filename)[1].lower()
    if img_ext not in ('.jpg', '.jpeg', '.png'):
        return 'Extensão de arquivo inválida. Use apenas .jpg, .jpeg ou .png.'

    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)

    width, height = img.size
    pdf.setPageSize((width, height))
    img.save('/tmp/image.png')
    pdf.drawImage('/tmp/image.png', 0, 0, width=width, height=height)

    pdf.showPage()
    pdf.save()

    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name='converted.pdf')


app.register_blueprint(multiple_routes)

if __name__ == '__main__':
    app.run()
