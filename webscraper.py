from bs4 import BeautifulSoup
import requests
import re
import html


base_url = "https://mdbarrows.com/procedure/"
procedure_names = ["top-eczema-dermatologist", "acne-specialist-gainesville", "psoriasis-north-texas",
                   "rosacea-treatment-dfw", "wart-removal-north-texas", "shingles-treatment-dfw",
                   "mole-removal-denton-tx", "mohs-micrographic-surgery-north-texas", "srt-radiation-mckinney",
                   "levulan-kerastick-dfw", "cryosurgery-north-texas", "topical-chemotherapy-dfw", "botox-dfw", "juvederm-north-texas",
                   "microdermabrasion-gainesville", "chemical-peel-dallas", "skinpen-microneedling-allen", "dermaplaning-rockwall",
                   "tattoo-removal-rockwall", "sclerotherapy-north-texas", "coolsculpting-mckinney", "north-texas-miradry",
                   "ultherapy-mckinney"]


for procedure_name in procedure_names:
    url = f"{base_url}{procedure_name}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        content_div = soup.find("div", class_="col-lg-8")
        if content_div:
            article = content_div.find("article", class_="singlepostinner")
            if article:
                paragraphs = article.find_all("p")
                procedure_content = "\n".join(p.get_text() for p in paragraphs)  # Extract content from paragraphs

                # Cleaning process
                # cleaned_content = re.sub(r'[^\w\s]', '', procedure_content)  # Remove punctuation
                # cleaned_content = cleaned_content.replace('\n', ' ')  # Remove line breaks
                # cleaned_content = re.sub(r'\\u[0-9a-fA-F]+', '', cleaned_content)  # Remove Unicode characters
                # cleaned_content = cleaned_content.replace('\xa0', ' ')  # Replace non-breaking space with regular space
                # # Preserve original web formatting for certain non-breaking space characters (NBSP) such as superscript "TM"
                # cleaned_content = html.unescape(cleaned_content)

                # Print the cleaned content for debugging
                print("Procedure Content:")
                print(procedure_content)

                # Append the cleaned content to the text file
                with open('webscraped_data.txt', 'a', encoding='utf-8') as txt_file:
                    txt_file.write(procedure_content + '\n')
            else:
                print(f"No article found for {procedure_name}")
        else:
            print(f"No content div found for {procedure_name}")
    else:
        print(f"Failed to fetch {url}")
