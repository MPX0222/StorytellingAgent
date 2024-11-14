# Sharp School - Interactive Storytelling Game

## Setup

1. Clone the repository:
```
git clone https://github.com/MPX0222/StorytellingAgent.git
```

2. Create and activate a virtual environment:
```
conda create -n story_agent python=3.9
conda activate story_agent
```
Or using venv:
```
python -m venv story_agent
source story_agent/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your OpenAI API configuration:
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=your_openai_api_base
```

## Running the Game

Start the game by running:
```
python main.py
```