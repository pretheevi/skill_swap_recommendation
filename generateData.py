import os
import uuid
import random
import requests
import bcrypt
import libsql_experimental as libsql
from dotenv import load_dotenv
from faker import Faker
from datetime import datetime, timedelta

load_dotenv()

fake = Faker()

TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

CATEGORIES = {
    "coding": {
        "unsplash_query": "coding programming laptop",
        "descriptions": [
            "Just built a REST API from scratch using Node.js 🚀",
            "Learning TypeScript — types actually save so much time",
            "My first fullstack project is live! React + Express + SQLite",
            "Debugging at 2am hits different 😅 finally fixed it",
            "Clean code is not a luxury, it's a habit",
            "Built a CLI tool that automates my daily workflow",
            "Understanding closures in JavaScript finally clicked for me",
            "Docker makes deployments so much smoother",
            "Recursion makes sense once you stop trying to trace it manually",
            "My VSCode setup after 2 years of tweaking 👨‍💻",
            "Finally understanding how async/await works under the hood",
            "Built my first Chrome extension — here's how",
            "WebSockets are simpler than I thought",
            "Learned Git rebasing properly. Game changer.",
            "My first open source contribution got merged! 🎉",
        ],
    },
    "design": {
        "unsplash_query": "ui ux design creative workspace",
        "descriptions": [
            "Redesigned my portfolio — less is more 🎨",
            "Color theory is underrated. Here's what I learned",
            "Typography can make or break a design",
            "Created a full design system for a client project",
            "Figma auto-layout changed how I think about components",
            "My process for designing mobile-first interfaces",
            "Dark mode UI — contrast ratios matter more than you think",
            "Brand identity project I've been working on for weeks",
            "Micro-interactions make apps feel alive ✨",
            "How I went from Photoshop to Figma and never looked back",
            "Accessibility in design is not optional",
            "Motion design principles I use every day",
            "Wireframing before designing saves so much time",
            "Icon design — consistency is everything",
            "Landing page teardown — what works and what doesn't",
        ],
    },
    "photography": {
        "unsplash_query": "photography camera portrait nature",
        "descriptions": [
            "Golden hour never disappoints 🌅",
            "Street photography — finding beauty in ordinary moments",
            "Manual mode only. Auto is for quitters 📷",
            "Shot this with a 50mm f/1.8 — bokeh is everything",
            "Long exposure photography at midnight",
            "Composition rule of thirds — a visual breakdown",
            "Editing workflow in Lightroom that saved me hours",
            "Film photography still hits different in 2024",
            "Behind the scenes of my latest portrait session",
            "Chasing light — my photography philosophy",
            "Macro photography is a whole different world",
            "Black and white photography — when to drop the color",
            "Shooting in RAW changed everything for me",
            "Drone photography tips for beginners",
            "Architecture photography — lines and geometry",
        ],
    },
    "music": {
        "unsplash_query": "music guitar piano studio",
        "descriptions": [
            "Finally nailed this fingerpicking pattern after weeks 🎸",
            "Produced my first beat entirely on FL Studio",
            "Music theory doesn't have to be boring — here's proof",
            "Busking in the city taught me more than any class",
            "How I practice scales without losing my mind",
            "My home recording setup on a budget 🎙️",
            "Jazz chords that will make your progressions interesting",
            "Wrote my first original song — lyrics are hard",
            "Piano improvisation — trust your ears more than theory",
            "The art of mixing — EQ and compression basics",
            "Learning to read sheet music at 24",
            "Bass guitar is criminally underrated",
            "Lo-fi beat making process from scratch",
            "How I memorized 10 songs in one month",
            "Vocal warm-up routine I do every morning",
        ],
    },
    "fitness": {
        "unsplash_query": "fitness gym workout training",
        "descriptions": [
            "6 months of consistent training — here's what changed 💪",
            "Morning workout routine that takes only 30 minutes",
            "Calisthenics > gym machines for functional strength",
            "Nutrition is 70% of the work. Let's talk macros",
            "My progressive overload plan for natural gains",
            "Rest days are not lazy days — recovery matters",
            "Form over weight. Always. 🏋️",
            "Running 5k every day for a month — what happened",
            "Mobility work I wish I started sooner",
            "Home workout that requires zero equipment",
            "Cold showers every morning for 30 days — results",
            "Meal prep Sunday is non-negotiable for me",
            "Yoga changed how I think about my body",
            "Jump rope is the most underrated cardio",
            "How sleep affects your gains more than training",
        ],
    },
    "cooking": {
        "unsplash_query": "cooking food recipe kitchen",
        "descriptions": [
            "Homemade pasta from scratch — it's easier than you think 🍝",
            "Knife skills that will change how you cook",
            "One pan meals for busy weeknights",
            "Fermentation journey — making my own kimchi",
            "The science behind caramelization 🧑‍🍳",
            "Budget meal prep for the entire week under $30",
            "Sourdough starter day 7 — it's alive!",
            "Street food inspired dishes from my travels",
            "Plant-based cooking without missing the flavor",
            "Why mise en place will make you a better cook",
            "How to make restaurant-quality ramen at home",
            "Spice blends I make from scratch",
            "Baking bread is therapy. Here's my recipe.",
            "5 sauces that go with everything",
            "Cooking with seasonal ingredients — a beginner guide",
        ],
    },
    "art": {
        "unsplash_query": "art painting drawing illustration",
        "descriptions": [
            "Watercolor practice — loose and expressive 🎨",
            "Sketchbook tour — 3 months of daily drawing",
            "Digital illustration process from sketch to final",
            "Learning perspective drawing the hard way",
            "Portrait study in charcoal — capturing emotion",
            "Abstract art — no rules, just expression",
            "Procreate brush settings I always use",
            "Color mixing fundamentals every artist should know",
            "Inktober 2024 — my favorite pieces this year",
            "How gesture drawing improved my art in 30 days",
            "Linocut printmaking — my first attempt",
            "Oil painting vs acrylic — which suits you?",
            "Anatomy studies that leveled up my figure drawing",
            "Creating a zine from scratch",
            "Fan art vs original art — my thoughts",
        ],
    },
    "writing": {
        "unsplash_query": "writing journal notebook pen",
        "descriptions": [
            "Published my first blog post — here's what I learned ✍️",
            "Writing every day for 60 days changed my thinking",
            "How I outline a story before writing a single word",
            "Copywriting tips that actually convert",
            "Journaling is the best therapy I've found",
            "My reading and writing routine in the morning",
            "How I wrote a short story in a weekend",
            "Poetry is not pretentious — here's why I love it",
            "Technical writing is a skill nobody talks about",
            "How to write a cold email that gets a reply",
            "World building for fiction writers — where to start",
            "Essay writing framework I use for everything",
            "Writing prompts that actually got me unstuck",
            "My editing process — kill your darlings",
            "Note-taking system that changed how I learn",
        ],
    },
    "language": {
        "unsplash_query": "language learning books study",
        "descriptions": [
            "Learning Japanese from zero — 6 month update 🇯🇵",
            "How I learned 1000 Spanish words in 3 months",
            "Immersion learning actually works — here's my method",
            "Why I stopped using Duolingo and what I do instead",
            "Speaking your first sentence in a new language",
            "Language exchange partners changed everything for me",
            "How to think in another language",
            "Korean is not as hard as people say",
            "My Anki deck setup for vocabulary retention",
            "Watching TV shows to learn French — does it work?",
            "Learning Arabic script — tips for beginners",
            "The best free resources for learning any language",
            "How accent reduction actually works",
            "Italian for travelers — the phrases that matter",
            "How I stay consistent with language learning",
        ],
    },
    "finance": {
        "unsplash_query": "finance money investing budget",
        "descriptions": [
            "How I paid off my student loan in 2 years 💰",
            "Index funds explained simply — just buy and hold",
            "Budgeting method that finally worked for me",
            "Emergency fund first — here's why it matters",
            "Understanding compound interest changed how I save",
            "My first year investing — what I learned",
            "Side income streams I built while working full time",
            "Frugal living tips that don't feel like sacrifice",
            "How to negotiate a salary increase",
            "Passive income is real but it takes work first",
            "Financial independence — what it means to me",
            "Credit score explained — and how to improve yours",
            "How I track every rupee I spend",
            "Tax saving investments every young person should know",
            "Why I started investing at 22",
        ],
    },
    "productivity": {
        "unsplash_query": "productivity desk workspace minimal",
        "descriptions": [
            "Second brain setup in Notion that changed my life 🧠",
            "Time blocking is the only productivity system I trust",
            "Deep work — how to focus for 4 hours straight",
            "My morning routine that sets the tone for the day",
            "Digital minimalism — deleted 30 apps, here's what happened",
            "How I read 20 books a year without rushing",
            "Pomodoro technique — how I actually use it",
            "Getting Things Done — a simplified breakdown",
            "Weekly review habit that keeps me on track",
            "How I cut my screen time in half",
            "The power of saying no — protecting your time",
            "Inbox zero is possible. Here's how.",
            "Building habits that stick — the science behind it",
            "Note-taking system for learning faster",
            "Why I wake up at 5am and what I do",
        ],
    },
    "travel": {
        "unsplash_query": "travel adventure landscape journey",
        "descriptions": [
            "Solo travel changed how I see myself 🌍",
            "Budget backpacking across Southeast Asia — full breakdown",
            "How I travel full time while working remotely",
            "Packing light — everything I need in a 20L bag",
            "Hidden gems in South India most people skip",
            "How to plan a trip in 24 hours",
            "Travel photography tips from a non-photographer",
            "Digital nomad lifestyle — the honest truth",
            "Cultural experiences you can't get from Google",
            "How I saved for a year to travel for 3 months",
            "Train travel in Europe — the complete guide",
            "Slow travel vs fast travel — what I prefer",
            "Street food adventures — the best meals I've had",
            "How to meet locals and not just other tourists",
            "My travel journaling habit and why it matters",
        ],
    },
}


# ─── helpers ──────────────────────────────────────────────────────────────────

def fetch_images(query, count=30):
    print(f"  Fetching {count} images for '{query}'...")
    try:
        url = f"https://api.unsplash.com/photos/random?query={query}&count={count}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url, timeout=10)
        photos = response.json()
        if isinstance(photos, list):
            return [photo["urls"]["regular"] for photo in photos]
        print(f"  Unsplash error: {photos.get('errors', 'unknown')}")
        return []
    except Exception as e:
        print(f"  Failed: {e}")
        return []

def fetch_avatar_urls(count=80):
    print(f"  Fetching {count} avatars...")
    try:
        url = f"https://api.unsplash.com/photos/random?query=person portrait face&count={count}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url, timeout=10)
        photos = response.json()
        if isinstance(photos, list):
            return [photo["urls"]["small"] for photo in photos]
        return []
    except Exception as e:
        print(f"  Failed: {e}")
        return []

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def random_date(start_days_ago=180, end_days_ago=1):
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    return start + (end - start) * random.random()

def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def execute(conn, sql, args=()):
    conn.execute(sql, args)

def executemany(conn, sql, data):
    for args in data:
        conn.execute(sql, args)


# ─── main ─────────────────────────────────────────────────────────────────────

def generate():
    conn = libsql.connect("skill-swap", uri=TURSO_URL, auth_token=TURSO_TOKEN)

    # ── 1. fetch images ───────────────────────────────────────────────────────
    print("\n[1/6] Fetching images from Unsplash...")
    image_pool = {}
    for category, data in CATEGORIES.items():
        urls = fetch_images(data["unsplash_query"], count=30)
        image_pool[category] = urls
        print(f"  {category}: {len(urls)} images")

    avatar_pool = fetch_avatar_urls(count=80)
    print(f"  avatars: {len(avatar_pool)}")

    # ── 2. users ──────────────────────────────────────────────────────────────
    print("\n[2/6] Creating users...")
    NUM_USERS = 80
    users = []
    hashed_pw = hash_password("password123")

    for i in range(NUM_USERS):
        category = random.choice(list(CATEGORIES.keys()))
        user_id = str(uuid.uuid4())
        name = fake.unique.user_name()
        email = fake.unique.email()
        avatar = avatar_pool[i % len(avatar_pool)] if avatar_pool else ""
        bio = fake.sentence(nb_words=10)
        created = fmt(random_date(180, 30))

        users.append({"id": user_id, "name": name, "email": email, "category": category})

        execute(conn,
            "INSERT OR IGNORE INTO User (id, name, email, password, avatar, bio, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, name, email, hashed_pw, avatar, bio, created, created)
        )

    conn.commit()
    print(f"  Created {NUM_USERS} users")

    # ── 3. skills ─────────────────────────────────────────────────────────────
    print("\n[3/6] Creating skills...")
    skills = []

    for user in users:
        category = user["category"]
        descriptions = CATEGORIES[category]["descriptions"]
        images = image_pool.get(category, [])

        for _ in range(random.randint(5, 10)):
            skill_id = str(uuid.uuid4())
            description = random.choice(descriptions)
            ratio = random.choice(["1:1", "2:3"])
            created = fmt(random_date(120, 1))

            skills.append({"id": skill_id, "user_id": user["id"], "category": category, "images": images})

            execute(conn,
                "INSERT OR IGNORE INTO Skill (id, user_id, description, media_ratio, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (skill_id, user["id"], description, ratio, created, created)
            )

    conn.commit()
    print(f"  Created {len(skills)} skills")

    # ── 4. media ──────────────────────────────────────────────────────────────
    print("\n[4/6] Creating skill media...")
    media_count = 0

    for skill in skills:
        images = skill["images"]
        if not images:
            continue
        for _ in range(random.randint(1, 3)):
            media_id = str(uuid.uuid4())
            media_url = random.choice(images)
            created = fmt(random_date(120, 1))
            execute(conn,
                "INSERT OR IGNORE INTO SkillMedia (id, skill_id, media_type, media_url, created_at) VALUES (?, ?, 'image', ?, ?)",
                (media_id, skill["id"], media_url, created)
            )
            media_count += 1

    conn.commit()
    print(f"  Created {media_count} media entries")

    # ── 5. follows ────────────────────────────────────────────────────────────
    print("\n[5/6] Creating follows...")
    follow_count = 0

    for user in users:
        same_cat = [u for u in users if u["category"] == user["category"] and u["id"] != user["id"]]
        diff_cat = [u for u in users if u["category"] != user["category"]]
        pool = same_cat * 3 + diff_cat
        targets = random.sample(pool, min(random.randint(8, 20), len(pool)))

        for target in targets:
            created = fmt(random_date(120, 1))
            execute(conn,
                "INSERT OR IGNORE INTO user_follows (follower_id, following_id, created_at) VALUES (?, ?, ?)",
                (user["id"], target["id"], created)
            )
            follow_count += 1

    conn.commit()
    print(f"  Created {follow_count} follows")

    # ── 6. likes and comments ─────────────────────────────────────────────────
    print("\n[6/6] Creating likes, comments and comment likes...")
    user_ids = [u["id"] for u in users]
    like_count = 0
    comment_count = 0
    comment_like_count = 0

    comment_texts = [
        "This is so helpful, thanks for sharing!",
        "I've been trying to learn this too 🔥",
        "Amazing work! How long did this take?",
        "Saved this for later 👌",
        "This is exactly what I needed to see today",
        "Can you share more about your process?",
        "Underrated post, more people need to see this",
        "Goals 🙌",
        "Love the detail here",
        "Been struggling with this — super useful!",
        "More of this please 🙏",
        "You make this look so easy",
        "This gave me the motivation I needed today",
        "I tried this and it actually works!",
        "Following for more content like this",
        "The way you explained this is perfect",
        "Bookmarked. Coming back to this.",
        "Didn't expect to learn something new today but here we are",
        "This deserves way more attention",
        "Keep going, you're inspiring people 💪",
    ]

    for user in users:
        same_cat_skills = [s for s in skills if s["category"] == user["category"]]
        diff_cat_skills = [s for s in skills if s["category"] != user["category"]]
        pool = same_cat_skills * 3 + diff_cat_skills

        num_likes = random.randint(20, 50)
        liked = random.sample(pool, min(num_likes, len(pool)))

        for skill in liked:
            if skill["user_id"] == user["id"]:
                continue

            created = fmt(random_date(90, 1))
            execute(conn,
                "INSERT OR IGNORE INTO Skill_Likes (skill_id, user_id, created_at) VALUES (?, ?, ?)",
                (skill["id"], user["id"], created)
            )
            like_count += 1

            if random.random() < 0.5:
                comment_id = str(uuid.uuid4())
                text = random.choice(comment_texts)
                created = fmt(random_date(90, 1))
                execute(conn,
                    "INSERT OR IGNORE INTO Comment (id, skill_id, user_id, text, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (comment_id, skill["id"], user["id"], text, created, created)
                )
                comment_count += 1

                likers = random.sample(user_ids, random.randint(0, 10))
                for liker_id in likers:
                    execute(conn,
                        "INSERT OR IGNORE INTO Comment_Likes (comment_id, user_id, created_at) VALUES (?, ?, ?)",
                        (comment_id, liker_id, fmt(random_date(90, 1)))
                    )
                    comment_like_count += 1

    conn.commit()
    print(f"  Created {like_count} skill likes")
    print(f"  Created {comment_count} comments")
    print(f"  Created {comment_like_count} comment likes")

    print("\n✅ Done! Summary:")
    print(f"   Users:         {NUM_USERS}")
    print(f"   Skills:        {len(skills)}")
    print(f"   Media:         {media_count}")
    print(f"   Follows:       {follow_count}")
    print(f"   Skill likes:   {like_count}")
    print(f"   Comments:      {comment_count}")
    print(f"   Comment likes: {comment_like_count}")
    print(f"\n   All users password: password123")

if __name__ == "__main__":
    generate()