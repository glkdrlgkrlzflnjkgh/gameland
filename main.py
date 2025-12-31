# -------------------------------
# Gameland Game Engine
# Licensed under MIT License
# See LICENSE for details.
# Or go to https://opensource.org/licenses/MIT
# Created by glkdrlgkrlzflnjkgh and contributors.
# -------------------------------


import os
import sys
import time
import json

import pygame  # pygame-ce
from lupa import LuaRuntime


# -------------------------------
# Global config
# -------------------------------

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (20, 20, 20)
TARGET_FPS = 60

GAMES_DIR = os.path.join(
    os.path.expanduser("~"),
    "AppData",
    "Roaming",
    "Gameland",
    "games",
)


# -------------------------------
# Entity system
# -------------------------------

class Entity:
    def __init__(self, name, x, y, w, h, color):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.vx = 0.0
        self.vy = 0.0
        self.color = color

    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface):
        rect = pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))
        pygame.draw.rect(surface, self.color, rect)


# -------------------------------
# Game API exposed to Lua
# -------------------------------

class GameAPI:
    """
    What Lua sees as `api` and calls like:
      api:Log("text")
      api:SpawnEntity(...)
      api:SetVelocity(...)
      api:IsKeyDown("left")
    """ # so yeah, use colon syntax in Lua. OR DIE!!!!

    def __init__(self, engine):
        self.engine = engine

    def Log(self, msg):
        print(f"[LUA] {msg}")

    def SpawnEntity(self, name, x, y, w, h, r, g, b):
        self.engine.spawn_entity(
            str(name),
            float(x),
            float(y),
            float(w),
            float(h),
            int(r),
            int(g),
            int(b),
        )

    def SetVelocity(self, name, vx, vy):
        self.engine.set_velocity(str(name), float(vx), float(vy))

    def IsKeyDown(self, key):
        return self.engine.is_key_down(str(key))
    def GetPosition(self, name):
        ent = self.engine.entities.get(name)
        if ent is None:
            return None, None
        return ent.x, ent.y
    def SetPosition(self, name, x, y):
        ent = self.engine.entities.get(name)
        if ent is not None:
            ent.x = float(x)
            ent.y = float(y)
        
    def SetTargetFPS(self, fps):
        global TARGET_FPS
        TARGET_FPS = int(fps)
    def SetBackgroundColor(self, r, g, b):
        global BACKGROUND_COLOR
        BACKGROUND_COLOR = (int(r), int(g), int(b))
    def GetScreenSize(self):
        return SCREEN_WIDTH, SCREEN_HEIGHT


# -------------------------------
# Lua script host
# -------------------------------

class LuaScript:
    def __init__(self, engine, script_path: str):
        self.engine = engine
        self.script_path = script_path

        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.globals = self.lua.globals()
        game_dir = engine.game_folder.replace("\\", "/")
        print(f"[ENGINE] Setting Lua package.path to include: {game_dir}/?.lua")  
        self.lua.execute(f"""
            package.path = package.path .. ";{game_dir}/?.lua"
        """)
     
        # Expose API
        print("[ENGINE] Exposing GameAPI to Lua script")
        self.globals.api = GameAPI(engine)

        self.on_init = None
        self.on_update = None
        self.on_event = None
        print("[ENGINE] Loading Lua script:", script_path)
        self._load_script()

    def _load_script(self):
        if not os.path.exists(self.script_path):
            print(f"[FATAL] Lua script not found: {self.script_path}")
            sys.exit(1)

        with open(self.script_path, "r", encoding="utf-8") as f:
            print("[ENGINE] Reading Lua script...")
            code = f.read()

        # Execute Lua script so it defines global functions like OnInit/Update/OnEvent
        self.lua.execute(code)

        # Correct way to read globals from Lupa: attribute access
        print("[ENGINE] Retrieving Lua callback functions...")
        self.on_init = self.globals.OnInit
        print(f"[ENGINE] on_init: {self.on_init}")
        self.on_update = self.globals.Update
        print(f"[ENGINE] on_update: {self.on_update}")
        self.on_event = self.globals.OnEvent
        print(f"[ENGINE] on_event: {self.on_event}")

    def call_on_init(self):
        if self.on_init is not None:
            try:
                self.on_init(self.globals.api)
            except Exception as e:
                print(f"[ENGINE] Exception in Lua OnInit: {e}")

    def call_update(self, dt: float):
        if self.on_update is not None:
            try:
                self.on_update(self.globals.api, dt)
            except Exception as e:
                print(f"[ENGINE] Exception in Lua Update: {e}")
                

    def call_event(self, event_type: str, data: dict | None):
        if self.on_event is not None:
            try:
                lua_data = self.lua.table(**(data or {}))
                self.on_event(self.globals.api, event_type, lua_data)
            except Exception as e:
                print(f"[ENGINE] Exception in Lua OnEvent: {e}")


# -------------------------------
# Engine core
# -------------------------------

class Engine:
    def __init__(self, game_folder: str, game_info: dict):
        self.game_folder = game_folder
        self.game_info = game_info
        print(f"[ENGINE] Initializing engine for game: {self.game_info.get('name', 'Unknown')}")
        # Pygame setup
        pygame.init()
        pygame.display.set_caption(self.game_info.get("name", "Gameland Lua Engine"))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # World
        self.entities: dict[str, Entity] = {}

        # Input
        self.keys_down: set[str] = set()

        # Lua script
        
        script_path = os.path.join(self.game_folder, "game.lua")
        self.script = LuaScript(self, script_path)

    # -------- Entities --------

    def spawn_entity(self, name, x, y, w, h, r, g, b):
        ent = Entity(name, x, y, w, h, (r, g, b))
        self.entities[name] = ent
        print(f"[ENGINE] Spawned entity '{name}' at ({x}, {y})")

    def set_velocity(self, name, vx, vy):
        ent = self.entities.get(name)
        if ent is not None:
            ent.vx = vx
            ent.vy = vy

    def update_entities(self, dt):
        for ent in self.entities.values():
            ent.update(dt)

    def draw_entities(self):
        for ent in self.entities.values():
            ent.draw(self.screen)

    # -------- Input --------

    def is_key_down(self, key: str) -> bool:
        return key.lower() in self.keys_down

    def _update_keys_from_events(self, events):
        self.keys_down.clear()
        pressed = pygame.key.get_pressed()

        key_map = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "w": pygame.K_w,
            "a": pygame.K_a,
            "s": pygame.K_s,
            "d": pygame.K_d,
            "space": pygame.K_SPACE,
            "escape": pygame.K_ESCAPE,
            "tab": pygame.K_TAB,
            "enter": pygame.K_RETURN,
            "shift": pygame.K_LSHIFT,
            "ctrl": pygame.K_LCTRL,
            "alt": pygame.K_LALT,
            
        }

        for name, keycode in key_map.items():
            if pressed[keycode]:
                self.keys_down.add(name)

    # -------- Events to Lua --------

    def _send_key_event_to_lua(self, event):
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            self.script.call_event("keyDown", {"key": key_name})
        elif event.type == pygame.KEYUP:
            key_name = pygame.key.name(event.key)
            self.script.call_event("keyUp", {"key": key_name})

    # -------- Main loop --------

    def run(self):
        self.script.call_on_init()

        running = True
        last_time = time.time()

        while running:
            now = time.time()
            dt = now - last_time
            last_time = now

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    self._send_key_event_to_lua(event)

            self._update_keys_from_events(events)

            self.script.call_update(float(dt))
            self.update_entities(float(dt))

            self.screen.fill(BACKGROUND_COLOR)
            self.draw_entities()
            pygame.display.flip()

            self.clock.tick(TARGET_FPS)

        pygame.quit()


# -------------------------------
# Game discovery and launcher
# -------------------------------

def find_games():
    games = []

    if not os.path.exists(GAMES_DIR):
        os.makedirs(GAMES_DIR, exist_ok=True)

    for folder in os.listdir(GAMES_DIR):
        folder_path = os.path.join(GAMES_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        info_path = os.path.join(folder_path, "info.json")
        lua_path = os.path.join(folder_path, "game.lua")

        if not (os.path.exists(info_path) and os.path.exists(lua_path)):
            continue

        try:
            with open(info_path, "r", encoding="utf-8") as f:
                info = json.load(f)
        except Exception:
            continue

        game_name = info.get("name", folder)

        games.append({
            "name": game_name,
            "folder": folder_path,
            "lua": lua_path,
            "info": info,
        })

    return games


def game_select_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gameland – Select a Game")
    font_title = pygame.font.SysFont("Arial", 40)
    font_item = pygame.font.SysFont("Arial", 28)

    games = find_games()

    if not games:
        # No games installed → show a friendly message
        while True:
            screen.fill((30, 30, 30))

            t1 = font_title.render("No games installed", True, (255, 255, 255))
            t2 = font_item.render("Place a game folder in:", True, (200, 200, 200))
            t3 = font_item.render(GAMES_DIR, True, (200, 200, 200))
            t4 = font_item.render("Press ESC to quit", True, (255, 255, 0))

            screen.blit(t1, (230, 150))
            screen.blit(t2, (120, 250))
            screen.blit(t3, (120, 290))
            screen.blit(t4, (120, 400))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

        # unreachable, but keeps structure clean

    # Normal game selection menu
    selected = 0

    while True:
        screen.fill((30, 30, 30))

        title_surf = font_title.render("Select a Game", True, (255, 255, 255))
        screen.blit(title_surf, (260, 60))

        for i, game in enumerate(games):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            text_surf = font_item.render(game["name"], True, color)
            screen.blit(text_surf, (200, 160 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(games)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(games)
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    return games[selected]


# -------------------------------
# Entry point
# -------------------------------

def main():
    selected_game = game_select_menu()
    print(f"[ENGINE] Launching: {selected_game['name']}")
    engine = Engine(selected_game["folder"], selected_game["info"])
    engine.run()


if __name__ == "__main__":
    main()