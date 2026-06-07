import { useFetch, Spinner, ErrorMsg } from '../App'
import './Drives.css'

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
              <td className="right">{(r.finish_rate * 100).toFixed(1) + '%'}</td>
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
  const offense = useFetch('/drives/offense/finishers')
  const defense = useFetch('/drives/defense/beaten')

  const loading = offense.loading || defense.loading
  const error   = offense.error   || defense.error

  if (loading) return <Spinner />
  if (error)   return <ErrorMsg msg={error} />

  return (
    <div>
      <div className="section-header">
        <h2 className="section-title">Drive Analytics</h2>
        <p className="section-sub">Drive creation, finishing, and defensive breakdowns</p>
      </div>

      <p className="sub-heading">MIL Drive Offense — Finishers</p>
      <div className="drives-glossary">
        <strong>Drives</strong> — when a ball-handler aggressively dribbles the ball toward the basket with the intent to score<br></br>
        <strong>Finish Rate</strong> - measuring player effiency at making shots on drives
      </div>
      <DriveOffenseTable data={offense.data} />

      <hr className="divider" />

      <p className="sub-heading">MIL Defenders Beaten Off Dribble</p>
      <div className="drives-glossary">
        <strong>Blowby%</strong> — when a ball-handler beats their defender off the dribble to gain an advantageous position. A higher blowby rate on offense indicates effective drive creation; a higher rate allowed on defense indicates difficulty staying in front of ball-handlers.

      </div>
      <DefenseBeatenTable data={defense.data} />
    </div>
  )
}