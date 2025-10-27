# 🗂️ DirTracker

**Author:** [PythonHubStudio / Oleksandr Tukas](https://github.com/PythonHubStudio)  
**Language:** Python 3.11+  
**License:** MIT  

---

### 📖 Description

**DirTracker** — This tool creates a "snapshot" of a directory (its full tree structure).
It detects any file changes since the last check, including:

- 🟢 files that were added;
- 🔴 files that were removed;
- 🟡 files whose contents have changed, even by one byte.

For each directory you monitor, a snapshot file (.snapshot.pkl) is created in the directory itself.

---
### Note! The first run only does a check (first snapshot), like init.

### 🧩 Output Example

**With full absolute paths (if `os.walk()` was run from an absolute path):**
```

[+] New file: /home/user/course/app.py
[-] Removed file: /home/user/Documents/passport.pdf
[~] Changed file: /home/user/Documents/contacts.xlsx

```

**Or with relative paths (if `os.walk()` was run from "."):**
```

[+] New file: ./course/app.py
[-] Removed file: ./Documents/passport.pdf
[~] Changed file: ./Documents/contacts.xlsx

````

> 💡 If redirect stdout, ANSI colors will be off.

---

### ⚙️ Usage

```bash
python dtr.py [-h] [path]
````

**Arguments:**

* `path` — the path to the directory you want to monitor, if not passed it uses CWD
* `-h` — see help

**Examples:**

```bash
python dtr.py

python dtr.py /home/user/Documents
```
---
File with settings and ignored names of dirs and files in ./settings, see them.
---

### 🪟 Windows Notes

On Windows, ANSI colors are supported automatically (without using `colorama`).

---

### 🎓 Educational Use

Используется как **образовательный пример** в моем курсе:
Used as an **educational example** in my course:
👉 [Python Full Course on Udemy](https://www.udemy.com/course/python-full-course/?referralCode=317EA7AF0A1C4C2C733A)

---

### 📦 Repository Structure (simplified)

```
DirTracker/
├── dtr.py            # Entry point (CLI)
├── core/
│   ├── dirtracker.py
│   ├── ansi/
│   │   ├── fix.py          # Enables ANSI colors on Windows
│   │   └── colorize.py     # Cross-platform color formatting
│   └── settings/
│       ├── conf_reader.py        # Read the config file
│       └── excludes_reader.py    # Read the excludes names.
└── settings/
    ├── config.conf
    ├── excludes_dirs.conf
    └── excludes_files.conf
```

---

### 🧠 Key Features

* Detects added, removed, and changed files
* Stores snapshot in `.snapshot.pkl`
* Automatically disables colors for redirected output
* Works cross-platform (Linux, macOS, Windows)
* Simple CLI interface using `argparse`

---

### 🧾 License

This project is distributed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

```



