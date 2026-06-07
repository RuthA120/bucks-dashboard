import { useFetch, pct } from '../App'
import './Overview.css'
import courtDiagram from '../assets/court-regions.jpeg'

function TeamStatsTable({ data }) {
  if (!data?.length) return null
  const mil = data.find(r => r.team === 'MIL')
  const cha = data.find(r => r.team === 'CHA')
  const rows = [
    { label: 'Points',    mil: mil?.pts,          cha: cha?.pts          },
    { label: 'FGA',       mil: mil?.fga,          cha: cha?.fga          },
    { label: 'FGM',       mil: mil?.fgm,          cha: cha?.fgm          },
    { label: 'FG%',       mil: pct(mil?.fg_pct),  cha: pct(cha?.fg_pct)  },
    { label: '3PA',       mil: mil?.fga3,         cha: cha?.fga3         },
    { label: '3PM',       mil: mil?.fg3m,         cha: cha?.fg3m         },
    { label: '3P%',       mil: pct(mil?.fg3_pct), cha: pct(cha?.fg3_pct) },
    { label: '2PA',       mil: mil?.fga2,         cha: cha?.fga2         },
    { label: '2PM',       mil: mil?.fg2m,         cha: cha?.fg2m         },
    { label: '2P%',       mil: pct(mil?.fg2_pct), cha: pct(cha?.fg2_pct) },
    { label: 'Turnovers', mil: mil?.turnovers,    cha: cha?.turnovers    },
  ]
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Stat</th>
            <th className="right" style={{color:'#00693A'}}>MIL</th>
            <th className="right" style={{color:'#05a8c5'}}>CHA</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.label}>
              <td className="muted">{r.label}</td>
              <td className="right accent">{r.mil ?? '—'}</td>
              <td className="right cha-color">{r.cha ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function ReboundTable({ data }) {
  if (!data?.length) return null
  const mil = data.find(r => r.team === 'MIL')
  const cha = data.find(r => r.team === 'CHA')
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Rebounds</th>
            <th className="right" style={{color:'#00693A'}}>MIL</th>
            <th className="right" style={{color:'#05a8c5'}}>CHA</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="muted">Defensive</td>
            <td className="right accent">{mil?.def_reb ?? '—'}</td>
            <td className="right cha-color">{cha?.def_reb ?? '—'}</td>
          </tr>
          <tr>
            <td className="muted">Offensive</td>
            <td className="right accent">{mil?.off_reb ?? '—'}</td>
            <td className="right cha-color">{cha?.off_reb ?? '—'}</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

function ShotRegions({ data, team }) {
  if (!data?.length) return null
  const teamData = data.filter(r => r.team === team)
  if (!teamData.length) return <p style={{color:'var(--text3)',fontSize:'0.9rem'}}>No data</p>
  return (
    <div className="regions-layout">
      <div className="regions-grid">
        {teamData.map(r => (
          <div key={r.region} className="region-card">
            <div className="region-name">{r.region}</div>
            <div className="region-pct">{pct(r.fg_pct)}</div>
            <div className="region-attempts">{r.fgm}/{r.fga} FGM/FGA</div>
          </div>
        ))}
      </div>
      <img
        src={courtDiagram}
        alt="Court shot regions diagram"
        className="regions-court-img"
      />
    </div>
  )
}

export default function Overview() {
  const stats = useFetch('/overview/stats')
  const reb   = useFetch('/overview/rebounding')
  const shots = useFetch('/overview/shot-chart')

  const loading = stats.loading || reb.loading || shots.loading
  const error   = stats.error   || reb.error   || shots.error

  const mil = stats.data?.find(r => r.team === 'MIL')
  const cha = stats.data?.find(r => r.team === 'CHA')

  return (
    <div>
      <div className="section-header">
        <h2 className="section-title">Game Overview</h2>
        <p className="section-sub">MIL vs CHA — January 22, 2026</p>
      </div>

      <div className="card overview-score-hero">
        <div>
          <div className="score-team-label">Milwaukee</div>
          <div className="score-number mil">{mil?.pts ?? '—'}</div>
        </div>
        <div className="score-final">FINAL</div>
        <div>
          <div className="score-team-label">Charlotte</div>
          <div className="score-number cha">{cha?.pts ?? '—'}</div>
        </div>
      </div>

      <div className="two-col">
        <div>
          <p className="sub-heading">Team Stats</p>
          <TeamStatsTable data={stats.data} />
        </div>
        <div>
          <p className="sub-heading">Rebounding</p>
          <ReboundTable data={reb.data} />
        </div>
      </div>

      <hr className="divider" />
      <p className="sub-heading">Shot Regions — Milwaukee</p>
      <ShotRegions data={shots.data} team="MIL" />

      <hr className="divider" />
      <p className="sub-heading">Shot Regions — Charlotte</p>
      <ShotRegions data={shots.data} team="CHA" />
    </div>
  )
}
