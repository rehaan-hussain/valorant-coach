# Valorant AI Coach MVP

An AI-powered coaching system that analyzes Valorant gameplay streams and provides real-time tips to help casual gamers improve their skills and potentially reach high ranks.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 10/11, macOS, or Linux
- 8GB RAM minimum (16GB recommended)
- Valorant installed (for real gameplay analysis)

### Installation

1. **Clone or download the repository**
```bash
git clone <repository-url>
cd valorant-ai-coach
```

2. **Run the automated setup**
```bash
python setup.py
```

3. **Or install manually**
```bash
pip install -r requirements.txt
python test_installation.py
```

### Usage

1. **Test the installation**
```bash
python test_installation.py
```

2. **Run the demo (no Valorant required)**
```bash
python demo.py
```

3. **Start the main application**
```bash
python main.py
# or
python run_streamlit.py
```

4. **Open your browser**
Navigate to `http://localhost:8501`

## 🎮 Features

### 🎯 Real-time Gameplay Analysis
- **Screen Capture**: Captures gameplay footage for analysis
- **Computer Vision**: Detects players, enemies, crosshair position, and game events
- **Performance Metrics**: Tracks accuracy, reaction time, positioning, and game sense

### 🤖 AI Coaching Engine
- **Behavioral Analysis**: Identifies patterns in gameplay and decision-making
- **Skill Assessment**: Evaluates mechanical skills, game sense, and strategic thinking
- **Personalized Tips**: Provides context-aware coaching advice

### 📊 Performance Tracking
- **Statistics Dashboard**: Visualizes improvement over time
- **Skill Breakdown**: Detailed analysis of different aspects of gameplay
- **Progress Reports**: Weekly/monthly performance summaries

### 🎯 Coaching Interface
- **Real-time Feedback**: Instant tips during gameplay
- **Post-Game Analysis**: Comprehensive review of matches
- **Training Recommendations**: Suggested drills and practice routines

## 🏗️ Architecture

```
valorant-ai-coach/
├── src/
│   ├── capture/          # Screen capture and video processing
│   │   ├── screen_capture.py
│   │   └── frame_processor.py
│   ├── analysis/         # AI analysis engine
│   │   ├── game_analyzer.py
│   │   ├── skill_assessor.py
│   │   └── behavior_analyzer.py
│   ├── coaching/         # Coaching logic and tips
│   │   ├── coach.py
│   │   ├── tip_generator.py
│   │   └── training_planner.py
│   ├── ui/              # User interface components
│   │   ├── streamlit_app.py
│   │   ├── dashboard.py
│   │   └── coaching_interface.py
│   └── utils/           # Utility functions
│       ├── logger.py
│       └── config.py
├── config/              # Configuration files
├── models/              # Pre-trained AI models (future)
├── data/               # Training data and configurations
├── logs/               # Application logs
├── main.py             # Main application entry point
├── demo.py             # Demo script
├── setup.py            # Automated setup script
├── test_installation.py # Installation test
└── requirements.txt    # Python dependencies
```

## 🎯 How It Works

### 1. Screen Capture
The system captures your screen in real-time using the `mss` library, focusing on the area where Valorant is running.

### 2. Frame Analysis
Each captured frame is processed to detect:
- **Crosshair position** and movement patterns
- **Enemy players** using color detection
- **UI elements** like health bars and ammo counters
- **Movement patterns** using optical flow analysis

### 3. AI Analysis
The analysis engine evaluates:
- **Accuracy**: Based on crosshair placement and target acquisition
- **Crosshair Placement**: Consistency and positioning quality
- **Movement Efficiency**: How well you move and position yourself
- **Game Sense**: Decision making and awareness

### 4. Coaching Tips
Based on the analysis, the system provides:
- **Real-time feedback** during gameplay
- **Personalized advice** based on your skill level
- **Training recommendations** for improvement
- **Performance tracking** over time

## 📊 Performance Metrics

The system tracks several key metrics:

- **Accuracy**: How well you aim and hit targets
- **Crosshair Placement**: How consistently you keep your crosshair at head level
- **Movement Efficiency**: How well you move and position yourself
- **Game Sense**: Your decision making and awareness
- **Overall Score**: Combined performance rating

## 🎓 Coaching Categories

The system provides coaching in these areas:

1. **Crosshair Placement** (Priority: High)
   - Keep crosshair at head level
   - Pre-aim common angles
   - Practice in the Range

2. **Movement** (Priority: High)
   - Learn counter-strafing
   - Don't move while shooting
   - Practice efficient movement

3. **Positioning** (Priority: Medium)
   - Always have cover nearby
   - Don't expose yourself to multiple angles
   - Learn common positions

4. **Game Sense** (Priority: Medium)
   - Learn common timings
   - Improve communication
   - Watch professional matches

5. **Mechanics** (Priority: Medium)
   - Practice recoil control
   - Work on flicking and tracking
   - Use aim training maps

## ⚙️ Configuration

The system can be configured through `config/settings.json`:

```json
{
  "capture": {
    "default_fps": 30,
    "default_monitor": 1
  },
  "analysis": {
    "session_duration": 300,
    "accuracy_threshold": 0.7
  },
  "coaching": {
    "tip_cooldown": 5.0,
    "max_tips_per_session": 50
  }
}
```

## 🧪 Testing

### Run the Demo
The demo script shows the system's capabilities without requiring actual gameplay:

```bash
python demo.py
```

### Test Installation
Verify that everything is working correctly:

```bash
python test_installation.py
```

## 🚨 Important Notes

### Privacy & Security
- The system captures your screen to analyze gameplay
- No data is sent to external servers
- All analysis is performed locally on your machine
- You can stop recording at any time

### Performance Impact
- Screen capture uses minimal CPU resources
- Analysis is optimized for real-time performance
- Recommended FPS: 30 (can be adjusted in settings)

### Limitations (MVP)
- Basic computer vision detection (enemy detection may not be 100% accurate)
- Limited to visual analysis (no audio analysis)
- Requires Valorant to be visible on screen
- Some advanced features may need refinement

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   python test_installation.py
   ```

2. **Screen Capture Issues**
   - Ensure you have permission to capture screen
   - Try running as administrator (Windows)
   - Check if Valorant is in fullscreen mode

3. **Performance Issues**
   - Reduce FPS in settings
   - Close unnecessary applications
   - Ensure adequate RAM (8GB+)

4. **Streamlit Issues**
   ```bash
   pip install streamlit --upgrade
   streamlit run src/ui/streamlit_app.py
   ```

## 🎯 Future Enhancements

- **Advanced AI Models**: More sophisticated computer vision
- **Audio Analysis**: Voice communication and sound analysis
- **Team Coordination**: Analysis of team play and communication
- **Map-Specific Analysis**: Different strategies for different maps
- **Professional Integration**: Integration with professional coaching tools
- **Mobile App**: Companion mobile application

## 📝 License

MIT License - see LICENSE file for details

## ⚠️ Disclaimer

This software is for educational and training purposes only. It is not affiliated with Riot Games or Valorant. Use at your own discretion and in accordance with Valorant's terms of service.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Run `python test_installation.py` to verify setup
3. Check the logs in the `logs/` directory
4. Create an issue on the repository

---

**🎮 Happy gaming and improving!**