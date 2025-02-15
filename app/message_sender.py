import sys
import subprocess
import os
import requests
import time
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def crop_image_to_grid(image_path, output_folder, x_cells, y_cells):
    img = Image.open(image_path)
    width, height = img.size
    cell_width = width // x_cells
    cell_height = height // y_cells
    os.makedirs(output_folder, exist_ok=True)

    images = []
    for row in range(y_cells):
        for col in range(x_cells):
            left, upper = col * cell_width, row * cell_height
            right, lower = left + cell_width, upper + cell_height
            cropped_img = img.crop((left, upper, right, lower))
            img_path = os.path.join(output_folder, f'cell_{row}_{col}.png')
            cropped_img.save(img_path)
            images.append((row, col, img_path))
    return images

def upload_to_imgur(file_path, client_id):
    headers = {'Authorization': f'Client-ID {client_id}'}
    with open(file_path, 'rb') as img:
        response = requests.post('https://api.imgur.com/3/upload', headers=headers, files={'image': img})
        print(response.text)
    data = response.json()
    return data['data']['link'] if 'data' in data else None

def upload_to_google_sheets(images, spreadsheet_url, sheet_name, creds_path, client_id):
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, [
        "https://spreadsheets.google.com/feeds", 
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    sheet = client.open_by_url(spreadsheet_url).worksheet(sheet_name)

    # Verificar onde o último upload parou
    last_uploaded = 0
    if os.path.exists('last_uploaded.txt'):
        with open('last_uploaded.txt', 'r') as file:
            last_uploaded = int(file.read())

    for idx, (row, col, img_path) in enumerate(images[last_uploaded:], start=last_uploaded):
        public_url = upload_to_imgur(img_path, client_id)
        if public_url:
            cell_value = f'=IMAGE("{public_url}")'
            sheet.update_cell(row + 1, col + 1, cell_value)
            # Atualizar o índice no arquivo de log
            with open('last_uploaded.txt', 'w') as file:
                file.write(str(idx + 1))  # Salvar o índice da próxima célula a ser carregada
        time.sleep(0.5)  # Espera de 0.5 segundo entre uploads

    print(f"Imagens inseridas em {spreadsheet_url} - {sheet_name}")

# Exemplo de uso:
CLIENT_ID = '03f21c703256061'  # Substitua pelo seu Client ID do Imgur
images = crop_image_to_grid(r'Mapa_Mundial.webp', 'recortes', 20, 11)
upload_to_google_sheets(images, 'https://docs.google.com/spreadsheets/d/1K2WCxt6oDK8OPjvnQjC6zM7FBCtjqPajxVZN1-W-omg/edit', 'Página2', 'credentials.json', CLIENT_ID)

# Instale as dependências com:
# pip install pillow gspread oauth2client requests
