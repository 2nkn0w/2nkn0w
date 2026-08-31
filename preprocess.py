import json
import os

def main():
    config_path = "config.json"
    if not os.path.exists(config_path):
        print("config.json not found!")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Render header and Twitch status badge
    github_user = config.get("github_username", "")
    header_img = config.get("header_image", "")
    
    header_html = f'<p align="center"><img src="https://raw.githubusercontent.com/{github_user}/{github_user}/main/{header_img}" /></p>\n\n' if header_img else ""

    twitch_url = config.get("socials", {}).get("twitch", "")
    twitch_badge = ""
    if twitch_url:
        twitch_user = twitch_url.split("/")[-1]
        twitch_badge = (
            f'<a href="{twitch_url}" target="_blank" rel="noreferrer"><img\n'
            f'src="https://img.shields.io/twitch/status/{twitch_user}?logo=twitchsx&style=for-the-badge&color=0891b2&labelColor=1c1917&label=TWITCH+STATUS" /></a>\n\n'
        )

    # Render Socials section
    socials_html = "### Socials\n\n<p align=\"left\">"
    socials_map = config.get("socials", {})
    enabled_socials = config.get("enabled_socials", [])

    # danielcranney icons lookup
    # Mapping for name overrides or light/dark assets
    icon_mapping = {
        "github": ("github.svg", "github-dark.svg"),
        "instagram": ("instagram.svg", "instagram-dark.svg"),
        "linkedin": ("linkedin.svg", "linkedin-dark.svg"),
        "rss": ("rss.svg", "rss-dark.svg"),
        "twitter": ("twitter.svg", "twitter-dark.svg"),
        "youtube": ("youtube.svg", "youtube-dark.svg"),
        "threads": ("threads.svg", "threads-dark.svg"),
        "twitch": ("twitch.svg", "twitch-dark.svg")
    }

    socials_list = []
    for platform in enabled_socials:
        url = socials_map.get(platform)
        if not url:
            continue
        icons = icon_mapping.get(platform, (f"{platform}.svg", f"{platform}-dark.svg"))
        light_icon = icons[0]
        dark_icon = icons[1]

        item_html = (
            f' <a href="{url}" target="_blank" rel="noreferrer"> <picture> '
            f'<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/{dark_icon}" /> '
            f'<source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/{light_icon}" /> '
            f'<img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/{light_icon}" width="32" height="32" /> '
            f'</picture> </a>'
        )
        socials_list.append(item_html)
    
    socials_html += "".join(socials_list) + "</p>\n\n"

    # Render Reach Me section
    reach_me_html = "### 📫 How to reach me:\n"
    reach_me_map = config.get("reach_me", {})
    for platform, url in reach_me_map.items():
        # calculate spacing
        padding = 10 - len(platform)
        if padding < 1:
            padding = 1
        reach_me_html += f"  - {platform}{' ' * padding}: <{url}>\n"

    # Read the base template file
    template_path = "README.gtpl.template"
    if not os.path.exists(template_path):
        # If it doesn't exist, we will write a generic template contents to generate README.gtpl
        print("README.gtpl.template not found!")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Perform substitutions
    rendered = template_content.replace("{{HEADER_IMAGE}}", header_html)
    rendered = rendered.replace("{{TWITCH_BADGE}}", twitch_badge)
    rendered = rendered.replace("{{SOCIALS}}", socials_html)
    rendered = rendered.replace("{{REACH_ME}}", reach_me_html)
    rendered = rendered.replace("{{GITHUB_USERNAME}}", github_user)

    with open("README.gtpl", "w", encoding="utf-8") as f:
        f.write(rendered)
    print("README.gtpl updated successfully.")

if __name__ == "__main__":
    main()
