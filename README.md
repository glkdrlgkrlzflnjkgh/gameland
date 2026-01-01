<p align="center">
  <img src="https://static.wikia.nocookie.net/gameland/images/e/e0/Gameland_logo.png/revision/latest?cb=20251231205803" width="250">
</p>

🎮 Gameland
is a lightweight 2D game engine written in Python with LuaJIT scripting.
Gameland is a custom game engine built using Python, pygame‑ce, and LuaJIT (via Lupa).
It’s designed to be simple, fast to iterate on, and easy to script using Lua.
This project is currently in early development.

✨ Features
- 🐍 Python engine core using pygame‑ce
- 🔥 LuaJIT scripting through Lupa
- 🎮 Simple API for entities, input, logging, and game lifecycle
- 📦 Modular design — Lua require() works thanks to configured package.path
- 🧱 Basic entity management (spawn, move, velocity, etc.)
- ⌨️ Keyboard input with IsKeyDown()
- 🖥️ Configurable target FPS
- 📝 Clean, documented API on the Gameland Wiki

📚 Documentation
Full API reference is available on the wiki:
👉 https://gameland.fandom.com/wiki/API
Main wiki page:
👉 https://gameland.fandom.com/wiki/Gameland_Wiki

🚀 Getting Started
Requirements
- Python 3.10+
- pygame‑ce
- lupa (LuaJIT bindings)
- pipenv (optional, recommended)
Install dependencies
If you're using Pipenv (recommended):
pipenv install


Or using pip:
pip install pygame-ce lupa



🧩 Running Gameland
To start the engine:
python main.py


This will launch the game select menu where you can select the game you want to launch with the arrow keys, then press enter to launch the selected game! (it will prompt you to create/install a game if there are no games!)


Place your script where the engine expects it (see main.py for details).


🤝 Contributing
Gameland is experimental, but contributions, ideas, and feedback are welcome.
Feel free to open issues or submit pull requests.
All commits should be signed off using:
git commit -s -m "message"



📄 License
Gameland is under the MIT license, see LICENSE file for more!
Gameland is released under the MIT License.
See the LICENSE file for details
