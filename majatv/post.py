import random
import re
from pathlib import Path

# ---------- Config ----------

TEMPLATES_FOLDER = Path("templates")

AFTER_TITLE_FILE = "after-title.txt"
PRE_TITLE_FILE = "pre-title.txt"
VS_FILE = "after-title.txt"
IMG_URL_FILE = "img-url.txt"

# NEW FILE
# Each line contains a filename keyword
# Example:
# demo
# review
# guide
# compare
FILENAME_WORDS_FILE = "filename-words.txt"

RESULTS_FOLDER = Path("results")

TOTAL_FILES = 150

USE_RANDOM_TEMPLATE = True

# Add random numbers to the LAST N files
LAST_RANDOM_FILES = 15

# ---------- Helpers ----------

def read_lines(file_path):
    """
    Read file and return non-empty stripped lines.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_file(file_path, content):
    """
    Write content to file.
    """
    file_path.write_text(content, encoding="utf-8")


def safe_filename(name):
    """
    Remove invalid filename characters.
    """
    return re.sub(r'[<>:"/\\|?*]', "_", name)


def choose_template(html_templates, index):
    """
    Choose template randomly or sequentially.
    """

    if USE_RANDOM_TEMPLATE:
        return random.choice(html_templates)

    return html_templates[index % len(html_templates)]


# ---------- Main ----------

def main():

    RESULTS_FOLDER.mkdir(exist_ok=True)

    # ---------- Load Templates ----------

    html_templates = sorted(TEMPLATES_FOLDER.glob("*.html"))

    if not html_templates:
        print("No HTML template files found.")
        return

    print(f"Loaded {len(html_templates)} HTML templates.")

    # ---------- Load Text Data ----------

    try:
        after_titles = read_lines(AFTER_TITLE_FILE)
        pre_titles = read_lines(PRE_TITLE_FILE)
        vs_lines = read_lines(VS_FILE)
        img_urls = read_lines(IMG_URL_FILE)

        # NEW
        filename_words = read_lines(FILENAME_WORDS_FILE)

    except FileNotFoundError as e:
        print(e)
        return

    # ---------- Validation ----------

    if not all([
        after_titles,
        pre_titles,
        vs_lines,
        img_urls,
        filename_words
    ]):
        print("One or more input files are empty.")
        return

    # ---------- Generate Files ----------

    for i in range(TOTAL_FILES):

        # Choose template
        template_path = choose_template(html_templates, i)

        # Read template
        html_template = template_path.read_text(encoding="utf-8")

        # Data selection
        after_title = after_titles[i % len(after_titles)]
        pre_title = pre_titles[i % len(pre_titles)]
        vs_text = vs_lines[i % len(vs_lines)]
        img_url = img_urls[i % len(img_urls)]

        # Random filename word
        filename_word = random.choice(filename_words)

        # ---------- Replace Placeholders ----------

        replacements = {
            "zbit-at": after_title,
            "zbit-l": f"lol3241{random.randint(1000, 9999)}",
            "zbit-pt": pre_title,
            "zbit-vs": vs_text,
            "zbit-iurl": img_url,
        }

        new_html = html_template

        for placeholder, value in replacements.items():
            new_html = new_html.replace(placeholder, value)

                # ---------- Create Filename ----------
        
        safe_vs = safe_filename(vs_text)
        safe_word = safe_filename(filename_word)
        
        # Base filename
        final_name = f"{safe_vs}-{safe_word}"
        
        # Add random numbers to EVERY filename
        random_number = random.randint(10000, 99999)
        final_name += f"-{random_number}"
        
        # Final filename
        filename = RESULTS_FOLDER / f"{final_name}.html"

        # ---------- Save File ----------

        write_file(filename, new_html)

        print(f"[{i + 1}/{TOTAL_FILES}] Generated: {filename.name}")

    print("\nAll files generated successfully.")


# ---------- Run ----------

if __name__ == "__main__":
    main()