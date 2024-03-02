from datetime import datetime
import os

def get_file_path(width: int, height: int, base_dir="charts") -> str:
    current_date = datetime.now()
    date_path = current_date.strftime("%Y/%m")
    directory_path = f"{base_dir}/{date_path}"

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_name = f"chart_{width}x{height}_{current_date.strftime('%Y%m%d%H%M%S')}.png"
    return f"{directory_path}/{file_name}"
