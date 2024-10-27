import fitz


def pdf_to_html(input_pdf, output_html):
    pdf_document = fitz.open(input_pdf)

    with open(output_html, "w", encoding="utf-8") as html_file:
        html_file.write("<html><body>\n")

        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)

            html_content = page.get_text("html")
            html_file.write(html_content)

        html_file.write("</body></html>")

    print(f"HTML saved as: {output_html}")
