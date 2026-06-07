import { useState } from 'react'
import { useFetch, Spinner, ErrorMsg, pct } from '../App'
import './Lineups.css'

function LineupOffenseTable({ data }) {
  if (!data?.length) return <p style={{color:'var(--text3)',padding:'1rem'}}>No data</p>
  return (
    <div className="table-wrap">
      <table className="lineup-table">
        <thead>
          <tr>
            <th className="right">#</th>
            <th className="right">Chances</th>
            <th className="right">PTS</th>
            <th className="right">xPTS</th>
            <th className="right">FGA</th>
            <th className="right">FGM</th>
            <th className="right">FG%</th>
            <th className="right">3PA</th>
            <th className="right">3PM</th>
            <th className="right">3P%</th>
            <th className="right">TO</th>
            <th className="right">qSQ</th>
            <th className="right">qSP</th>
          </tr>
        </thead>
        <tbody>
          {data.map((r, i) => (
            <tr key={i}>
              <td className="right">{i + 1}</td>
              <td className="right">{r.chances ?? '—'}</td>
              <td className="right accent" style={{fontWeight:700}}>{r.pts_scored ?? 0}</td>
              <td className="right">{r.expected_points ?? '—'}</td>
              <td className="right">{r.fga ?? 0}</td>
              <td className="right">{r.fgm ?? 0}</td>
              <td className="right">{pct(r.fg_pct)}</td>
              <td className="right">{r.fga3 ?? 0}</td>
              <td className="right">{r.fg3m ?? 0}</td>
              <td className="right">{pct(r.fg3_pct)}</td>
              <td className="right" >{r.turnovers ?? 0}</td>
              <td className="right">{r.avg_qsq ?? '—'}</td>
              <td className="right">{r.avg_qsp ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function LineupDefenseTable({ data }) {
  if (!data?.length) return <p style={{color:'var(--text3)',padding:'1rem'}}>No data</p>
  return (
    <div className="table-wrap">
      <table className="lineup-table">
        <thead>
          <tr>
            <th className="right">#</th>
            <th className="right">Chances Defended</th>
            <th className="right">PTS Allowed</th>
            <th className="right">xPTS</th>
            <th className="right">Pts/Chance</th>
            <th className="right">FGA</th>
            <th className="right">FG%</th>
            <th className="right">3PA</th>
            <th className="right">3P%</th>
            <th className="right">TO Forced</th>
            <th className="right">Opp qSQ</th>
            <th className="right">Opp qSP</th>
          </tr>
        </thead>
        <tbody>
          {data.map((r, i) => (
            <tr key={i}>
              <td className="right">{i + 1}</td>
              <td className="right">{r.pts_allowed ?? 0}</td>
              <td className="right">{r.expected_points_allowed ?? '—'}</td>
              <td className="right">{r.chances_defended ?? '—'}</td>
              <td className="right">{r.pts_allowed_per_chance ?? '—'}</td>
              <td className="right">{r.fga_allowed ?? 0}</td>
              <td className="right">{pct(r.fg_pct_allowed)}</td>
              <td className="right">{r.fga3_allowed ?? 0}</td>
              <td className="right">{pct(r.fg3_pct_allowed)}</td>
              <td className="right accent">{r.turnovers_forced ?? 0}</td>
              <td className="right">{r.opp_avg_qsq ?? '—'}</td>
              <td className="right">{r.opp_avg_qsp ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function LineupPlayerKey({ data, type }) {
  if (!data?.length) return <p style={{color:'var(--text3)'}}>No player key data</p>

  const filtered = data.filter(r => r.lineup_type === type)
  if (!filtered.length) return <p style={{color:'var(--text3)'}}>No lineups found</p>

  return (
    <div className="lineup-key-grid">
      {filtered.map((row, i) => {
        const players = row.players ? row.players.split(', ') : []
        return (
          <div key={i} className="lineup-key-card">
            <div className="lineup-key-id">Lineup {i + 1}</div>
            <div className="lineup-key-players">
              {players.map((p, j) => (
                <div key={j} className="lineup-key-player">
                  <span className="lineup-key-dot" />
                  <span>{p}</span>
                </div>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default function Lineups() {
  const offense   = useFetch('/lineups/mil/offense')
  const defense   = useFetch('/lineups/mil/defense')
  const playerKey = useFetch('/lineups/mil/player-keys')

  const [showOffenseKey, setShowOffenseKey] = useState(false)
  const [showDefenseKey, setShowDefenseKey] = useState(false)

  const loading = offense.loading || defense.loading || playerKey.loading
  const error   = offense.error   || defense.error   || playerKey.error

  if (loading) return <Spinner />
  if (error)   return <ErrorMsg msg={error} />

  return (
    <div>
      <div className="section-header">
        <h2 className="section-title">Milwaukee Lineups</h2>
        <p className="section-sub">Lineup-level offensive and defensive performance metrics</p>
      </div>

      <div className="lineups-note">
        Each row represents a distinct 5-man lineup used by Milwaukee, ranked by number of 'chances' each lineup had on the offensive side, and for the defensive side we look at the number of 'chances' they defended. Use the Player Key buttons to see which players make up each lineup.
      </div>

      <div className="lineup-key-header">
        <p className="sub-heading" style={{margin:0}}>Offense — Top Lineups by Points Scored</p>
        <button className="lineup-key-toggle" onClick={() => setShowOffenseKey(v => !v)}>
          {showOffenseKey ? 'Hide' : 'Show'} Player Key
        </button>
      </div>
      <LineupOffenseTable data={offense.data} />

      {showOffenseKey && (
        <div className="lineup-key-section">
          <p className="sub-heading">Offense Lineup Player Key</p>
          <LineupPlayerKey data={playerKey.data} type="offense" />
        </div>
      )}

      <hr className="divider" />

      <div className="lineup-key-header">
        <p className="sub-heading" style={{margin:0}}>Defense — Lineups by Points Allowed</p>
        <button className="lineup-key-toggle" onClick={() => setShowDefenseKey(v => !v)}>
          {showDefenseKey ? 'Hide' : 'Show'} Player Key
        </button>
      </div>
      <LineupDefenseTable data={defense.data} />

      {showDefenseKey && (
        <div className="lineup-key-section">
          <p className="sub-heading">Defense Lineup Player Key</p>
          <LineupPlayerKey data={playerKey.data} type="defense" />
        </div>
      )}
    </div>
  )
}