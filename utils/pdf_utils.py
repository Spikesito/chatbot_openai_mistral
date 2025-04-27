import os

def save_uploaded_pdf(uploaded_file, raw_dir="./downloaded_files/raw/"):
    filename = uploaded_file.name.replace(".pdf", "")
    path = os.path.join(raw_dir, f"{filename}.pdf")
    with open(path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return filename

def convert_pdf_to_chunks(pdf_name, output_dir="./downloaded_files/prepared/"):
    os.system(f"marker_single ./downloaded_files/raw/{pdf_name}.pdf --output_dir {output_dir}")
    with open(f"{output_dir}/{pdf_name}/{pdf_name}.md", "r") as f:
        data = f.read()
    return data.split("# ")[1:]
