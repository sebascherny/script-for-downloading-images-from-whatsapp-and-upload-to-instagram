from PIL import Image, ImageDraw, ImageFont

def generate_game_result(
    background_path, team1_logo_path, team2_logo_path,
    team1_name, team1_score, team2_name, team2_score,
    liga_banner_path, liga_logo_path,
    output_path
):
    # Load images
    background = Image.open(background_path).resize((1080, 1080))
    team1_logo = Image.open(team1_logo_path).resize((150, 150))
    team2_logo = Image.open(team2_logo_path).resize((150, 150))
    liga_banner = Image.open(liga_banner_path).resize((150, 150))
    liga_logo = Image.open(liga_logo_path).resize((150, 150))
    
    # Create canvas
    final_image = Image.new("RGBA", background.size)
    final_image.paste(background, (0, 0))
    
    # Paste team logos
    final_image.paste(team1_logo, (180, 770), mask=team1_logo)
    final_image.paste(team2_logo, (750, 770), mask=team2_logo)
    final_image.paste(liga_banner, (0, 0), mask=liga_banner)
    final_image.paste(liga_logo, (900, 0), mask=liga_logo)
    
    # Draw text
    draw = ImageDraw.Draw(final_image)
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"  # Adjust if needed
    font_large = ImageFont.truetype(font_path, 80)
    font_medium = ImageFont.truetype(font_path, 50)
    
    # Draw scores
    draw.text((150, 930), str(team1_score), (255, 255, 255), font=font_large)
    draw.text((800, 930), str(team2_score), (255, 255, 255), font=font_large)
    
    # Draw team names
    draw.text((150, 1020), team1_name, (255, 255, 255), font=font_medium)
    draw.text((700, 1020), team2_name, (255, 255, 255), font=font_medium)
    
    # Save output
    final_image = final_image.convert("RGB")
    final_image.save(output_path, "JPEG", quality=90)

if __name__ == "__main__":
    generate_game_result(
        background_path="whatsapp_image_6_Pumbas 43 - 31 Zierbos. Gente muy maja y muy buen partido!.png",
        team1_logo_path="logos_equipos/lcb_jaleo_real.png",
        team2_logo_path="logos_equipos/lcb_paralimpiakos.png",
        team1_name="Jaleo Real",
        team1_score=43,
        team2_name="Paralimpiakos",
        team2_score=31,
        liga_banner_path="liga_banner_captura.png",
        liga_logo_path="lcb_logo_liga.png",
        output_path="game_result.jpg"
    )
