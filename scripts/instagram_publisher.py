from instagrapi import Client

def upload_instagram_post(username, password, image_paths, caption):
    """
    Uploads multiple images as a carousel post to Instagram.

    :param username: Instagram username
    :param password: Instagram password
    :param image_paths: List of image file paths
    :param caption: Caption for the post
    """
    try:
        cl = Client()
        print(f"Logueandome en cuenta de {username}")
        cl.login(username, password)
        print(f"Entré!\nSubo album con {len(image_paths)} fotos, de texto: {caption}")
        print("...")
        cl.album_upload(image_paths, caption=caption)
        print("Álbum subido correctamente!")
    except Exception as e:
        print("Error uploading to Instagram:", e)

if __name__ == "__main__":
    # Example usage
    username = os.getenv("IG_USERNAME")
    password = os.getenv("IG_PASSWORD")
    image_paths = ["game_result.jpg", "game_result2.jpg"]  # Add all image paths
    caption = "This week's basketball league results! 🏀🔥 #BasketballLeague"
    upload_instagram_post(username, password, image_paths, caption)
