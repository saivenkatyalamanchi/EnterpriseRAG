import fitz


def parse_pdf(file_path):
    documents = []

    with fitz.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):

            documents.append(
                {
                    "page": page_number,
                    "content": page.get_text(),
                    "metadata": {
                        "source": str(file_path),
                        "page": page_number
                    }
                }
            )

    return documents