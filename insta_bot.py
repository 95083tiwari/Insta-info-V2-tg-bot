import instaloader
import json
from datetime import datetime

# Tere channel ka link – change mat karna
CHANNEL = "@lifeonbots"
CHANNEL_LINK = "https://t.me/lifeonbots"

L = instaloader.Instaloader()

# Thoda sa fast banane ke liye (sirf zaruri cheez download karega)
L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False
)

def fast_scrape(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)

        print("\n" + "═" * 60)
        print(f"   Username   : @{profile.username}")
        print(f"   Full Name  : {profile.full_name or 'Not set'}")
        print(f"   Followers  : {profile.followers:,}")
        print(f"   Following  : {profile.followees:,}")
        print(f"   Posts      : {profile.mediacount}")
        print(f"   Private    : {'Yes' if profile.is_private else 'No'}")
        print(f"   Verified   : {'Yes' if profile.is_verified else 'No'}")
        print(f"   Bio        : {profile.biography.replace(chr(10), ' ') if profile.biography else 'No bio'}")
        if profile.external_url:
            print(f"   Link       : {profile.external_url}")

        # Last 5 posts (fast mode mein bhi kaafi tezi se aayenge)
        print("\n   Recent 5 Posts:")
        count = 0
        for post in profile.get_posts():
            if count >= 5:
                break
            caption = (post.caption[:70] + "..." if post.caption and len(post.caption) > 70 else post.caption) if post.caption else "No caption"
            print(f"   {count+1}. {post.date_local.strftime('%d %b %Y')} | {post.likes:,} likes | {caption}")
            print(f"      https://instagram.com/p/{post.shortcode}")
            count += 1

        # JSON bhi save kar de silently
        data = {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "is_private": profile.is_private,
            "is_verified": profile.is_verified,
            "bio": profile.biography,
            "external_url": profile.external_url,
            "profile_pic": profile.profile_pic_url
        }
        with open(f"{username}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("═" * 60)
        print(f"   JSON saved → {username}.json")
        print("═" * 60)
        print(f"   Please Join Our Channel {CHANNEL}")
        print(f"   {CHANNEL_LINK}")
        print("═" * 60)

    except instaloader.exceptions.ProfileNotExistsException:
        print("   Profile nahi mila bhai! Username check kar")
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        print("   Private profile hai – sirf basic info mila")
    except Exception as e:
        print(f"   Error: {e}")

# Bot start hote hi yeh dikhega (Telegram style)
if __name__ == "__main__":
    print("\n" + "█" * 60)
    print("      INSTAGRAM PUBLIC PROFILE SCRAPER")
    print("            Made by @lifeonbots")
    print("█" * 60)
    print(f"\n   Please Join Our Channel {CHANNEL}")
    print(f"   {CHANNEL_LINK}\n")
    print("   Send Username:")
    print("   Example → the_aadarshtiwari  (bina @ ke)")
    print("█" * 60)

    while True:
        user = input("\n   Username daal: ").strip()
        if user.startswith("@"):
            user = user[1:]
        if user:
            fast_scrape(user)
        else:
            print("   Username to daal na bhai!")
