from whatsapp_checker_script import main as get_latest_pictures_from_whatsapp
from image_generator import generate_game_result
from instagram_publisher import upload_instagram_post

import re

team_logo_path_to_aliases = {
    "lcb_airballs.png": ["airballs"],
    "lcb_all_stones.png": ["all stones", "allstones"],
    "lcb_zierbos_lokos.png": ["zierbos", "zierbos lokos", "lokos zierbos", "zierboslokos", "siervos lokos", "ciervos lokos"],
    "lcb_pumbas.png": ["pumbas"],
}

def get_pictures_to_upload():
    pictures_to_upload = []
    pictures_paths_and_texts = get_latest_pictures_from_whatsapp()
    for (players_picture_path, text) in pictures_paths_and_texts:
        print(f"Viendo la foto guardada en '{players_picture_path}', cuyo texto en Whatsapp es '{text}'")
        for i, regex_str in enumerate([
            "([\w\d ]+) (\d+) ?- ?([\w\d ]+) (\d+)",
            "([\w\d ]+) (\d+) ?- ?(\d+) ([\w\d ]+)[\.\,$]"
        ]):
            matched_groups = re.search(regex_str, text)
            if (not matched_groups) or (not matched_groups.groups()):
                continue
            matched_groups = matched_groups.groups()
            if len(matched_groups) == 4:
                team_1_name = matched_groups[0]
                team_1_score = matched_groups[1]
                if i == 0:
                    team_2_name = matched_groups[2]
                    team_2_score = matched_groups[3]
                else:
                    team_2_score = matched_groups[2]
                    team_2_name = matched_groups[3]
                team_1_name = team_1_name.lower()
                team_2_name = team_2_name.lower()
                print(f"Equipos y resultados encontrados! {team_1_name} ({team_1_score}) jugó contra {team_2_name} ({team_2_score})")
                team1_logo_path, team2_logo_path = None, None
                for logo_path, aliases in team_logo_path_to_aliases.items():
                    if team_1_name in aliases:
                        team1_logo_path = logo_path
                    if team_2_name in aliases:
                        team2_logo_path = logo_path
                if team1_logo_path is None or team2_logo_path is None:
                    continue
                output_path = "game_results/" + team_1_name + " " + team_1_score + " - " + team_2_name + " " + team_2_score + ".jpg"
                generate_game_result(
                    players_picture_path,
                    "logos_equipos/" + team1_logo_path, "logos_equipos/" + team2_logo_path,
                    team_1_name, team_1_score, team_2_name, team_2_score,
                    "liga_banner_captura.png", "lcb_logo_liga.png",
                    output_path
                )
                pictures_to_upload.append(output_path)
    return pictures_to_upload

def main():
    # pictures_to_upload = ['game_results/pumbas 43 - zierbos 31.jpg', 'game_results/all stones 39 - airballs 45.jpg']
    pictures_to_upload = get_pictures_to_upload()
    print(f"Creé {len(pictures_to_upload)} imágenes con logos y resultados que se van a publicar: {pictures_to_upload}")
    username = "estebanchedno@gmail.com"
    password = "JajaJaja12"
    upload_instagram_post(username, password, pictures_to_upload, "Hola! Esta es una prueba automática de subida de fotos... con emoji 🏀 🏀")


if __name__ == "__main__":
    main()