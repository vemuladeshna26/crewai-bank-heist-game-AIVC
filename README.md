## 🧠 CrewAI Architecture — How the Game Is Built

This project follows a **configuration-driven multi-agent architecture** powered by **crewAI**.  
Rather than hardcoding behavior, the entire game-generation workflow is defined through **YAML configuration files** and a **base HTML template**, allowing multiple AI agents to collaborate on building a complete game.

At a high level, the system answers three questions:

- **What should the game be?** → defined in `gamedesign.yaml`
- **Who is responsible for building each part?** → defined in `agents.yaml`
- **In what order should the work happen?** → defined in `tasks.yaml`

The final output is assembled into a playable HTML game using a shared template.

---

### 📄 Core Inputs to the Crew

#### `gamedesign.yaml` — Game Mechanics Specification
This file describes the **high-level game idea and mechanics**, including:
- The overall theme and objective of the bank heist game
- Core entities (player, guards, cards, win/lose conditions)
- Design constraints that guide all agents

Agents use this file as the **single source of truth** for gameplay intent, ensuring consistency across UI, logic, and interactions.

---

#### `gameTemplate.html` — Base Game Template
This file defines the **structural skeleton** of the game page:
- The overall HTML layout
- Placeholder markers for injected UI, logic, and assets
- A consistent structure that all agents must conform to

By generating code *into* a fixed template, the system guarantees that the final output is deployable as a standalone HTML file.

---

#### `agents.yaml` — Agent Definitions
This file defines **who participates in the crew**.

Each agent has:
- A clear role (UI, logic, input handling, assets, integration, QA)
- A focused responsibility
- A constrained scope of generation

This specialization allows the system to break a complex task (building a game) into manageable, coordinated parts.

---

#### `tasks.yaml` — Task Orchestration
This file defines **how the crew operates**:
- Which agent runs which task
- The execution order of tasks
- How outputs from one agent feed into the next

Together with `agents.yaml`, this file acts as the **execution blueprint** for the entire pipeline.

---

## 🔁 End-to-End Workflow

When the crew runs, the system follows this flow:

1. Load game rules and design intent from `gamedesign.yaml`
2. Initialize agents defined in `agents.yaml`
3. Execute tasks in the order defined by `tasks.yaml`
4. Generate UI, game logic, input handling, and assets independently
5. Inject all generated components into `gameTemplate.html`
6. Package everything into a single HTML game file
7. Perform basic validation before final output

This design makes the system **modular, extensible, and reusable** for other games or interactive applications.

---

## 🚀 Running the Project

### Prerequisites

- Python **>= 3.10 and < 3.13**
- `pip`
- OpenAI API key

---

### Step 1: Install uv

```bash
pip install uv
```

---

### Step 2: Install Project Dependencies

From the project root:

```bash
crewai install
```

This installs and locks all required dependencies.

---

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ Do not commit this file to version control.

---

### Step 4: Run the Project

To kickstart crew of AI agents and begin game generation, run:

```bash
crewai run
```

This command:
- Initializes the crew
- Executes all tasks defined in `tasks.yaml`
- Produces the final game output

---

## 🎮 Output

After execution, the system generates a **standalone HTML game file** (e.g., `output/game.html`).

Open this file in any modern web browser to play the **CrewAI Bank Heist Game** — no server required.

---

## 📄 License

Educational / experimental use.
