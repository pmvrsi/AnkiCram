<div align="center">

<img src="https://cdn.hackclub.com/019c4d49-71ff-7533-af81-41a9611a58b0/logo1.png" alt="AnkiCram" width="160" />

**Anki addon for cramming your decks**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/ankicram/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Anki](https://img.shields.io/badge/anki-2.1+-blue.svg)](https://apps.ankiweb.net/)

[**Features**](#-features) • [**Installation**](#-installation) • [**Usage**](#-usage) • [**Compatibility**](#-compatibility)

https://github.com/user-attachments/assets/b0c26616-da85-4430-9dc0-7f65837e1ace

</div>

---

## 🎯 Overview
**AnkiCram** is an Anki add-on that lets you loop and rebuild decks infinitely without ruining your long-term spaced repetition data. It uses filtered decks behind the scenes so your main scheduling remains untouched.

**Perfect for:**
* 📚 Last-minute exam preparation
* 🔄 Intensive review sessions
* 🎯 Focused studying on specific decks
* 📊 Tracking your cramming progress

---

## ✨ Features

### 🚀 Core Features
* **Infinite Loop Mode**: Failed cards instantly return to the queue for immediate retry.
* **Smart Deck Selection**: Search and select from all your decks with an intuitive interface.
* **Tag Filtering**: Focus on specific cards by filtering with tags.
* **Session Statistics**: Real-time tracking of:
  * ⏱️ Session duration
  * ✅ Cards reviewed
  * 🧠 Retention rate
  * 🔄 Failed cards count

---

## 📥 Installation

### Method 1: AnkiWeb (Recommended)
1. Open Anki.
2. Go to `Tools` → `Add-ons` → `Get Add-ons...`.
3. Enter the add-on code: `123859453`
4. Restart Anki.

### Method 2: Manual Installation
1. Download the latest release from [**Releases**](https://github.com/yourusername/ankicram/releases).
2. Open Anki.
3. Go to `Tools` → `Add-ons` → `View Files`.
4. Extract the downloaded ZIP into the `addons21` folder.
5. Restart Anki.

---

## 🎮 Usage

### Starting a Cram Session
1. **Launch AnkiCram**: Click `Tools` → `AnkiCram` in the menu bar.
2. **Select Your Deck**: Browse or search for the deck you want to cram. The selected deck will be highlighted in purple.
3. **Configure Options**:
    * **Infinite Loop**: Enable to retry failed cards immediately.
    * **Keep deck after session**: Preserve the cram deck when you finish.
    * **Tag Filter**: Enter tags to focus on specific cards (comma-separated).
4. **Start Cramming**: Click **"Start Cram Session"**. A filtered deck named `AnkiCram - [Your Deck]` will be created.

### During Your Session
* **Corner Widget**: A floating widget appears in the bottom-left. Click it to:
    * View live session statistics.
    * Access **Rebuild** (to do the deck again).
    * **Stop** the session.
* **Stats Tracker**: Monitor your time elapsed, cards reviewed, and retention percentage in real-time.

### Ending Your Session
1. Click the corner widget.
2. Click **"End Session"**.

---

## 🔧 Compatibility

* ✅ Anki 2.1.50+
* ✅ Qt6 (Anki 2.1.55+)
* ✅ Windows, macOS, Linux
* ✅ All deck types

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
