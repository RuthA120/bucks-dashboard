import { useState, useEffect } from 'react'
import Overview from './components/Overview'
import Players from './components/Players'
import Drives from './components/Drives'
import PickAndRoll from './components/PickAndRoll'
import ShotQuality from './components/ShotQuality'
import './App.css'

const API = 'http://localhost:8000'

const NAV = [
  { id: 'overview',     label: 'Overview' },
  { id: 'players',      label: 'Players' },
  { id: 'drives',       label: 'Drives' },
  { id: 'pick-and-roll',label: 'Pick & Roll' },
  { id: 'shot-quality', label: 'Shot Quality' }
]

export function useFetch(url) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  useEffect(() => {
    setLoading(true)
    setError(null)
    fetch(`${API}${url}`)
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(d => { setData(d); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }, [url])
  return { data, loading, error }
}

export function pct(val) {
  if (val == null) return '—'
  return (val * 100).toFixed(1) + '%'
}

export function round(val, dec = 1) {
  if (val == null) return '—'
  return Number(val).toFixed(dec)
}

export default function App() {
  const [section, setSection] = useState('overview')

  const pages = {
    overview:       <Overview />,
    players:        <Players />,
    drives:         <Drives />,
    'pick-and-roll':<PickAndRoll />,
    'shot-quality': <ShotQuality />,
  }

  return (
    <div className="app">
      <header className="site-header">
        <div className="header-inner">
          <div className="matchup">
            <span className="team mil">MIL</span>
            <span className="vs">VS</span>
            <span className="team cha">CHA</span>
          </div>
          <div className="game-meta">
            <span>January 22, 2026 Game Report</span>
          </div>
        </div>
      </header>

      <nav className="site-nav">
        {NAV.map(n => (
          <button
            key={n.id}
            className={`nav-btn${section === n.id ? ' active' : ''}`}
            onClick={() => setSection(n.id)}
          >
            {n.label}
          </button>
        ))}
      </nav>

      <main className="site-main">
        {pages[section]}
      </main>
    </div>
  )
}
