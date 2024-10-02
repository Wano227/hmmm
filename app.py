from flask import Flask, render_template, request, send_file
from weasyprint import HTML
from io import BytesIO
import datetime

app = Flask(__name__)

# Home route to render the invoice form
@app.route('/')
def invoice_form():
    return render_template('invoice_form.html')

# Route to handle form submission and PDF generation
@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    invoice_data = {
        'invoice_number': request.form.get('invoice_number'),
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'client_name': request.form.get('client_name'),
        'client_address': request.form.get('client_address'),
        'items': [],
        'total': 0,
    }

    # Fetch the items from the form
    for i in range(5):  # Assume up to 5 items
        item_name = request.form.get(f'item_name_{i}')
        quantity = request.form.get(f'quantity_{i}')
        price = request.form.get(f'price_{i}')
        if item_name and quantity and price:
            total_price = int(quantity) * float(price)
            invoice_data['items'].append({
                'name': item_name,
                'quantity': quantity,
                'price': price,
                'total_price': total_price
            })
            invoice_data['total'] += total_price

    # Render the HTML template and generate PDF
    rendered_html = render_template('invoice_template.html', data=invoice_data)
    pdf_file = BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_file)
    pdf_file.seek(0)

    return send_file(pdf_file, attachment_filename=f"invoice_{invoice_data['invoice_number']}.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
