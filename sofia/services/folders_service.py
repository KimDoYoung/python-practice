import asyncio

async def get_image_folder_with_id(folder_id):
    # Assuming you have an asynchronous database connection
    # Replace the database query with the appropriate code for your database
    # Here's an example using a fictional database library called "asyncdb"
    db = asyncdb.connect("your_database_connection_string")
    folder = await db.query("SELECT * FROM image_folders WHERE id = ?", folder_id)

    # Return None if no image folder with the given ID is found
    if not folder:
        return None

    # Assuming the database query returns a dictionary-like object
    image_folder = {
        "id": folder["id"],
        "name": folder["name"],
        "files": folder["files"].split(",")  # Assuming files are stored as a comma-separated string
    }

    return image_folder

# Example usage
async def main():
    folder_id = 2
    image_folder = await get_image_folder_with_id(folder_id)
    if image_folder:
        print(f"Image folder found: {image_folder['name']}")
        print(f"Related files: {image_folder['files']}")
    else:
        print("Image folder not found.")

# Run the main function asynchronously
asyncio.run(main())
