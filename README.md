# MandiMitra AI — Harvest Intelligence Platform

A farmer-focused market decision workspace built from the supplied Google AI Studio project.

## Technology

- **Frontend:** React + Vite + JavaScript + Tailwind CSS + custom CSS
- **Main application server / Gemini advisor:** Node.js + Express
- **Market-data connector:** Python + FastAPI (optional service)
- **Market source:** AGMARKNET published mandi records through data.gov.in

Java is not included in the runtime. A Java service would duplicate the existing API layer and make local setup harder without adding a feature. The project uses JavaScript for the browser application and Python for the market-data connector.

## What's changed in this rebuild

- Login asks for preferred language (English, Kannada, Hindi), farmer name, mobile number, and locality. Locality starts blank so the farmer enters their own place.
- No crop is preselected. The farmer enters any crop name; known crops use the supplied crop profiles and unknown names get a clearly identified generic profile.
- The crop search is a compact, prominent entry point instead of showing a catalogue of every crop on the dashboard.
- One crop workspace contains grade/size selection, quantity and required-quantity alert, historical/forecast chart, shelf-life adjusted sell/wait recommendation, mandi ranking, net-profit comparison, and the personal AI advisor.
- Added a personal farm-expense calculator for transport, labour, packing, loading, other costs, sale rate, revenue and estimated net proceeds.
- Added an optional Python AGMARKNET connector. The UI distinguishes official published records from illustrative local estimates. It does not claim simulated values are live prices.
- Random automatic price-bump notifications have been disabled to avoid presenting simulated price movements as real market alerts.
- Added a premium emerald, ivory and champagne-gold visual system.

## Requirements

- Node.js 20 or newer (recommended)
- Python 3.10 or newer
- A Gemini API key for AI advisor/chat features
- A data.gov.in API key for official AGMARKNET records

## 1. Install frontend and Express server

Open this project folder in VS Code, then run:

```bash
npm install
```

Copy `.env.example` to `.env` and add your Gemini key:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
PORT=3000
MARKET_API_BASE_URL=http://127.0.0.1:8001
```

Start the application:

```bash
npm run dev
```

Open `http://localhost:3000`.

## 2. Enable official AGMARKNET data (optional but recommended)

Open a second terminal:

```bash
cd services/python_api
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `services/python_api/.env` and add your data.gov.in API key. Confirm the active AGMARKNET resource ID in your data.gov.in account/catalog before using it.

Start the connector:

```bash
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

The connector health check is `http://127.0.0.1:8001/health`.

## Important data and decision notes

- AGMARKNET/data.gov.in records are published market-arrival price records. They may not be intraday/live tick quotes; the source's update cadence applies.
- The existing local mandi ranking, transport deductions, crop history, and five-day forecast are estimates from the supplied demonstration dataset until replaced with verified local data and a validated forecasting model.
- The shelf-life model is an indicative decision aid, not a guarantee. Real storage conditions, grade, weather, disease, and buyer demand can change outcomes.
- Confirm market schedules, fees, transport availability, and final bids with the mandi before dispatch.
- Keep API keys in `.env` files; never commit them or expose them in frontend code.

## Build for production

```bash
npm run build
```

Set `NODE_ENV=production` and run:

```bash
npm start
```

## Folder map

```text
src/                    React application, components, styles and supplied demo data
server.js               Express API + Gemini endpoints + Python market-data proxy
services/python_api/    Optional AGMARKNET/data.gov.in connector
.env.example            Environment variable template
```
