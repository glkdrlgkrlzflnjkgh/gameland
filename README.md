🎮 Gameland
A lightweight 2D game engine written in Python with LuaJIT scripting.
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


This will load your Lua script and begin the game loop.

🧪 Example Script
Here’s a minimal example of a Gameland Lua script:
function OnInit(api)
    api:Log("Game started!")
    api:SpawnEntity("player")
end

function Update(api, dt)
    if api:IsKeyDown("right") then
        api:SetVelocity("player", 100, 0)
    end
end


Place your script where the engine expects it (see main.py for details).

📁 Project Structure
gameland/
│
├── main.py          # Engine core
├── Pipfile          # Dependencies
├── Pipfile.lock
└── LICENSE          # MIT License


More structure will be added as the engine grows.

🤝 Contributing
Gameland is experimental, but contributions, ideas, and feedback are welcome.
Feel free to open issues or submit pull requests.
All commits should be signed off using:
git commit -s -m "message"



📄 License
Gameland is under the MIT license, see LICENSE file for more!
Gameland is released under the MIT License.
See the LICENSE file for details
