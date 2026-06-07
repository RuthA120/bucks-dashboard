import { useFetch, Spinner, ErrorMsg } from '../App'
import './PickAndRoll.css'

function CoverageBar({ label, count, pts, ptsPerAction, colorClass, maxCount }) {
  const width = maxCount > 0 ? Math.round((count / maxCount) * 100) : 0
  return (
    <div className="coverage-block">
      <div className="coverage-top">
        <span className="coverage-label">{label}</span>
        <span className="coverage-meta">{count} possessions · {ptsPerAction ?? '—'} pts/poss</span>
      </div>
      <div className="bar-track">
        <div className={`bar-fill ${colorClass}`} style={{width:`${width}%`}} />
      </div>
      <div className="coverage-pts-note">{pts} pts allowed</div>
    </div>
  )
}

function PnROffenseGrid({ data, team }) {
  const row = data?.find(r => r.team === team)
  if (!row) return <p style={{color:'var(--text3)'}}>No data</p>
  const colorClass = team === 'MIL' ? 'mil' : 'cha'
  const stats = [
    { label: 'Roll Actions', val: row.roll_actions },
    { label: 'Roll Pts',     val: row.roll_pts },
    { label: 'Pts/Roll',     val: row.pts_per_roll },
    { label: 'Roll xPts',    val: row.roll_expected_points },
    { label: 'Pop Actions',  val: row.pop_actions },
    { label: 'Pop Pts',      val: row.pop_pts },
    { label: 'Pts/Pop',      val: row.pts_per_pop },
    { label: 'Pop xPts',     val: row.pop_expected_points },
  ]
  return (
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'10px'}}>
      {stats.map(s => (
        <div key={s.label} className="pnr-stat-card">
          <div className="pnr-stat-label">{s.label}</div>
          <div className={`pnr-stat-value ${colorClass}`}>{s.val ?? '—'}</div>
        </div>
      ))}
    </div>
  )
}

function CoverageSection({ data }) {
  if (!data?.length) return <p style={{color:'var(--text3)'}}>No data</p>
  return (
    <div>
      {data.map((row, i) => {
        const maxCount = Math.max(row.over_count || 0, row.under_count || 0, row.switch_count || 0)
        return (
          <div key={i} className="card" style={{marginBottom:'1rem'}}>
            <div className="card-title">{row.team} Defense</div>
            <CoverageBar label="Go Over"  count={row.over_count   || 0} pts={row.pts_allowed_over   || 0} ptsPerAction={row.pts_per_over}   colorClass="over"   maxCount={maxCount} />
            <CoverageBar label="Go Under" count={row.under_count  || 0} pts={row.pts_allowed_under  || 0} ptsPerAction={row.pts_per_under}  colorClass="under"  maxCount={maxCount} />
            <CoverageBar label="Switch"   count={row.switch_count || 0} pts={row.pts_allowed_switch || 0} ptsPerAction={row.pts_per_switch} colorClass="switch" maxCount={maxCount} />
          </div>
        )
      })}
    </div>
  )
}

export default function PickAndRoll() {
  const offense      = useFetch('/pick-and-roll/offense')
  const rollCoverage = useFetch('/pick-and-roll/defense/roll-coverage')
  const popCoverage  = useFetch('/pick-and-roll/defense/pop-coverage')

  const loading = offense.loading || rollCoverage.loading || popCoverage.loading
  const error   = offense.error   || rollCoverage.error   || popCoverage.error

  if (loading) return <Spinner />
  if (error)   return <ErrorMsg msg={error} />

  return (
    <div>
      <div className="section-header">
        <h2 className="section-title">Pick &amp; Roll / Pop</h2>
        <p className="section-sub">Screen offense efficiency and defensive coverage breakdowns</p>
      </div>

      <p className="sub-heading">Offense — Roll &amp; Pop Stats</p>
      <div className="two-col" style={{marginBottom:'2rem'}}>
        <div>
          <p className="pnr-team-label" style={{color:'var(--mil-accent)'}}>Milwaukee</p>
          <PnROffenseGrid data={offense.data} team="MIL" />
        </div>
        <div>
          <p className="pnr-team-label" style={{color:'var(--cha-color)'}}>Charlotte</p>
          <PnROffenseGrid data={offense.data} team="CHA" />
        </div>
      </div>

      <hr className="divider" />
      <p className="sub-heading">Roll Coverage — Points Allowed by Scheme</p>
      <CoverageSection data={rollCoverage.data} />

      <hr className="divider" />
      <p className="sub-heading">Pop Coverage — Points Allowed by Scheme</p>
      <CoverageSection data={popCoverage.data} />
    </div>
  )
}