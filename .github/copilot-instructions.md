# Copilot Instructions for ULTRON Atlas GUI & Web Dashboard

## Big Picture Architecture
- **Multi-component system**: Combines Python backends (`ultron_web_server.py`, `launch_ultron_web.py`, etc.), React-based SPA (`ultron-agent/src/`), and pure HTML/JS dashboards (`public-dashboard/`, `ultron-dashboard.js`).
- **Frontend Dashboards**: `public-dashboard/` is a self-contained static dashboard (no backend required). `ultron-agent/` is a React app for richer UI and integration.
- **Backend Services**: Python scripts provide system metrics, agent logic, and serve web UIs. Communication is typically via HTTP endpoints or local server.
- **Integration**: Frontends may connect to Python backends for real data, but can run in demo mode with randomized metrics.

## Developer Workflows
- **Frontend (React)**:
  - `cd ultron-agent && npm start` to run locally
  - `npm test` for unit tests
  - `npm run build` for production build
- **Static Dashboard**:
  - `cd public-dashboard && python -m http.server 8000` to serve locally
  - No build step required; deploy `index.html` directly
- **Backend (Python)**:
  - Run `launch_ultron_web.py` or `ultron_web_server.py` for web server
  - Use `real-system-monitor.py` for real metrics

## Project-Specific Conventions
- **Theme**: Cyberpunk ULTRON blue (`#00d4ff`), green success (`#00ff88`), dark backgrounds
- **Metrics**: Demo dashboards use randomized values; real dashboards connect to Python for live stats
- **Activity Log**: Chronological, newest at bottom, auto-scroll, 50-message limit
- **AI Chat**: Message history, typing indicator, customizable responses in `aiResponses` array
- **System Controls**: Restart, clear logs, export, health check, performance report

## Integration Points & Patterns
- **Python <-> JS/React**: Use HTTP endpoints for data exchange; see `ultron_web_server.py` and React hooks/components
- **Static Hosting**: `public-dashboard/index.html` can be deployed to Netlify, Vercel, GitHub Pages, or Surge.sh
- **Customization**: Colors, metrics, and AI responses are easily editable in dashboard source files

## Key Files & Directories
- `public-dashboard/index.html`: Pure HTML/JS dashboard
- `ultron-agent/src/`: React app source
- `ultron_web_server.py`, `launch_ultron_web.py`: Python web backends
- `real-system-monitor.py`: Real system metrics
- `imgs/`: Cyberpunk art assets

## Example Patterns
- **Serve dashboard locally**:
  ```sh
  cd public-dashboard
  python -m http.server 8000
  ```
- **Run React app**:
  ```sh
  cd ultron-agent
  npm start
  ```
- **Start backend server**:
  ```sh
  python launch_ultron_web.py
  ```

---
For questions, see the relevant README files or ask for clarification on specific workflows or integration points.
