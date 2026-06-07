import { useFetch, Spinner, ErrorMsg, pct } from '../App'
import './Players.css'

function LeaderCard({ category, data, statKey, statLabel }) {
  if (!data) return null
  const teamClass = data.team === 'MIL' ? 'mil' : 'cha'
  return (
    <div className="leader-card">
      <div className="leader-category">{category}</div>
      <div className="leader-name">{data.player}</div>
      <div className="leader-stat">{data[statKey] ?? '—'}</div>
      <div className="leader-sub">{statLabel}</div>
      <div className="leader-team">
        <span className={`team-badge ${teamClass}`}>{data.team}</span>
      </div>
    </div>
  )
}

function BoxScoreTable({ rows }) {
  if (!rows?.length) return <p className="no-data">No data</p>
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Player</th>
            <th className="right">PTS</th>
            <th className="right">FGA</th>
            <th className="right">FGM</th>
            <th className="right">FG%</th>
            <th className="right">3PM</th>
            <th className="right">3P%</th>
            <th className="right">FTA</th>
            <th className="right">FTM</th>
            <th className="right">FT%</th>
            <th className="right">REB</th>
            <th className="right">AST</th>
            <th className="right">STL</th>
            <th className="right">BLK</th>
            <th className="right">TO</th>
            <th className="right">PF</th>
            <th className="right">+/-</th>
            <th className="right">qSQ</th>
            <th className="right">qSP</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td className="player-name">{r.player}</td>
              <td className="right pts-col">{r.pts ?? 0}</td>
              <td className="right muted">{r.fga ?? 0}</td>
              <td className="right muted">{r.fgm ?? 0}</td>
              <td className="right">{pct(r.fg_pct)}</td>
              <td className="right muted">{r.fg3m ?? 0}</td>
              <td className="right">{pct(r.fg3_pct)}</td>
              <td className="right muted">{r.fta ?? 0}</td>
              <td className="right muted">{r.ft ?? 0}</td>
              <td className="right">{pct(r.ft_pct)}</td>
              <td className="right">{r.trb ?? 0}</td>
              <td className="right">{r.ast ?? 0}</td>
              <td className="right">{r.stl ?? 0}</td>
              <td className="right">{r.blk ?? 0}</td>
              <td className="right">
                {r.turnovers ?? 0}
              </td>
              <td className="right muted">{r.pf ?? 0}</td>
              <td className="right" style={{
                color: r.plus_minus > 0 ? '#6fcf97' : r.plus_minus < 0 ? '#ff6b6b' : 'inherit',
                fontWeight: 600
              }}>
                {r.plus_minus > 0 ? '+' : ''}{r.plus_minus ?? 0}
              </td>
              <td className="right muted">{r.avg_qsq ?? '—'}</td>
              <td className="right muted">{r.avg_qsp ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function TeamSection({ team, label, accentColor, scoringData, teamLeaders }) {
  const rows = scoringData?.filter(r => r.team === team) ?? []
  const l = teamLeaders ?? {}

  return (
    <div className="team-section">
      <div className="team-section-header" style={{borderColor: accentColor}}>
        <span className="team-section-name" style={{color: accentColor}}>{label}</span>
      </div>

      <p className="sub-heading" style={{marginTop: '1.25rem'}}>Leaders</p>
      <div className="leader-grid" style={{marginBottom: '1.5rem'}}>
        <LeaderCard category="Points"   data={l.scoring_leader}       statKey="pts"    statLabel="PTS" />
        <LeaderCard category="Rebounds" data={l.rebounding_leader}    statKey="trb"    statLabel="REB" />
        <LeaderCard category="Assists"  data={l.assist_leader}        statKey="ast"    statLabel="AST" />
        <LeaderCard category="Stocks"   data={l.steals_blocks_leader} statKey="stocks" statLabel="STL+BLK" />
      </div>

      <p className="sub-heading">Box Score</p>
      <BoxScoreTable rows={rows} />
    </div>
  )
}

export default function Players() {
  const scoring = useFetch('/players/scoring')
  const leaders = useFetch('/players/leaders')

  const loading = scoring.loading || leaders.loading
  const error   = scoring.error   || leaders.error

  if (loading) return <Spinner />
  if (error)   return <ErrorMsg msg={error} />

  const milLeaders = leaders.data?.MIL ?? {}
  const chaLeaders = leaders.data?.CHA ?? {}

  return (
    <div>
      <div className="section-header">
        <h2 className="section-title">Player Stats</h2>
        <p className="section-sub">Individual performance breakdown by team</p>
      </div>

      <TeamSection
        team="MIL"
        label="Milwaukee Bucks"
        accentColor="var(--mil-accent)"
        scoringData={scoring.data}
        teamLeaders={milLeaders}
      />

      <hr className="divider" />

      <TeamSection
        team="CHA"
        label="Charlotte Hornets"
        accentColor="var(--cha-color)"
        scoringData={scoring.data}
        teamLeaders={chaLeaders}
      />
    </div>
  )
}