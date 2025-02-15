import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image

def crop_image_to_grid(image_path, output_folder, x_cells, y_cells):
    img = Image.open(image_path)
    width, height = img.size
    os.makedirs(output_folder, exist_ok=True)
    
    return [(row, col, f'cell_{row}_{col}.png') for row in range(y_cells) for col in range(x_cells)]

def upload_to_google_sheets(images, spreadsheet_url, sheet_name, creds_path, github_user, repo, branch, folder):
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, [
        "https://spreadsheets.google.com/feeds", 
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    sheet = client.open_by_url(spreadsheet_url).worksheet(sheet_name)

    for row, col, img_name in images:
        github_url = f'https://raw.githubusercontent.com/{github_user}/{repo}/{branch}/{folder}/{img_name}?raw=true'
        cell_value = f'=IMAGE("{github_url}")'
        sheet.update_cell(row + 1, col + 1, cell_value)

    print(f"Matriz de imagens inserida em {spreadsheet_url} - {sheet_name}")

# Parâmetros - Repositório deve ser público para acesso direto:
github_user = 'ThiagoJurge'
repo = 'nindo-new'
branch = 'main'
folder = 'recortes'
creds_path = 'credentials.json'
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1K2WCxt6oDK8OPjvnQjC6zM7FBCtjqPajxVZN1-W-omg/edit'
sheet_name = 'Página2'

images = crop_image_to_grid('Mapa_Mundial.webp', 'recortes', 20, 11)
upload_to_google_sheets(images, spreadsheet_url, sheet_name, creds_path, github_user, repo, branch, folder)
