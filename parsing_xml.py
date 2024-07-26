from bs4 import BeautifulSoup

def extract_text_from_tei(tei_file):
    with open(tei_file, 'r', encoding='utf-8') as file:
        tei_string = file.read()

    soup = BeautifulSoup(tei_string, 'xml')
    paragraphs = soup.find_all('p')

    extracted_text = ''
    for i, paragraph in enumerate(paragraphs):
        extracted_text += f'p{i + 1}:\n{paragraph.get_text(strip=False)}\n\n'

    # Write extracted text to a file with .txt extension
    output_file = tei_file[:-4] + '.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(extracted_text)

    print(f"Text extracted and saved to {output_file}")

# Example usage
tei_file = 'xml_files/1703-08-08.xml'
extract_text_from_tei(tei_file)
