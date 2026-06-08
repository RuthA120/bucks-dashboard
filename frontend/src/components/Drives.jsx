import { useFetch } from '../App'
import './Drives.css'

function DriveSummaryCards({ data }) {
  if (!data?.length) return null
  return (
    <div className="drive-summary-grid">
      {data.map((r, i) => {
        const teamClass = r.offense_team === 'MIL' ? 'mil' : 'cha'
        return (
          <div key={i} className="drive-summary-card">
            <div className="drive-summary-team">
              <span style={{fontSize: "2rem", fontWeight: "1000"}}>{r.offense_team}</span>
            </div>
            <div className="drive-summary-stats">
              <div className="drive-stat-item">
                <span className="drive-stat-value">{r.total_drives ?? 0}</span>
                <span className="drive-stat-label">Total Drives</span>
              </div>
              <div className="drive-stat-item">
                <span className="drive-stat-value">{r.drive_pts_scored ?? 0}</span>
                <span className="drive-stat-label">Points</span>
              </div>
              <div className="drive-stat-item">
                <span className="drive-stat-value">{r.pts_per_drive ?? '—'}</span>
                <span className="drive-stat-label">Pts / Drive</span>
              </div>
              <div className="drive-stat-item">
                <span className="drive-stat-value">{r.num_blowby_opportunities ?? 0}</span>
                <span className="drive-stat-label">Blowby Opps</span>
              </div>
              <div className="drive-stat-item">
                <span className="drive-stat-value">{r.blowbys_in_scoring_drives ?? 0}</span>
                <span className="drive-stat-label">Blowbys and Score</span>
              </div>
              <div className="drive-stat-item">
                <span className="drive-stat-value">
                  {r.blowby_success_rate != null
                    ? (r.blowby_success_rate * 100).toFixed(1) + '%'
                    : '—'}
                </span>
                <span className="drive-stat-label">Blowby Success</span>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

function DriveOffenseTable({ data }) {
  if (!data?.length) return <p style={{color:'var(--text3)',padding:'1rem'}}>No data</p>
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Player</th>
            <th className="right">Drives</th>
            <th className="right">PTS</th>
            <th className="right">Finish Rate</th>
          </tr>
        </thead>
        <tbody>
          {data.map((r, i) => (
            <tr key={i}>
              <td className="player-name">{r.player}</td>
              <td className="right">{r.drive_finish_attempts ?? 0}</td>
              <td className="right">{r.pts_scored ?? 0}</td>
              <td className="right">
                {r.finish_rate != null
                  ? (r.finish_rate * 100).toFixed(1) + '%'
                  : '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function DefenseBeatenTable({ data }) {
  if (!data?.length) return <p style={{color:'var(--text3)',padding:'1rem'}}>No data</p>
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Defender</th>
            <th className="right">Beaten on Blowby</th>
            <th className="right">Blowby Attempts</th>
            <th className="right">Blowby%</th>
          </tr>
        </thead>
        <tbody>
          {data.map((r, i) => {
            const rate = r.blowby_rate_allowed != null
              ? (r.blowby_rate_allowed * 100).toFixed(1) + '%'
              : '—'
            return (
              <tr key={i}>
                <td className="player-name">{r.defender}</td>
                <td className="right">{r.blowbys_allowed ?? 0}</td>
                <td className="right">{r.blowby_opportunities ?? 0}</td>
                <td className="right">{rate}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default function Drives() {
  const driveStats = useFetch('/drives/drive-offense')
  const offense    = useFetch('/drives/offense/finishers')
  const defense    = useFetch('/drives/defense/beaten')

  return (
    <div>
      <div className="section-header">
        <h2 className="section-title">Drive Analytics</h2>
        <p className="section-sub">Drive creation, finishing, and defensive breakdowns</p>
      </div>

      <p className="sub-heading">Team Drive Summary</p>
      <div className="drives-glossary">
        <strong>Drives</strong> — when a ball-handler aggressively dribbles toward the basket with intent to score<br />
        <strong>Blowby Success</strong> — rate at which blowbys resulted in scoring drives
      </div>
      <DriveSummaryCards data={driveStats.data} />

      <hr className="divider" />

      <p className="sub-heading">MIL Drive Offense — Finishers</p>
      <div className="drives-glossary">
        <strong>Finish Rate</strong> — measuring player efficiency at making shots on drives
      </div>
      <DriveOffenseTable data={offense.data} />

      <hr className="divider" />

      <p className="sub-heading">MIL Defenders Beaten Off Dribble</p>
      <div className="drives-glossary">
        <strong>Blowby%</strong> — when a ball-handler beats their defender off the dribble to gain an advantageous position. A higher rate allowed indicates difficulty staying in front of ball-handlers.
      </div>
      <DefenseBeatenTable data={defense.data} />
    </div>
  )
}