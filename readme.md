# Your old buddy, Snake, slithering through your terminal! (WIP)
## Player Section
### Key Features:
1. **It's Fun!** Why not play a game of Snake while compiling code inside your terminal?
2. **Cross-Platform:** Works seamlessly on any operating system and terminal thanks to [Textual](https://textual.textualize.io/).
3. **Vim Lover Support:** Move your snake with WASD, arrow keys, or HJKL.
4. **Pretty Snakes:** Choose from a palette of 20 colors for your snake’s body.
5. **Game Controller Support (Experimental):** Play Snake using the arrows on your game controller.
6. **Local Multiplayer (Coming Soon):** Play Snake on your couch with a buddy—team up or compete.
7. **LAN Party (Coming Soon):** I see, you are a pro player... No need to share your PC with filthy casuals!

### Needed Tools
#### For Windows:
1. **Python Installation:**
    -  If you don’t have it installed, download Python from the official [website](https://www.python.org/downloads/).
    - During installation, make sure to check the checkbox that says **“Add Python to PATH”**.
2. **Install `Scoop`:**
    - Scoop is a command-line installer for Windows. If you don’t have it installed, follow the instructions on the
      Scoop official [website](https://scoop.sh).
3. **Install `pipx`:**
```bash
scoop install pipx
pipx ensurepath
```

#### For macOS:
1. **Install `Homebrew`:**
    - Homebrew is a package manager for macOS. If you don’t have it installed, follow the instructions on the
      Homebrew official [website](https://brew.sh/).
2. **Install `pipx`:**
```bash
brew install pipx
pipx ensurepath
```

#### For Linux:
1. **Install `pipx`:**
    - Install pipx using your package [manager](https://github.com/pypa/pipx?tab=readme-ov-file#on-linux).

### FocusTUI Installation (every OS)
Once you have `pipx` installed, you can easily install `tui-snake`:

1. **Install `tui-snake`:**
```bash
pipx install tui-snake
```

### Run the App
After installation, you can start `tui-snake` by typing:
```bash
tuisnake
```
## Dev Section

This is my experimental repo where I break a few rules and test different approaches.

### Guidelines & Rationale:

1. **The entire app is built inside one file** (.tcss does not count).
   > I used to split code into many modules. Then, I saw [msgspec](https://github.com/jcrist/msgspec/blob/main/msgspec/_core.c), a single file with 20K lines.
   > I wondered: is this a good practice? Is maintaining such a codebase difficult?

2. **No unit tests unless absolutely necessary.**
   > Unit tests create tons of dead code. Instead, let’s focus on writing more features.
   > The app should work as a whole, not just individual procedures. A holistic view of the system is preferred.

3. **No code comments unless the code is tricky or unreadable at first glance.**
   > The API should be logical and easy to use. If I need comments, I should simplify the code instead.

4. **No linters.**
   > I want to develop my own coding style by reviewing the code myself, not following linters’ orders.

5. **Code should be "static" – no type mixing.**
   > Static typing has its benefits. Mixing types makes the code harder to work with.

6. **Big procedures.**
   > Splitting one big procedure into many smaller ones makes navigation harder and increases the call stack.
